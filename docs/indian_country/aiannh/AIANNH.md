American Indian and Alaska Native Areas
================
Ty Tuff, ESIIL Data Scientist
2023-05-21

The National American Indian/Alaska Native/Native Hawaiian (AIANNH)
Areas Shapefile is a dataset that provides a comprehensive view of the
geographic, demographic, and cultural landscape of Indigenous
communities in the United States. This unique resource comprises diverse
legal entities, encompassing federally recognized American Indian
reservations, off-reservation trust lands, Alaska Native regional
corporations, and Native Hawaiian homelands.

These entities hold a rich tapestry of diverse cultures, languages, and
histories, each with unique stories to tell and invaluable wisdom to
impart. The AIANNH Areas Shapefile is more than just a collection of
data; it is a detailed map of vibrant communities and proud nations,
embodying the resilience and enduring spirit of the Indigenous peoples
of America.

For researchers, policy makers, educators, and anyone with a vested
interest in understanding these communities and their contributions to
the broader cultural fabric of the United States, this dataset serves as
a vital resource. Its depth and breadth offer unprecedented insights
into the geographic boundaries that define these communities, the
demographic characteristics that diversify them, and the cultural
aspects that unify and distinguish them.

From the wild expanses of Alaska to the lush tropical landscapes of
Hawaii, and across the vast American mainland, the AIANNH Areas
Shapefile traces the footsteps of the First Nations. By diving into this
dataset, you are not only exploring data, but also appreciating the rich
tapestry of cultures that form an integral part of the United States’
historical, present, and future narrative.

<https://catalog.data.gov/dataset/tiger-line-shapefile-2020-nation-u-s-american-indian-alaska-native-native-hawaiian-aiannh-areas>

R code:

``` r
# Install and load necessary libraries
library(sf)
library(dplyr)
library(knitr)

# Download dataset from source
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
