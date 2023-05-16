# FIRED

This data set contains event- and daily-level polygons for the [Fire Event Delineation](https://scholar.colorado.edu/concern/datasets/d504rm74m) (FIRED) product for the conterminous US from November 2001 to January 2022. You can find more information [here](https://www.mdpi.com/2072-4292/12/21/3498).

In R, we need 3 packages to download and visualize the data. First, check if the packages are already installed. Install them if they are not:

``` r
packages <- c("tidyverse", "httr", "sf") 
new.packages <- packages[!(packages %in% installed.packages()[,"Package"])] 
if(length(new.packages)>0) install.packages(new.packages) 
```

Then, load them:

``` r
lapply(packages, library, character.only = TRUE)
```

```         
── Attaching packages ─────────────────────────────────────── tidyverse 1.3.0 ──

✔ ggplot2 3.4.1     ✔ purrr   0.3.4
✔ tibble  3.2.1     ✔ dplyr   1.0.9
✔ tidyr   1.1.2     ✔ stringr 1.4.0
✔ readr   1.4.0     ✔ forcats 0.5.0

── Conflicts ────────────────────────────────────────── tidyverse_conflicts() ──
✖ dplyr::filter() masks stats::filter()
✖ dplyr::lag()    masks stats::lag()

Warning: package 'sf' was built under R version 4.0.5

Linking to GEOS 3.9.1, GDAL 3.4.0, PROJ 8.1.1; sf_use_s2() is TRUE

[[1]]
 [1] "forcats"   "stringr"   "dplyr"     "purrr"     "readr"     "tidyr"    
 [7] "tibble"    "ggplot2"   "tidyverse" "stats"     "graphics"  "grDevices"
[13] "utils"     "datasets"  "methods"   "base"     

[[2]]
 [1] "httr"      "forcats"   "stringr"   "dplyr"     "purrr"     "readr"    
 [7] "tidyr"     "tibble"    "ggplot2"   "tidyverse" "stats"     "graphics" 
[13] "grDevices" "utils"     "datasets"  "methods"   "base"     

[[3]]
 [1] "sf"        "httr"      "forcats"   "stringr"   "dplyr"     "purrr"    
 [7] "readr"     "tidyr"     "tibble"    "ggplot2"   "tidyverse" "stats"    
[13] "graphics"  "grDevices" "utils"     "datasets"  "methods"   "base"     
```

Download the data set:

``` r
url <- "https://scholar.colorado.edu/downloads/zw12z650d" 
fired <- GET(url) 
data_file <-"fired.zip" 
writeBin(content(fired, "raw"), data_file)

# Unzip the file
unzip(data_file)
```

Read the data set:

``` r
fired <- st_read("fired_conus_ak_to_January_2022_gpkg_shp/conus_ak_to2022001_events.shp") 
```

```         
Reading layer `conus_ak_to2022001_events' from data source 
  `/Users/viig7608/Desktop/data library/FIRED/fired_conus_ak_to_January_2022_gpkg_shp/conus_ak_to2022001_events.shp' 
  using driver `ESRI Shapefile'
Simple feature collection with 109999 features and 23 fields
Geometry type: MULTIPOLYGON
Dimension:     XY
Bounding box:  xmin: -11045380 ymin: 2797944 xmax: -5137210 ymax: 7783655
CRS:           unknown
```

Plot fire duration as a function of ignition day:

``` r
ggplot(fired) +
  geom_point(aes(ig_day, event_dur)) +
  theme_bw() +
  xlab('Day') +
  ylab('Event duration (days)')
```

![](FIRED_files/figure-commonmark/unnamed-chunk-5-1.png)

In Python, we need 5 libraries to download and visualize the data.

``` python
import requests 
import zipfile 
import geopandas as gpd 
import matplotlib.pyplot as plt
import seaborn as sns
```

Download the data set:

``` python
url = "https://scholar.colorado.edu/downloads/zw12z650d"
fired = requests.get(url)
data_file = "fired.zip"
with open(data_file, 'wb') as f:
    f.write(fired.content)

# Unzip the file
```

```         
64677742
```

``` python
with zipfile.ZipFile(data_file, 'r') as zip_ref:
    zip_ref.extractall()
```

Read it:

``` python
fired = gpd.read_file("fired_conus_ak_to_January_2022_gpkg_shp/conus_ak_to2022001_events.shp")
```

Plot fire duration as a function of ignition day:

``` python
plt.figure()
sns.scatterplot(data=fired, x='ig_day', y='event_dur')
sns.set_style('whitegrid')
plt.xlabel('Day')
plt.ylabel('Event duration (days)')
plt.show()
```

![](FIRED_files/figure-commonmark/unnamed-chunk-9-1.png)
