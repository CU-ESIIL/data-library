---
tags:
- forecasting
- prism
- innovation-summit-2025
---

PRISM (U.S. Gridded Climate)
================
Ty Tuff, ESIIL
2025-09-05

## Why use this dataset

PRISM is a widely used U.S. climate surface: terrain‑aware, quality‑controlled, and **long‑running** (monthly back to 1895, daily back to 1981). If you need consistent precipitation and temperature fields for modeling, mapping, or anomalies — and you want to **stream data instead of downloading** — PRISM’s newer COG‑in‑ZIP format and web service make it easy.

**Highlights**

* **Coverage & history:** CONUS monthly (1895→present), annual (1895→present), daily (1981→present).
* **Variables:** `ppt, tmin, tmax, tmean, tdmean, vpdmin, vpdmax` (plus radiation components in normals products).
* **Streamable:** each file is a **Cloud‑Optimized GeoTIFF** packaged in a **.zip** with predictable names; works cleanly with GDAL’s `/vsizip//vsicurl/`.
* **Freshness signals:** the web service exposes endpoints for `releaseDate` and `gridCount` so you can decide when to refresh.

---

## How to use it (copy/paste)

> Assumes you’ll **copy this function and tweak the arguments**. Inputs are annotated with valid values and typical ranges. The function streams a PRISM grid via GDAL (no local download) and plots a quick preview.

