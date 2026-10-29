-------------------

ABSTRACT

-------------------

This is event-level polygons for the fire event delineation (FIRED) product for REF\INDIVIDUAL COUNTRIES\CONUS AK from November 2000  to January 2022. It is derived from the MODIS MCD64A1 burned area product (see https://lpdaac.usgs.gov/products/mcd64a1v006/ for more details). The MCD64A1 is a monthly raster grid of estimated burned dates. Firedpy (www.github.com/earthlab/firedpy) is an algorithm that converts these rasters into events by stacking the entire time series into a spatial-temporal data cube, then uses an algorithm to assign event identification numbers to pixels that fit into the same 3-dimensional spatial temporal window. This particular dataset was created using a spatial parameter of 5 pixels and 11 days. If daily polygons are included, the event identification numbers are the same for both files, but the event-level product has only single polygons for each entire event, while the daily product has separate polygons for each date per event. See the associated paper for more details on the methods and more:

Balch, J.K.; St. Denis, L.A.; Mahood, A.L.; Mietkiewicz, N.P.; Williams, T.M.; McGlinchy, J.; Cook, M.C. FIRED (Fire Events Delineation): An Open, Flexible Algorithm and Database of US Fire Events Derived from the MODIS Burned Area Product (2001–2019). Remote Sens. 2020, 12, 3498. https://doi.org/10.3390/rs12213498 

-------------------

GENERAL INFORMATION

-------------------



1. Title of Dataset:  FIRED  REF\INDIVIDUAL COUNTRIES\CONUS AK 



2. Authors: Jennifer K. Balch, Lise A. St. Denis, Adam L. Mahood, Nathan P.  Mietkiewicz, Travis Williams, Joe McGlinchy, Maxwell C. Cook, Estelle J. Lindrooth.



3. Contact information: jennifer.balch@colorado.edu; adam.mahood@colorado.edu



4. Date of data collection:November 2000 - January 2022



--------------------------

SHARING/ACCESS INFORMATION

--------------------------



1. Licenses/restrictions placed on the data: MIT



2. Links to publications that cite or use the data: TBD



3. Links to other publicly accessible locations of the data: None



4. Recommended citation for the data: 


Balch, J.K.; St. Denis, L.A.; Mahood, A.L.; Mietkiewicz, N.P.; Williams, T.M.; McGlinchy, J.; Cook, M.C. FIRED (Fire Events Delineation): An Open, Flexible Algorithm and Database of US Fire Events Derived from the MODIS Burned Area Product (2001–2019). Remote Sens. 2020, 12, 3498. https://doi.org/10.3390/rs12213498
 
-------------------

DATA & FILE OVERVIEW

-------------------

1. File List: 

     1. Table:
 
         A. conus_ak_to2022001_events.csv

     2. Shapefile: 

         A. conus_ak_to2022001_events.shp

         B. conus_ak_to2022001_events.gpkg

-------------------

METHODOLOGICAL INFORMATION

-------------------

 1. Spatial window: 5 

 2. Temporal window: 11 

See Balch et al 2020 for complete methods. DOI: https://doi.org/10.3390/rs12213498

-------------------

DATA-SPECIFIC INFORMATION FOR: conus_ak_to2022001_events.csv, conus_ak_to2022001_events.gpkg, conus_ak_to2022001_events.shp
-------------------

