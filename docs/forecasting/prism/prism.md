---
tags:
- forecasting
- prism
- innovation-summit-2025
---

# PRISM (U.S. Gridded Climate)

## Source
- Provider: PRISM Climate Group, Oregon State University
- Access: https://services.nacse.org/prism/data (COG-in-ZIP web service)
- License: [PRISM Data Terms of Use](https://prism.oregonstate.edu/documents/PRISM_terms_of_use.pdf)

## Why it matters
PRISM offers terrain-aware, quality-controlled climate normals and grids for the conterminous United States. Monthly data extend back to 1895 and daily to 1981, supplying consistent temperature and precipitation fields for modeling, drought monitoring, and ecological studies [Daly et al., 2008](https://doi.org/10.1175/2007JAMC1356.1). The service delivers Cloud-Optimized GeoTIFFs inside ZIP files so you can stream them directly with GDAL.

## Example usage
```python
# Stream a daily maximum temperature grid and plot it
from osgeo import gdal
import matplotlib.pyplot as plt

base = "https://services.nacse.org/prism/data/get/us/800m/tmax/20250715"
vsi = f"/vsizip//vsicurl/{base}/prism_tmax_us_30s_20250715.tif"
ds = gdal.Open(vsi)
arr = ds.ReadAsArray() / 10.0  # °C×10 → °C
plt.imshow(arr)
plt.title("PRISM tmax — 2025-07-15")
plt.show()
```
```r
# R equivalent using terra
library(terra)
base <- "https://services.nacse.org/prism/data/get/us/800m/tmax/20250715"
vsi  <- paste0("/vsizip//vsicurl/", base, "/prism_tmax_us_30s_20250715.tif")
r <- rast(vsi) / 10
plot(r, main = "PRISM tmax — 2025-07-15")
```

## Visualization
![PRISM TMAX daily (°C×10) — Front Range](../../assets/prism-static.png)
*Static example of PRISM TMAX daily data rendered as an image.*

## Harmonization notes
- Resolution options: 400 m, 800 m, or 4 km grids in geographic WGS84.
- Units: temperatures stored as °C ×10; precipitation in mm; vapor pressure deficit in hPa.
- Recent grids may be revised for a few months; check `releaseDate` or `gridCount` endpoints for freshness.
- Filenames follow `prism_<var>_<region>_<resolution>_<date>.tif` inside a ZIP delivered via the web service.

## References
- [PRISM Climate Group](https://prism.oregonstate.edu)
- [PRISM Web Service](https://services.nacse.org/prism/data)
- Daly, C., et al. 2008. Physiographically sensitive mapping of temperature and precipitation across the conterminous United States. *Journal of Applied Meteorology and Climatology*. https://doi.org/10.1175/2007JAMC1356.1