```python
# Requires: GDAL, numpy, matplotlib
# pip install numpy matplotlib
# (Install GDAL via your system/conda: conda install -c conda-forge gdal)

from osgeo import gdal
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
from typing import Union, Tuple

# --- Internal mappings for PRISM's new (COG-in-ZIP) file naming ---
_RES_WS = {"400m": "400m", "800m": "800m", "4km": "4km"}         # web-service resolution parameter
_RES_IN = {"400m": "15s",  "800m": "30s",  "4km": "25m"}         # filename tag inside the ZIP

def _parse_date(date: Union[str, dt.date, dt.datetime], freq: str) -> Tuple[str, str]:
    """
    Normalize dates for PRISM naming.
    Accepted formats per frequency:
      daily:    'YYYY-MM-DD' or 'YYYYMMDD'
      monthly:  'YYYY-MM'    or 'YYYYMM'
      annual:   'YYYY'
    Returns: (datecode, yyyy_str)
    """
    if isinstance(date, (dt.datetime, dt.date)):
        d = date if isinstance(date, dt.date) and not isinstance(date, dt.datetime) else date.date()
    elif isinstance(date, str):
        s = date.strip()
        if   freq == "daily":   d = (dt.datetime.strptime(s, "%Y-%m-%d") if "-" in s else dt.datetime.strptime(s, "%Y%m%d")).date()
        elif freq == "monthly": d = (dt.datetime.strptime(s, "%Y-%m")     if "-" in s else dt.datetime.strptime(s, "%Y%m")).date().replace(day=1)
        elif freq == "annual":  d =  dt.datetime.strptime(s, "%Y").date().replace(month=1, day=1)
        else: raise ValueError("freq must be 'daily','monthly','annual'")
    else:
        raise TypeError("date must be str, date, or datetime")

    if   freq == "daily":   return d.strftime("%Y%m%d"), d.strftime("%Y")
    elif freq == "monthly": return d.strftime("%Y%m"),   d.strftime("%Y")
    else:                    return d.strftime("%Y"),     d.strftime("%Y")


def build_prism_vsi(
    variable: str = "tmax",
    date: Union[str, dt.date, dt.datetime] = "2025-07-15",
    resolution: str = "800m",            # '400m' | '800m' | '4km'
    region: str = "us",                  # 'us' (CONUS). Other regions via service roadmap.
    freq: str = "daily",                 # 'daily' | 'monthly' | 'annual'
    dataset: str = "an"                  # 'an' (all networks). For monthly 800m, 'lt' also available.
) -> str:
    """
    Build a GDAL VSI path that streams a PRISM COG inside its remote ZIP via the PRISM web service.

    Inputs you’ll likely change:
      variable: one of {'ppt','tmin','tmax','tmean','tdmean','vpdmin','vpdmax'}
      date:     daily 1981-01-01 .. present | monthly 1895-01 .. present | annual 1895 .. present
      resolution: '400m','800m','4km'   (availability varies by product)
      freq:     'daily','monthly','annual'
      dataset:  'an' or (ONLY for monthly 800 m) 'lt'  # 'lt' = long-term emphasis
      region:   'us' for web service today (CONUS)

    Docs:
      Web service:    https://services.nacse.org/prism/data
      Formats/naming: https://prism.oregonstate.edu/documents/
    """
    if resolution not in _RES_WS:
        raise ValueError("resolution must be one of '400m','800m','4km'")
    if variable not in {"ppt","tmin","tmax","tmean","tdmean","vpdmin","vpdmax"}:
        raise ValueError("unknown PRISM variable")

    datecode, yyyy = _parse_date(date, freq)
    res_ws = _RES_WS[resolution]
    res_in = _RES_IN[resolution]

    tail = ""
    if dataset.lower() == "lt":
        if not (freq == "monthly" and resolution == "800m"):
            raise ValueError("dataset='lt' is only available for monthly 800 m series")
            
        tail = "/lt"

    # Returns a .zip “grid package” with a COG inside
    # Pattern: https://services.nacse.org/prism/data/get/<region>/<res>/<element>/<date>[ /lt ]
    base = f"https://services.nacse.org/prism/data/get/{region}/{res_ws}/{variable}/{datecode}{tail}"

    # Inside ZIP: prism_<var>_<region>_<res_in>_<date>.tif
    inner_tif = f"prism_{variable}_{region}_{res_in}_{datecode}.tif"

    # Let GDAL read the inner TIFF directly over HTTP via nested VSIs
    return f"/vsizip//vsicurl/{base}/{inner_tif}"


def open_prism_gdal(**kwargs) -> gdal.Dataset:
    """Open the PRISM raster read-only over HTTP. Returns gdal.Dataset or raises on failure."""
    vsi = build_prism_vsi(**kwargs)
    # Stream-friendly GDAL settings
    gdal.SetConfigOption("GDAL_DISABLE_READDIR_ON_OPEN", "YES")
    gdal.SetConfigOption("CPL_VSIL_CURL_ALLOWED_EXTENSIONS", ".zip,.tif,.tiff,.xml,.stx,.prj,.aux.xml")
    ds = gdal.Open(vsi, gdal.GA_ReadOnly)
    if ds is None:
        raise RuntimeError(f"GDAL failed to open:\n{vsi}")
    return ds


def _extent(ds):
    gt = ds.GetGeoTransform()
    w, h = ds.RasterXSize, ds.RasterYSize
    xmin, ymax = gt[0], gt[3]
    xmax, ymin = xmin + w*gt[1], ymax + h*gt[5]
    return (xmin, xmax, ymin, ymax)


def plot_prism(
    variable="tmax",
    date="2025-07-15",          # daily: 'YYYY-MM-DD' or 'YYYYMMDD'; monthly: 'YYYY-MM' or 'YYYYMM'; annual: 'YYYY'
    resolution="800m",
    freq="daily",
    dataset="an",               # 'an' or (if monthly & 800m) 'lt'
    region="us",
    scale_temp_by_10=True,      # PRISM temps are °C*10 → divide by 10 for °C
    vmin=None, vmax=None,
    title=None
):
    """Stream a PRISM grid and plot it (simple preview)."""
    ds = open_prism_gdal(variable=variable, date=date, resolution=resolution,
                         region=region, freq=freq, dataset=dataset)
    band = ds.GetRasterBand(1)
    arr = band.ReadAsArray()
    ndv = band.GetNoDataValue()
    if ndv is not None:
        arr = np.where(arr == ndv, np.nan, arr)
    if scale_temp_by_10 and variable in {"tmin","tmax","tmean"}:
        arr = arr / 10.0
    extent = _extent(ds)
    plt.figure(figsize=(8,6))
    im = plt.imshow(arr, extent=extent, origin="upper", vmin=vmin, vmax=vmax)
    plt.xlabel("Longitude"); plt.ylabel("Latitude")
    plt.title(title or f"PRISM {variable} — {date} ({resolution}, {freq})")
    cb = plt.colorbar(im, shrink=0.85)
    cb.set_label(f"{variable} ({'°C' if variable in {'tmin','tmax','tmean'} else 'native units'})")
    plt.tight_layout(); plt.show()
```

