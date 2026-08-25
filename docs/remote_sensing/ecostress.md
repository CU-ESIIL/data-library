
This unified dataset was combines Ecostress Water Use Efficiency (WUE), SRTM, NLCD (2019), slope, aspect, and GEDI level 2B cover, pavd, and fhd data at a 5m resolution.
Another repo explaines in detials about building a dataset, training and evlauating machine learning models on the data, and running diagnostics. 
Please refer to https://github.com/j-gams/neon_data_project.

Dataset info:
  -  File type	Cloud-Optimized GeoTIFF (.tif)
  -  Temporal coverage	2018 to 2022
  -  Dataset structure:
        Western-conus: aspect / slope / elevation / WUE (2018-2022)
        Colorado Sate: WUE (2018-2022) / Evaporative Stress Index (ESI, 2018-2022)
  - Access: free. Whole dataset has no key required via cyverse esiil-data-oasis
    

Access pattern:
The files live in the CyVerse Data Store, in the ESIIL community folder (the ESIIL Data Oasis), and are shared read-only with the anonymous user. 
That makes them readable over plain HTTPS through CyVerse's anonymous WebDAV endpoint:
https://data.cyverse.org/dav-anon/iplant/projects/esiil/Ecostress/colorado/colorado_esi_2018_output_cog.tif
text
iRODS path:  /iplant/home/shared/esiil/Ecostress/
HTTPS base:  https://data.cyverse.org/dav-anon/iplant/projects/esiil/Ecostress

Because the rasters are Cloud-Optimized GeoTIFFs served over HTTPS, GDAL's /vsicurl/ driver can read a bounding-box subset without downloading the whole file. Browse the folder in the CyVerse Data Commons.

Access constraints
No key, no account, no authentication required. The folder is shared read-only with the CyVerse anonymous user, so any HTTPS client can read it. There is no rate-limit guarantee — if a request returns a redirect to unblockme.cyverse.org, your IP has been throttled or blocked; wait and retry or use the unblock page.




Python example
python
# pip install rioxarray matplotlib
import matplotlib.pyplot as plt
import rioxarray

ECOSTRESS_URL = (
    "https://data.cyverse.org/dav-anon/iplant/home/shared/esiil/"
    "Ecostress/colorado/colorado_wue_2018_output_cog.tif"
)


def get_ecostress_wue(url=ECOSTRESS_URL, aoi=(-105.5, 40.0, -105.2, 40.3)):
    """Stream an ECOSTRESS WUE subset, make a minimum viable plot, return it.

    aoi is (xmin, ymin, xmax, ymax) in the raster's CRS.
    """
    # Open lazily over HTTPS; only the requested window is transferred.
    da = rioxarray.open_rasterio(url, masked=True, chunks=True).squeeze()

    xmin, ymin, xmax, ymax = aoi
    sub = da.rio.clip_box(minx=xmin, miny=ymin, maxx=xmax, maxy=ymax)

    if sub.size == 0:
        raise ValueError(f"Empty subset - check that {aoi} overlaps the raster extent.")

    # Minimum viable plot.
    sub.plot(robust=True)
    plt.title("ECOSTRESS water use efficiency")
    plt.tight_layout()
    plt.show()

    return sub
#test and print the results
 wue = get_ecostress_wue()
 print(float(wue.mean()))


Derived layers: GEDI-ECOSTRESS data project, Earth Lab / ESIIL, University of Colorado Boulder. https://github.com/earthlab/GEDI-ECOSTRESS_data_project
Hosting: ESIIL community folder, CyVerse Data Store, /iplant/home/shared/esiil/ECOSTRESS/.
