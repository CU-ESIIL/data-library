Uranium Mines and Mills Location Database
================

Created by the EPA, the [Uranium Mines and Mills Location
Database](https://www.epa.gov/radiation/uranium-mines-and-mills-location-database-0)
is comprised of information regarding known or potential mine and mill
locations and mine features from federal, state, and Tribal agencies
into a single database. More information can be found
[here](https://www.epa.gov/sites/default/files/2015-05/documents/402-r-05-009.pdf).

In R, we need 3 packages to download and visualize the data. First,
check if the packages are already installed. Install them if they are
not:

``` r
packages <- c("tidyverse", "httr", "sf") 
new.packages <- packages[!(packages %in% installed.packages()[,"Package"])] 
if(length(new.packages)>0) install.packages(new.packages)
```

Then, load them:

``` r
lapply(packages, library, character.only = TRUE)
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

Download the data set:

``` r
url <- "https://www.epa.gov/sites/default/files/2015-03/uld-ii_gis.zip" 
Uranium <- GET(url)
data_file <- "Uranium_mines.zip"
writeBin(content(Uranium, "raw"), data_file)

# Unzip the file 
unzip(data_file)
```

Read the data set:

``` r
mines <- st_read("Master_Database_and_Shape_Files/ULD_albers.shp")
```

    Reading layer `ULD_albers' from data source 
      `/Users/viig7608/Desktop/data library/Uranium_mines/Master_Database_and_Shape_Files/ULD_albers.shp' 
      using driver `ESRI Shapefile'
    Simple feature collection with 14810 features and 30 fields
    Geometry type: MULTIPOINT
    Dimension:     XY
    Bounding box:  xmin: -3296195 ymin: -1542681 xmax: 1955673 ymax: 4183792
    Projected CRS: North_America_Albers_Equal_Area_Conic

Calculate number of mines per county in Colorado:

``` r
mines_co <- mines %>% 
  filter(STATE_NAME %in% 'Colorado') %>% 
  group_by(COUNTY_NAM) %>% 
  summarise(mines = n())
```

And plot them (top ten):

``` r
mines_co <- mines_co[order(-mines_co$mines),][1:10,] %>% 
  mutate(COUNTY_NAM = factor(COUNTY_NAM))
ggplot(mines_co) +
  geom_bar(aes(y = fct_reorder(COUNTY_NAM, mines), x = mines), stat = "identity") +
  xlab("Number of Uranium mines") +
  ylab("") +
  theme_bw() +
  ggtitle("Top 10 counties with Uranium mines in Colorado")
```

![](Uranium_mines_files/figure-commonmark/unnamed-chunk-6-1.png)

In Python, we need 4 libraries to download and visualize the data. You
can find data definitions and sources
[here](https://www.epa.gov/sites/default/files/2015-05/documents/402-r-05-009.pdf).

``` python
import requests
import zipfile
import geopandas as gpd
import matplotlib.pyplot as plt
```

Download the data set:

``` python
# download file
url = "https://www.epa.gov/sites/default/files/2015-03/uld-ii_gis.zip"
response = requests.get(url)

# save to file
data_file = "Uranium_mines.zip"
with open(data_file, 'wb') as f:
    f.write(response.content)

# unzip file
```

    222483119

``` python
with zipfile.ZipFile(data_file, 'r') as zip_ref:
    zip_ref.extractall('.')
```

Read the data set:

``` python
mines = gpd.read_file("Master_Database_and_Shape_Files/ULD_albers.shp")
```

Calculate number of mines per county in Colorado:

``` python
mines_co = (
    mines
    .loc[mines['STATE_NAME'] == 'Colorado']
    .groupby('COUNTY_NAM')
    .agg(mines=('COUNTY_NAM', 'size'))
)
```

And plot them (top ten):

``` python
mines_co = mines_co.sort_values('mines', ascending=False).iloc[:10]

plt.barh(y=mines_co.index, width=mines_co['mines'])
```

    <BarContainer object of 10 artists>

``` python
plt.xlabel('Number of Uranium mines')
plt.ylabel('County')
plt.title('Top 10 counties with Uranium mines in Colorado')
plt.gca().invert_yaxis()
plt.show()
```

![](Uranium_mines_files/figure-commonmark/unnamed-chunk-11-1.png)
