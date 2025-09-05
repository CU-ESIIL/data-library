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

`streamable` `vegetation` `rangeland` `rap` `tiles` `teaching` `png` `quicklook` `innovation-summit-2025`

Ty Tuff, ESIIL 2025-09-05


## Why use this dataset

RAP provides annual fractional cover and biomass for U.S. rangelands, with public web map tiles that are easy to stream into quick previews and teaching demos. If you need a fast “peek” at vegetation functional groups (e.g., perennial forbs and grasses) without standing up Earth Engine or downloading full rasters, these PNG tiles work great for bounding-box mosaics and notebooks.

**Highlights**
- Coverage: CONUS, annual series (1984→present for cover; 1986→present for biomass v3).
- Variables (cover): annual forbs & grasses, perennial forbs & grasses, shrubs, trees, bare ground, litter.
- Stream-first: tiles are public on Google Cloud Storage; simple HTTP GET per {z}/{x}/{y} path.

*Learn more:* RAP products overview and version 3 notes (coverage, variables, updates) are at rangelands.app; API docs describe tile and time-series endpoints. :contentReference[oaicite:0]{index=0}

---

## How to use it (copy/paste)

> Assumes you’ll copy this function and tweak the arguments. It builds a small **mosaic** over a bounding box by fetching PNG tiles and stacking them. This is a lightweight preview tool — perfect for exploration and teaching.

```python
# Requires: pillow numpy requests matplotlib
# pip install pillow numpy requests
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
    """
    Build a quick-look mosaic from RAP cover v3 PNG tiles.

    Parameters
    ----------
    vegetation : str
        Functional group code (e.g., 'pfg' = perennial forbs & grasses).
        Other common codes include 'afg' (annual forbs & grasses), 'shrubs',
        'trees', 'bare', 'litter' — availability varies by product.
    year : int
        Year in the RAP time series (e.g., 1986..present for cover v3).
    masked : bool
        Use 'masked' tiles (non-rangeland/invalid masked to transparent) or
        'unmasked' (full prediction surface).
    bbox : tuple
        (W, S, E, N) in degrees for the area of interest.
    z : int
        Web mercator zoom level. RAP tiles are available up to around 12.

    Returns
    -------
    numpy.ndarray
        RGBA mosaic as a NumPy array.
    """
    W, S, E, N = bbox
    x_min, y_max = lonlat_to_tile(W, S, z)
    x_max, y_min = lonlat_to_tile(E, N, z)
    x_range = range(min(x_min, x_max), max(x_min, x_max) + 1)
    y_range = range(min(y_min, y_max), max(y_min, y_max) + 1)

    base = "masked" if masked else "unmasked"
    # Tileset choices:
    #   Cover v3:   usda-rap-tiles-cover-v3
    #   Biomass v3: usda-rap-tiles-biomass-v3
    tileset = "usda-rap-tiles-cover-v3"

    mosaic = None
    for y in y_range:
        row_imgs = []
        for x in x_range:
            url = f"https://storage.googleapis.com/{tileset}/{base}/{vegetation}/{year}/{z}/{x}/{y}.png"
            try:
                row_imgs.append(fetch_tile_png(url))
            except Exception:
                # Fill gaps with transparent tiles
                row_imgs.append(Image.new("RGBA", (256, 256), (0, 0, 0, 0)))
        row = np.hstack([np.array(im) for im in row_imgs])
        mosaic = row if mosaic is None else np.vstack([mosaic, row])
    return mosaic

# --- Example: PFG cover in 2011, masked, zoom 10 over Boulder, CO area
mosaic = rap_tile_mosaic(vegetation="pfg", year=2011, masked=True,
                         bbox=(-105.9, 40.1, -105.3, 40.6), z=10)
plt.figure(figsize=(6, 6))
plt.imshow(mosaic)
plt.axis("off"); plt.title("RAP tiles — PFG 2011 (masked)")
plt.show()
```

## What you get (content & format)

* **Products:** cover (fractional %) and biomass (lbs/acre) series; versioning and scope are documented in RAP 3.0 notes.  
  [rangelands.app](https://rangelands.app)
* **Tiles:** public PNGs arranged by `{zoom}/{x}/{y}` with folders by product/version, mask type, vegetation group, and year. See RAP API docs for map tiles and time-series endpoints.  
  [rangelands.app](https://rangelands.app)

---

## Notes & gotchas

* **Zoom limits:** RAP tiles are optimized for overview mapping (typically up to ~z12).
* **Masked vs unmasked:** "masked" hides non-rangeland classes and certain invalid regions for cleaner visualizations (transparent background).
* **Colors & legends:** PNG tiles are pre-colored; you’re mosaicking rendered tiles rather than raw values. For analysis on the numbers, use RAP rasters via Earth Engine or raster downloads noted in product docs.

---

## Learn more / docs

* RAP products & versions: [https://rangelands.app/products](https://rangelands.app/products) (RAP 3.0 overview).
* RAP home & app: [https://rangelands.app](https://rangelands.app).
* RAP API (tiles, time series): [https://rangelands.app/support/71-api-documentation](https://rangelands.app/support/71-api-documentation).
* Background & help articles: [Climate Engine RAP guide](https://support.climateengine.com/) (Climate Engine Support).

