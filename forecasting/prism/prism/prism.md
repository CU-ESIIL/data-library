---
tags:
- forecasting
- prism
- innovation-summit-2025
---

# PRISM (U.S. Gridded Climate)

PRISM offers terrain-aware, quality-controlled climate normals and grids for the conterminous United States. Monthly data extend back to 1895 and daily to 1981, supplying consistent temperature and precipitation fields for modeling, drought monitoring, and ecological studies [Daly et al., 2008](https://doi.org/10.1175/2007JAMC1356.1). The service delivers Cloud-Optimized GeoTIFFs inside ZIP files so you can stream them directly with GDAL.

## Python
Paste into your Python console:
```python
from osgeo import gdal
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
from typing import Union, Tuple, Optional

# ---------- PRISM helpers (VSI) ----------
_RES_CODE = {"4km": "25m", "800m": "30s", "400m": "15s"}

def _as_datecode(date: Union[str, dt.date, dt.datetime], freq: str) -> Tuple[str, str]:
    """
    Parse date for PRISM naming. Accepts:
      daily:    'YYYY-MM-DD' or 'YYYYMMDD'
      monthly:  'YYYY-MM'    or 'YYYYMM'
      annual:   'YYYY'
    Also accepts datetime/date objects.
    Returns: (datecode, yyyy)
    """
    if isinstance(date, (dt.datetime, dt.date)):
        d = date if isinstance(date, dt.date) and not isinstance(date, dt.datetime) else date.date()
    elif isinstance(date, str):
        s = date.strip()
        if freq == "daily":
            # Try ISO first, then compact
            try:
                d = dt.datetime.strptime(s, "%Y-%m-%d").date()
            except ValueError:
                d = dt.datetime.strptime(s, "%Y%m%d").date()
        elif freq == "monthly":
            # Use day=1 internally
            try:
                d = dt.datetime.strptime(s, "%Y-%m").date().replace(day=1)
            except ValueError:
                d = dt.datetime.strptime(s, "%Y%m").date().replace(day=1)
        elif freq == "annual":
            d = dt.datetime.strptime(s, "%Y").date().replace(month=1, day=1)
        else:
            raise ValueError("freq must be one of: 'daily','monthly','annual'")
    else:
        raise TypeError("date must be str, datetime, or date")

    if freq == "daily":
        return d.strftime("%Y%m%d"), d.strftime("%Y")
    elif freq == "monthly":
        return d.strftime("%Y%m"), d.strftime("%Y")
    else:  # annual
        return d.strftime("%Y"), d.strftime("%Y")

def build_prism_vsi(
    variable: str = "tmax",
    date: Union[str, dt.date, dt.datetime] = "2025-07-15",
    resolution: str = "800m",
    region: str = "us",
    freq: str = "daily",
    network: str = "an",
) -> str:
    if resolution not in _RES_CODE:
        raise ValueError("resolution must be one of {'800m','4km','400m'}")
    datecode, yyyy = _as_datecode(date, freq)
    res_code = _RES_CODE[resolution]
    base_dir = f"https://data.prism.oregonstate.edu/time_series/{region}/{network}/{resolution}/{variable}/{freq}/{yyyy}/"
    zip_name = f"prism_{variable}_{region}_{res_code}_{datecode}.zip"
    tif_name = f"prism_{variable}_{region}_{res_code}_{datecode}.tif"
    return f"/vsizip//vsicurl/{base_dir}{zip_name}/{tif_name}"

def gdal_open_prism(**kwargs) -> gdal.Dataset:
    vsi = build_prism_vsi(**kwargs)
    gdal.SetConfigOption("GDAL_DISABLE_READDIR_ON_OPEN", "YES")
    gdal.SetConfigOption("CPL_VSIL_CURL_ALLOWED_EXTENSIONS", ".zip,.tif,.xml,.stx,.prj,.aux.xml")
    ds = gdal.Open(vsi, gdal.GA_ReadOnly)
    if ds is None:
        raise RuntimeError(f"GDAL failed to open PRISM via VSI:\n{vsi}")
    return ds

def _extent_from_gt(ds) -> Tuple[float, float, float, float]:
    gt = ds.GetGeoTransform()
    w = ds.RasterXSize
    h = ds.RasterYSize
    xmin = gt[0]
    ymax = gt[3]
    xmax = xmin + w * gt[1]
    ymin = ymax + h * gt[5]
    return (xmin, xmax, ymin, ymax)

def plot_prism(
    variable="tmax",
    date="2025-07-15",
    resolution="800m",
    freq="daily",
    bbox: Optional[Tuple[float, float, float, float]] = None,  # minx,miny,maxx,maxy
    title: Optional[str] = None,
    vmin=None,
    vmax=None,
):
    """
    Stream a PRISM raster and plot it.
    If bbox is provided, data are warped/cropped in-memory before plotting.
    """
    ds = gdal_open_prism(variable=variable, date=date, resolution=resolution, freq=freq)

    # Optionally crop to bbox using a WarpedVRT (no download, server-side reads)
    if bbox:
        minx, miny, maxx, maxy = bbox
        warp_opts = gdal.WarpOptions(
            format="VRT",
            outputBounds=(minx, miny, maxx, maxy),
            dstSRS="EPSG:4326",
            resampleAlg="nearest"
        )
        vrt = gdal.Warp("", ds, options=warp_opts)
        src = vrt
    else:
        src = ds

    band = src.GetRasterBand(1)
    arr = band.ReadAsArray()
    arr = np.where(arr == band.GetNoDataValue(), np.nan, arr)

    extent = _extent_from_gt(src)
    plt.figure(figsize=(8, 6))
    im = plt.imshow(arr, extent=extent, origin="upper", vmin=vmin, vmax=vmax)
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    if title is None:
        title = f"PRISM {variable.upper()} ({freq}) {date}"
    plt.title(title)
    cb = plt.colorbar(im, shrink=0.85)
    cb.set_label(f"{variable} (native units)")
    plt.tight_layout()
    plt.show()

# 1) PRISM: daily max temp for Colorado Front Range, 2025-07-15
plot_prism(
    variable="tmax",
    date="2025-07-15",
    resolution="800m",
    freq="daily",
    bbox=[-106.0, 39.0, -104.5, 40.5],  # minx,miny,maxx,maxy
    title="PRISM TMAX daily (°C×10) — Front Range"
)

# 2) PRISM: monthly precipitation for March 2024, CONUS view
plot_prism(variable="ppt", date="2024-03", freq="monthly", resolution="4km")
```

### Example: Stream PRISM to a polygon

Building on the point example above, the script below uses a GeoJSON polygon to
clip PRISM data on the fly, warp it to EPSG:4326, and optionally return stats
for the clipped grid.

```python
#!/usr/bin/env python3
"""
stream_prism_to_polygon()
- Streams PRISM via /vsicurl inside /vsizip (no manual download)
- Clips/crops to a user-provided polygon (GeoJSON/GPKG/SHP path, GeoJSON dict/str, or WKT)
- Warps to EPSG:4326 for easy plotting
- Optionally returns data array, extent, and simple stats
"""

from __future__ import annotations
from osgeo import gdal, ogr, osr
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
from typing import Union, Tuple, Optional, Dict, Any
import json
import uuid

# Enable GDAL exceptions (GDAL 4.0 will default to this)
gdal.UseExceptions()

# ---------------- PRISM helpers ---------------- #
_RES_CODE = {"4km": "25m", "800m": "30s", "400m": "15s"}

def _as_datecode(date: Union[str, dt.date, dt.datetime], freq: str) -> Tuple[str, str]:
    if isinstance(date, (dt.datetime, dt.date)):
        d = date if isinstance(date, dt.date) and not isinstance(date, dt.datetime) else date.date()
    elif isinstance(date, str):
        s = date.strip()
        if freq == "daily":
            try: d = dt.datetime.strptime(s, "%Y-%m-%d").date()
            except ValueError: d = dt.datetime.strptime(s, "%Y%m%d").date()
        elif freq == "monthly":
            try: d = dt.datetime.strptime(s, "%Y-%m").date().replace(day=1)
            except ValueError: d = dt.datetime.strptime(s, "%Y%m").date().replace(day=1)
        elif freq == "annual":
            d = dt.datetime.strptime(s, "%Y").date().replace(month=1, day=1)
        else:
            raise ValueError("freq must be one of: 'daily','monthly','annual'")
    else:
        raise TypeError("date must be str, datetime, or date")

    if freq == "daily":   return d.strftime("%Y%m%d"), d.strftime("%Y")
    if freq == "monthly": return d.strftime("%Y%m"),   d.strftime("%Y")
    return d.strftime("%Y"), d.strftime("%Y")

def _build_prism_vsi(variable: str, date, resolution: str, region: str, freq: str, network: str) -> str:
    if resolution not in _RES_CODE:
        raise ValueError("resolution must be one of {'800m','4km','400m'}")
    datecode, yyyy = _as_datecode(date, freq)
    res_code = _RES_CODE[resolution]
    base_dir = f"https://data.prism.oregonstate.edu/time_series/{region}/{network}/{resolution}/{variable}/{freq}/{yyyy}/"
    zip_name = f"prism_{variable}_{region}_{res_code}_{datecode}.zip"
    tif_name = f"prism_{variable}_{region}_{res_code}_{datecode}.tif"
    return f"/vsizip//vsicurl/{base_dir}{zip_name}/{tif_name}"

def _gdal_open_prism(**kwargs) -> gdal.Dataset:
    vsi = _build_prism_vsi(**kwargs)
    gdal.SetConfigOption("GDAL_DISABLE_READDIR_ON_OPEN", "YES")
    gdal.SetConfigOption("CPL_VSIL_CURL_ALLOWED_EXTENSIONS", ".zip,.tif,.xml,.stx,.prj,.aux.xml")
    ds = gdal.Open(vsi, gdal.GA_ReadOnly)
    if ds is None:
        raise RuntimeError(f"GDAL failed to open PRISM via VSI:\n{vsi}")
    return ds

def _extent_from_gt(ds) -> Tuple[float, float, float, float]:
    gt = ds.GetGeoTransform()
    w, h = ds.RasterXSize, ds.RasterYSize
    xmin, ymax = gt[0], gt[3]
    xmax, ymin = xmin + w * gt[1], ymax + h * gt[5]
    return (xmin, xmax, ymin, ymax)

# --------------- Polygon input helpers --------------- #
def _write_geojson_vsimmem(geojson_obj) -> str:
    geojson_str = json.dumps(geojson_obj) if isinstance(geojson_obj, dict) else str(geojson_obj)
    path = f"/vsimem/cutline_{uuid.uuid4().hex}.geojson"
    gdal.FileFromMemBuffer(path, geojson_str.encode("utf-8"))
    return path

def _wkt_to_geojson_vsimmem(wkt: str, srs_epsg: str = "EPSG:4326") -> str:
    sr = osr.SpatialReference(); sr.SetFromUserInput(srs_epsg)
    geom = ogr.CreateGeometryFromWkt(wkt)
    if geom is None:
        raise ValueError("Could not parse WKT geometry.")
    feat = ogr.Feature(ogr.FeatureDefn()); feat.SetGeometry(geom)
    ds = ogr.GetDriverByName("GeoJSON").CreateDataSource("/vsimem/tmp_geojson.json")
    try:
        layer = ds.CreateLayer("cutline", srs=sr, geom_type=ogr.wkbUnknown); layer.CreateFeature(feat); ds.SyncToDisk()
        vsipath = f"/vsimem/cutline_{uuid.uuid4().hex}.geojson"
        buf = gdal.VSIGetMemFileBuffer("/vsimem/tmp_geojson.json", 0); gdal.FileFromMemBuffer(vsipath, buf)
        return vsipath
    finally:
        gdal.Unlink("/vsimem/tmp_geojson.json")

def _normalize_cutline_input(cutline, srs: str = "EPSG:4326") -> Tuple[Optional[str], Optional[str]]:
    if cutline is None: return None, None
    if isinstance(cutline, str) and cutline.lower().endswith((".geojson", ".json", ".gpkg", ".shp", ".zip")):
        return cutline, None
    if isinstance(cutline, str) and cutline.strip().upper().startswith(("POLYGON", "MULTIPOLYGON")):
        return _wkt_to_geojson_vsimmem(cutline, srs), None
    return _write_geojson_vsimmem(cutline), None

# ----------------- MAIN ONE-CALL FUNCTION ----------------- #
def stream_prism_to_polygon(
    polygon: Union[str, dict],
    polygon_srs: str = "EPSG:4326",
    *,
    variable: str = "tmax",
    date: Union[str, dt.date, dt.datetime] = "2025-07-15",
    resolution: str = "800m",
    freq: str = "daily",
    region: str = "us",
    network: str = "an",
    title: Optional[str] = None,
    vmin: Optional[float] = None,
    vmax: Optional[float] = None,
    mask_outside: bool = True,
    return_array: bool = False,
    compute_stats: bool = False
) -> Optional[Dict[str, Any]]:
    ds = _gdal_open_prism(variable=variable, date=date, resolution=resolution,
                          region=region, freq=freq, network=network)

    cutline_path, cutline_layer = _normalize_cutline_input(polygon, polygon_srs)

    warp_opts = gdal.WarpOptions(
        format="VRT",
        dstSRS="EPSG:4326",
        resampleAlg="nearest",
        cutlineDSName=cutline_path,
        cutlineLayer=cutline_layer,
        cropToCutline=True,
        dstAlpha=False,
        warpOptions=[f"CUTLINE_SRS={polygon_srs}", f"INIT_DEST={'NO_DATA' if mask_outside else '0'}"],
    )
    vrt = gdal.Warp("", ds, options=warp_opts)
    if vrt is None:
        raise RuntimeError("GDAL.Warp failed to build VRT with the provided polygon.")

    band = vrt.GetRasterBand(1)
    nodata = band.GetNoDataValue()
    arr = band.ReadAsArray()
    if nodata is not None:
        arr = np.where(arr == nodata, np.nan, arr)

    extent = _extent_from_gt(vrt)
    plt.figure(figsize=(8, 6))
    im = plt.imshow(arr, extent=extent, origin="upper", vmin=vmin, vmax=vmax)
    plt.xlabel("Longitude"); plt.ylabel("Latitude")
    if title is None:
        title = f"PRISM {variable.upper()} ({freq}) {date}"
    plt.title(title)
    cb = plt.colorbar(im, shrink=0.85); cb.set_label(f"{variable} (native units)")
    plt.tight_layout(); plt.show()

    if not return_array and not compute_stats:
        return None

    out: Dict[str, Any] = {"array": arr, "extent": extent, "nodata": nodata}
    if compute_stats:
        finite = np.isfinite(arr)
        if finite.any():
            out["stats"] = {
                "count": int(finite.sum()),
                "mean": float(np.nanmean(arr)),
                "min": float(np.nanmin(arr)),
                "max": float(np.nanmax(arr)),
                "std": float(np.nanstd(arr)),
            }
        else:
            out["stats"] = {"count": 0, "mean": np.nan, "min": np.nan, "max": np.nan, "std": np.nan}
    return out

# ---------------- Example usage ---------------- #
if __name__ == "__main__":
    boulder_poly = {
      "type": "FeatureCollection",
      "features": [{
        "type": "Feature",
        "properties": {},
        "geometry": {"type": "Polygon", "coordinates": [[
          [-105.38, 40.15], [-105.10, 40.25], [-104.95, 40.15],
          [-104.95, 39.95], [-105.15, 39.90], [-105.38, 40.00],
          [-105.38, 40.15]
        ]]}
      }]
    }

    out = stream_prism_to_polygon(
        polygon=boulder_poly, polygon_srs="EPSG:4326",
        variable="tmax", date="2025-07-15", resolution="800m", freq="daily",
        title="PRISM TMAX daily (°C×10) — Boulder polygon",
        return_array=True, compute_stats=True
    )
    print("Stats:", out["stats"])
```

## R
Paste into your R console:
```r
# R equivalent using terra
library(terra)
base <- "https://services.nacse.org/prism/data/get/us/800m/tmax/20250715"
vsi  <- paste0("/vsizip//vsicurl/", base, "/prism_tmax_us_30s_20250715.tif")
r <- rast(vsi) / 10
plot(r, main = "PRISM tmax — 2025-07-15")
```

## More information

### Source
- Provider: PRISM Climate Group, Oregon State University
- Access: https://services.nacse.org/prism/data (COG-in-ZIP web service)
- License: [PRISM Data Terms of Use](https://prism.oregonstate.edu/documents/PRISM_terms_of_use.pdf)

### Visualization
![PRISM TMAX daily (°C×10) — Front Range](../../assets/prism-static.png)
*Static example of PRISM TMAX daily data rendered as an image.*

### Harmonization notes
- Resolution options: 400 m, 800 m, or 4 km grids in geographic WGS84.
- Units: temperatures stored as °C ×10; precipitation in mm; vapor pressure deficit in hPa.
- Recent grids may be revised for a few months; check `releaseDate` or `gridCount` endpoints for freshness.
- Filenames follow `prism_<var>_<region>_<resolution>_<date>.tif` inside a ZIP delivered via the web service.

### References
- [PRISM Climate Group](https://prism.oregonstate.edu)
- [PRISM Web Service](https://services.nacse.org/prism/data)
- Daly, C., et al. 2008. Physiographically sensitive mapping of temperature and precipitation across the conterminous United States. *Journal of Applied Meteorology and Climatology*. https://doi.org/10.1175/2007JAMC1356.1
