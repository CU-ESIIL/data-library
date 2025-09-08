---
tags:
- hazards
- nclimgrid
- innovation-summit-2025
---

# NOAA NClimGrid Monthly

## Source
- Provider: NOAA National Centers for Environmental Information (NCEI)
- Access: [Planetary Computer STAC](https://planetarycomputer.microsoft.com/api/stac/v1) collection `noaa-nclimgrid-monthly`
- License: Public Domain (NOAA)

## Why it matters
NOAA's NClimGrid provides a gridded view of historical climate conditions across the contiguous United States. The dataset aggregates station observations into a ~4 km grid, offering monthly precipitation and temperature values that help researchers monitor climate trends, assess regional extremes, and support risk management decisions.

## Use cases
- Monitor drought and precipitation extremes across the United States.
- Evaluate regional temperature trends for climate change studies [Vose et al. 2014](https://doi.org/10.1175/JAMC-D-13-0248.1).

## Copy-and-paste example
```python
from pystac_client import Client
import planetary_computer as pc
from osgeo import gdal
import numpy as np
import matplotlib.pyplot as plt

PC_STAC = "https://planetarycomputer.microsoft.com/api/stac/v1"

def plot_pc_stac_cog(collection_id, time=None, bbox=None, title=None):
    client = Client.open(PC_STAC)
    search = client.search(collections=[collection_id], datetime=time, bbox=bbox, limit=1)
    item = pc.sign(next(search.items()))
    asset = next(a for a in item.assets.values() if a.media_type and "tiff" in a.media_type)
    gdal.SetConfigOption("GDAL_DISABLE_READDIR_ON_OPEN", "YES")
    gdal.SetConfigOption("CPL_VSIL_CURL_ALLOWED_EXTENSIONS", ".tif,.tiff")
    ds = gdal.Open(f"/vsicurl/{asset.href}")
    band = ds.GetRasterBand(1)
    arr = band.ReadAsArray().astype(float)
    ndv = band.GetNoDataValue()
    if ndv is not None:
        arr[arr == ndv] = np.nan
    gt = ds.GetGeoTransform()
    extent = (gt[0], gt[0] + gt[1]*ds.RasterXSize, gt[3] + gt[5]*ds.RasterYSize, gt[3])
    plt.imshow(arr, extent=extent, origin="upper")
    plt.xlabel("Longitude"); plt.ylabel("Latitude")
    plt.title(title or collection_id)
    plt.colorbar(label=asset.title or "value")
    plt.tight_layout(); plt.show()

plot_pc_stac_cog(
    collection_id="noaa-nclimgrid-monthly",
    time="2021-07",
    bbox=[-125, 24, -66, 50],
    title="NClimGrid Monthly — July 2021",
)
```
```r
library(rstac)
library(terra)

pc_stac <- "https://planetarycomputer.microsoft.com/api/stac/v1"

items <- stac(pc_stac) |>
  stac_search(collections = "noaa-nclimgrid-monthly",
              datetime = "2021-07",
              bbox = c(-125, 24, -66, 50)) |>
  get_request() |>
  items_fetch() |>
  items_sign()

asset <- items$features[[1]]$assets$prcp
r <- rast(paste0("/vsicurl/", asset$href))
plot(r, main = "NClimGrid Monthly — July 2021")
```

## Visualization
Run the example above to render a map of July 2021 conditions. (Preview image omitted.)

## Harmonization notes
- Spatial resolution: ~4 km (1/24°) grid in EPSG:4326.
- Variables are stored as GeoTIFFs with units of millimeters (precipitation) or degrees Celsius (temperature).
- Aligns well with other gridded climate products; reproject to a common CRS if combining with non-WGS84 data.

## References
- [NClimGrid on NOAA](https://www.ncei.noaa.gov/products/climate-data-records/temperature-precipitation)
- [Planetary Computer catalog entry](https://planetarycomputer.microsoft.com/dataset/noaa-nclimgrid)
