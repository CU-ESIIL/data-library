---
tags:
- streamable
- vegetation
- rangeland
- rap
- tiles
- teaching
- png
- quicklook
- innovation-summit-2025
---

# RAP Tiles (Rangeland Analysis Platform)

## Source
- Provider: Rangeland Analysis Platform
- Access: Public Google Cloud Storage tiles at `https://storage.googleapis.com/usda-rap-tiles-cover-v3`
- License: Creative Commons Attribution 4.0

## Why it matters
RAP provides annual fractional cover and biomass for U.S. rangelands. Its PNG map tiles stream quickly for previews and teaching demos, allowing fast looks at vegetation functional groups without downloading large rasters or using Earth Engine.

**Highlights**
- Coverage: CONUS, annual series (1984→present for cover; 1986→present for biomass v3).
- Variables (cover): annual forbs & grasses, perennial forbs & grasses, shrubs, trees, bare ground, litter.
- Stream-first: tiles available via simple HTTP `/{z}/{x}/{y}` paths.

## Example usage
```python
# Requires: pillow numpy requests matplotlib
import math, io, requests, numpy as np
from PIL import Image
import matplotlib.pyplot as plt

def lonlat_to_tile(lon, lat, z):
    lat_rad = math.radians(lat)
    n = 2.0 ** z
    x = int((lon + 180.0) / 360.0 * n)
    y = int((1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n)
    return x, y

def fetch_tile_png(url):
    r = requests.get(url, timeout=60); r.raise_for_status()
    return Image.open(io.BytesIO(r.content)).convert("RGBA")

def rap_tile_mosaic(vegetation="pfg", year=2011, masked=True,
                    bbox=(-105.9, 40.1, -105.3, 40.6), z=10):
    """Build a quick-look mosaic from RAP cover v3 PNG tiles."""
    W, S, E, N = bbox
    x_min, y_max = lonlat_to_tile(W, S, z)
    x_max, y_min = lonlat_to_tile(E, N, z)
    x_range = range(min(x_min, x_max), max(x_min, x_max) + 1)
    y_range = range(min(y_min, y_max), max(y_min, y_max) + 1)
    base = "masked" if masked else "unmasked"
    tileset = "usda-rap-tiles-cover-v3"
    mosaic = None
    for y in y_range:
        row_imgs = []
        for x in x_range:
            url = f"https://storage.googleapis.com/{tileset}/{base}/{vegetation}/{year}/{z}/{x}/{y}.png"
            try:
                row_imgs.append(fetch_tile_png(url))
            except Exception:
                row_imgs.append(Image.new("RGBA", (256, 256), (0, 0, 0, 0)))
        row = np.hstack([np.array(im) for im in row_imgs])
        mosaic = row if mosaic is None else np.vstack([mosaic, row])
    return mosaic

mosaic = rap_tile_mosaic()
```
```r
# R equivalent using png and httr
library(png)
library(httr)

rap_tile <- function(vegetation="pfg", year=2011, z=10,
                     masked=TRUE, x=482, y=986) {
  base <- if (masked) "masked" else "unmasked"
  tileset <- "usda-rap-tiles-cover-v3"
  url <- sprintf("https://storage.googleapis.com/%s/%s/%s/%d/%d/%d.png",
                 tileset, base, vegetation, year, z, x, y)
  img <- readPNG(GET(url)$content)
  grid::grid.raster(img)
}
rap_tile()
```

## Visualization
```python
plt.figure(figsize=(6, 6))
plt.imshow(mosaic)
plt.axis("off")
plt.title("RAP tiles — PFG 2011 (masked)")
plt.show()
```

## Harmonization notes
- Tiles are in Web Mercator (EPSG:3857); reproject if combining with other CRS.
- Zoom levels optimized for overview mapping (≈z12 max).
- "Masked" tiles hide non-rangeland classes for cleaner visuals.
- Tiles are pre-colored PNGs; for raw values use RAP rasters or Earth Engine assets.

## References
- [Rangeland Analysis Platform](https://rangelands.app)
- [RAP API documentation](https://rangelands.app/support/71-api-documentation)
- [RAP product overview](https://rangelands.app/products)
