---
title: ECOSTRESS Water Use Efficiency
description: Public ECOSTRESS-derived water use efficiency Cloud-Optimized GeoTIFFs with no-key R and Python examples for streaming a small raster subset.
tags:
  - ECOSTRESS
  - evapotranspiration
  - ET
  - water use efficiency
  - WUE
  - evaporative stress
  - ESI
  - remote sensing
  - raster
  - Cloud-Optimized GeoTIFF
  - COG
  - Colorado
  - western United States
  - annual
  - no key required
  - public access
  - cloud native
  - streaming
  - subset by bounding box
  - R example
  - Python example
  - minimum viable plot
access: no-key
languages:
  - R
  - Python
data_types:
  - raster
spatial_extent:
  - Colorado
  - western United States
temporal_resolution:
  - annual
---

# ECOSTRESS Water Use Efficiency

## Why this dataset is useful

This dataset combines ECOSTRESS-derived water use efficiency (WUE) and evaporative stress information with terrain, land cover, and GEDI vegetation-structure layers. It can help users explore how vegetation water use and stress vary across landscapes, especially when paired with elevation, slope, aspect, NLCD land cover, and GEDI canopy metrics.

The related GEDI-ECOSTRESS data project explains the broader workflow for building the dataset and using it in machine-learning experiments.

## What it contains

| Field | Description |
| --- | --- |
| File type | Cloud-Optimized GeoTIFF (`.tif`) |
| Temporal coverage | 2018 to 2022 |
| Colorado layers | WUE and Evaporative Stress Index (ESI), 2018 to 2022 |
| Western CONUS layers | Aspect, slope, elevation, and WUE, 2018 to 2022 |
| Example variable | ECOSTRESS water use efficiency for Colorado in 2018 |
| Example access URL | `https://data.cyverse.org/dav-anon/iplant/home/shared/esiil/Ecostress/colorado/colorado_wue_2018_output_cog.tif` |

## Access pattern

The files live in the CyVerse Data Store in the ESIIL community folder and are shared read-only with anonymous users. They can be accessed over HTTPS through CyVerse's anonymous WebDAV endpoint.

Because the rasters are Cloud-Optimized GeoTIFFs served over HTTPS, GDAL-compatible tools can stream metadata and read a bounding-box subset without downloading the full file.

```text
iRODS path: /iplant/home/shared/esiil/Ecostress/
HTTPS base: https://data.cyverse.org/dav-anon/iplant/home/shared/esiil/Ecostress/
```

## Access constraints

No key, account, password, token, or authentication is required. The folder is shared read-only with the CyVerse anonymous user.

CyVerse may throttle or temporarily block repeated heavy requests. If a request redirects to an unblock page, wait and retry later or use the CyVerse guidance on the unblock page.

## R example

```r
# install.packages(c("terra", "httr"))
library(terra)

ECOSTRESS_URL <- paste0(
  "https://data.cyverse.org/dav-anon/iplant/home/shared/esiil/",
  "Ecostress/colorado/colorado_wue_2018_output_cog.tif"
)

get_ecostress_wue <- function(url = ECOSTRESS_URL,
                              aoi = c(-105.5, -105.2, 40.0, 40.3)) {
  # aoi = c(xmin, xmax, ymin, ymax) in the raster's CRS.
  # /vsicurl/ lets terra stream bytes from the COG instead of downloading it.
  r <- terra::rast(paste0("/vsicurl/", url))

  if (terra::ncell(r) == 0) {
    stop("Raster could not be read from: ", url)
  }

  # Subset before pulling pixels into memory.
  sub <- terra::crop(r, terra::ext(aoi))

  if (terra::ncell(sub) == 0) {
    stop("Empty subset. Check that the AOI overlaps the raster extent.")
  }

  terra::plot(sub, main = "ECOSTRESS water use efficiency")

  sub
}

# Example call:
# wue <- get_ecostress_wue()
# summary(terra::values(wue))
# print(global(wue, "mean", na.rm = TRUE))
```

## Python example

```python
# pip install rioxarray matplotlib
import matplotlib.pyplot as plt
import rioxarray

ECOSTRESS_URL = (
    "https://data.cyverse.org/dav-anon/iplant/home/shared/esiil/"
    "Ecostress/colorado/colorado_wue_2018_output_cog.tif"
)


def get_ecostress_wue(url=ECOSTRESS_URL, aoi=(-105.5, 40.0, -105.2, 40.3)):
    """Stream an ECOSTRESS WUE subset, make a minimum viable plot, and return it.

    aoi is (xmin, ymin, xmax, ymax) in the raster's CRS.
    """
    # Open lazily over HTTPS; only the requested window is transferred.
    data_array = rioxarray.open_rasterio(url, masked=True, chunks=True).squeeze()

    xmin, ymin, xmax, ymax = aoi
    subset = data_array.rio.clip_box(minx=xmin, miny=ymin, maxx=xmax, maxy=ymax)

    if subset.size == 0:
        raise ValueError(f"Empty subset. Check that {aoi} overlaps the raster extent.")

    subset.plot(robust=True)
    plt.title("ECOSTRESS water use efficiency")
    plt.tight_layout()
    plt.show()

    return subset


# Example call:
# wue = get_ecostress_wue()
# print(float(wue.mean()))
```

## Minimum viable plot

Both examples stream a small Colorado bounding-box subset and plot ECOSTRESS water use efficiency values. The plot confirms that the remote COG can be reached, subsetted, and visualized without downloading the full raster.

## Suggested uses

- Compare water use efficiency across elevation or land-cover gradients.
- Explore where vegetation appears water-stressed during a selected year.
- Teach cloud-native raster access with a public COG.
- Prototype inputs for models that combine ECOSTRESS, GEDI, terrain, and land-cover predictors.

## Limitations and cautions

- The examples use one Colorado WUE COG for a small subset, not the full multi-year collection.
- Values and units should be checked against the source workflow before formal analysis.
- CyVerse anonymous HTTPS access can be throttled for heavy or repeated requests.
- The dataset is externally hosted by CyVerse; this repository only documents access code.

## Tags

ECOSTRESS, evapotranspiration, ET, water use efficiency, WUE, evaporative stress, ESI, remote sensing, raster, Cloud-Optimized GeoTIFF, COG, Colorado, western United States, annual, no key required, public access, cloud native, streaming, subset by bounding box, R example, Python example, minimum viable plot.

## Citation

Derived layers: GEDI-ECOSTRESS data project, Earth Lab / ESIIL, University of Colorado Boulder. See the [GEDI-ECOSTRESS data project](https://github.com/earthlab/GEDI-ECOSTRESS_data_project).

Hosting: ESIIL community folder, CyVerse Data Store, `/iplant/home/shared/esiil/Ecostress/`.