### Example calls (edit these)

```python
# Daily 800 m maximum temperature for a summer day
plot_prism(variable="tmax", date="2025-07-15", resolution="800m", freq="daily",
           title="PRISM tmax — 2025-07-15 (800 m)")

# Monthly 4 km precipitation for March 2024
plot_prism(variable="ppt", date="2024-03", resolution="4km", freq="monthly",
           title="PRISM ppt — 2024-03 (4 km)")

# Monthly 800 m LT (long-term) series — only for monthly 800 m
plot_prism(variable="tmax", date="2005-06", resolution="800m", freq="monthly", dataset="lt",
           title="PRISM tmax — 2005-06 (800 m, LT)")
```

---

## What you get (content & format)

* **Variables:** precipitation, min/mean/max temperature, mean dew point, min/max VPD. (Radiation components available in *normals* products.)
* **Files:** each web‑service request returns a **`.zip`** “grid package” containing a **COG** (GeoTIFF) plus metadata (`.xml`, `.prj`), station list, and stats. Filenames follow `prism_<var>_<region>_<res>_<date>.*` (e.g., `prism_ppt_us_25m_20250312.zip`).

---

## Freshness & stability (optional, but useful)

PRISM revises recent grids for a few months. Use these endpoints to check freshness in code:

* **Release date** (JSON):

  * `https://services.nacse.org/prism/data/get/releaseDate/<region>/<res>/<element>/<date>?json=true`
* **Grid count** (how many revisions exist for a month):

  * `https://services.nacse.org/prism/data/get/gridCount/<region>/<element>/<YYYYMM>`

---

## Notes & gotchas

* **Units:** temperature variables are **°C × 10** (divide by 10 for °C); precipitation is mm over the period; VPD in hPa (check metadata).
* **Availability:** monthly/annual extend to **1895**, daily to **1981**; specifics vary by variable/resolution.
* **Format transition:** prefer the **COG‑in‑ZIP** format going forward; older BIL bundles are being deprecated.
* **Regions:** the web service focuses on CONUS; see PRISM updates for AK/HI/PR status.

---

## Learn more / docs

* PRISM homepage & downloads hub: [https://prism.oregonstate.edu](https://prism.oregonstate.edu)
* Web service guide & endpoints: [https://services.nacse.org/prism/data](https://services.nacse.org/prism/data)
* File formats & naming (COG‑in‑ZIP): [https://prism.oregonstate.edu/documents/](https://prism.oregonstate.edu/documents/)
* Dataset & variables overview: [https://prism.oregonstate.edu/documents/](https://prism.oregonstate.edu/documents/)

---

### Why this page is “stream‑first”

We assume most users will **copy/paste** the function above and just change `variable`, `date`, `resolution`, and `freq`. The function returns a real GDAL dataset, so you can window‑read arrays, build VRTs for **time stacks**, or pass it into raster ops — all **without local downloads**. If you’d like a follow‑up snippet that crops to a bounding box (in‑memory `WarpedVRT`) or stacks a date range into a VRT for animation, we can add that here.
