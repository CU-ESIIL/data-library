AIANNH
================

# American Indian and Alaska Native Areas (AIANNH)

In this example, we’ll download and analyze the American Indian and
Alaska Native Areas (AIANNH) TIGER/Line Shapefile from the U.S. Census
Bureau. We’ll download the data for the year 2020, and analyze the
number of AIANNH per congressional district

R: In R, we’ll use the ‘sf’ and ‘dplyr’ packages to read and process the
Shapefile data.

R code:

``` r
# Install and load necessary libraries
library(sf)
```

    Linking to GEOS 3.10.2, GDAL 3.4.2, PROJ 8.2.1; sf_use_s2() is TRUE

``` r
library(dplyr)
```


    Attaching package: 'dplyr'

    The following objects are masked from 'package:stats':

        filter, lag

    The following objects are masked from 'package:base':

        intersect, setdiff, setequal, union

``` r
library(knitr)

# Download historic redlining data for Philadelphia
url <- "https://www2.census.gov/geo/tiger/TIGER2020/AIANNH/tl_2020_us_aiannh.zip"
temp_file <- tempfile(fileext = ".zip")
download.file(url, temp_file, mode = "wb")
unzip(temp_file, exdir = tempdir())

# Read the Shapefile
shapefile_path <- file.path(tempdir(), "tl_2020_us_aiannh.shp")
aiannh <- read_sf(shapefile_path)

# Count the number of AIANNH per congressional district
state_counts <- aiannh %>%
  group_by(LSAD) %>%
  summarize(count = n())

kable(state_counts[order(-state_counts$count),])
```

| LSAD | count | geometry                     |
|:-----|------:|:-----------------------------|
| 79   |   221 | MULTIPOLYGON (((-166.5331 6… |
| 86   |   206 | MULTIPOLYGON (((-83.38811 3… |
| OT   |   155 | MULTIPOLYGON (((-92.32972 4… |
| 78   |    75 | MULTIPOLYGON (((-155.729 20… |
| 85   |    46 | MULTIPOLYGON (((-122.3355 3… |
| 92   |    35 | MULTIPOLYGON (((-93.01356 3… |
| 88   |    25 | MULTIPOLYGON (((-97.35299 3… |
| 96   |    19 | MULTIPOLYGON (((-116.48 32…. |
| 84   |    16 | MULTIPOLYGON (((-105.5937 3… |
| 89   |    11 | MULTIPOLYGON (((-95.91705 4… |
| 82   |     8 | MULTIPOLYGON (((-123.5766 4… |
| 80   |     7 | MULTIPOLYGON (((-77.21183 3… |
| 81   |     6 | MULTIPOLYGON (((-119.1725 3… |
| 97   |     5 | MULTIPOLYGON (((-122.5227 3… |
| 98   |     5 | MULTIPOLYGON (((-119.7176 3… |
| 90   |     4 | MULTIPOLYGON (((-94.96309 3… |
| 83   |     3 | MULTIPOLYGON (((-106.4006 3… |
| 95   |     3 | MULTIPOLYGON (((-87.33648 4… |
| 94   |     2 | MULTIPOLYGON (((-116.7145 3… |
| 00   |     1 | POLYGON ((-106.1191 36.0735… |
| 87   |     1 | POLYGON ((-131.7133 55.099,… |
| 91   |     1 | POLYGON ((-119.2362 39.0904… |
| 93   |     1 | POLYGON ((-116.8737 32.7020… |
| 99   |     1 | POLYGON ((-106.4424 35.6096… |
| 9C   |     1 | POLYGON ((-106.0627 35.8852… |
| 9D   |     1 | MULTIPOLYGON (((-92.61927 4… |

Python: In Python, we’ll use the ‘geopandas’ library to read and process
the Shapefile data.

Python code:

``` python
import geopandas as gpd
import pandas as pd
import requests
import zipfile
import os
from io import BytesIO

# Download historic redlining data for Philadelphia
url = "https://www2.census.gov/geo/tiger/TIGER2020/AIANNH/tl_2020_us_aiannh.zip"
response = requests.get(url)
zip_file = zipfile.ZipFile(BytesIO(response.content))

# Extract Shapefile
temp_dir = "temp"
if not os.path.exists(temp_dir):
    os.makedirs(temp_dir)

zip_file.extractall(path=temp_dir)
shapefile_path = os.path.join(temp_dir, "tl_2020_us_aiannh.shp")

# Read the Shapefile
aiannh = gpd.read_file(shapefile_path)

# Count the number of AIANNH per congressional district
state_counts = aiannh.groupby("LSAD").size().reset_index(name="count")

# Sort by descending count
state_counts_sorted = state_counts.sort_values(by="count", ascending=False)

print(state_counts_sorted)
```

       LSAD  count
    2    79    221
    9    86    206
    25   OT    155
    1    78     75
    8    85     46
    15   92     35
    11   88     25
    19   96     19
    7    84     16
    12   89     11
    5    82      8
    3    80      7
    4    81      6
    21   98      5
    20   97      5
    13   90      4
    18   95      3
    6    83      3
    17   94      2
    16   93      1
    14   91      1
    10   87      1
    22   99      1
    23   9C      1
    24   9D      1
    0    00      1

In conclusion, both R and Python offer efficient ways to download and
process AIANNH TIGER/Line Shapefile data from the U.S. Census Bureau.
The ‘sf’ package in R provides a simple way to read and manipulate
spatial data, while the ‘geopandas’ library in Python offers similar
functionality. The ‘dplyr’ package in R can be used for data
manipulation and analysis, and Python’s built-in functions like
value_counts() can be used for aggregating data. Depending on your
preferred programming language and environment, both options can be
effective for working with AIANNH data.
