Native lands Digital
================
Ty Tuff, ESIIL Data Scientist
2023-05-21

We are grateful to have the opportunity to work with data provided by
Native Land Digital <https://native-land.ca>. This data represents
territories, languages, and treaties associated with Indigenous nations
across North America and other parts of the world.

This rich dataset is more than just a collection of shapes, names, or
historical facts. Each entry represents a living community with a rich
history, vibrant culture, and ongoing connection to the lands and waters
that sustain them. The boundaries and names reflect deep relationships
between these communities and their homelands—relationships that predate
colonial borders and continue to be meaningful today.

Working with this data should be a continual reminder of the resilience
and diversity of Indigenous nations, as well as the ongoing struggles
they face to protect their rights, languages, and cultures. It’s also a
reminder of our responsibilities in acknowledging Indigenous lands,
respecting treaty rights, and supporting Indigenous sovereignty.

It is crucial to recognize that this data is not comprehensive nor
infallible. Despite the utmost care taken by Native Land Digital,
errors, omissions, or misrepresentations may exist, reflecting the
complex and often contentious nature of Indigenous histories and
geographies. It’s also important to note that Indigenous peoples have
diverse perspectives on the sharing and mapping of their lands,
languages, and cultures.

We encourage users of this data to learn more about the nations,
territories, languages, and treaties it represents, and to seek out and
respect Indigenous perspectives in their work. Always remember that
behind each data point is a community, a culture, and a history that
deserves our respect and understanding.

Finally, we acknowledge and express our gratitude to Native Land Digital
for their work in compiling and sharing this data. This work is a
powerful tool for education, reconciliation, and the affirmation of
Indigenous presence across the globe.

## Download from Native Land API

Please be aware that as part of this tutorial, we encountered challenges
when attempting to directly download and load the data from the Native
Land API using R due to its specific formatting. As a solution, we
turned to Python, which allowed for a more straightforward handling of
this dataset. Specifically, we used Python to download the data from the
API, convert it into a GeoDataFrame, and save it as a GeoJSON file. This
intermediate GeoJSON file was then successfully loaded into R for
further analysis. While this may seem like an extra step, it effectively
resolves the issue encountered in R, and facilitates a smooth
integration of the data into our R-based workflow. This approach
underscores the utility of being versatile in multiple programming
languages, as each language has its own strengths and may be more suited
to different tasks.

``` python
import requests
import geopandas as gpd
from shapely.geometry import shape
import matplotlib.pyplot as plt

# Send GET request to the API
response = requests.get("https://native-land.ca/api/index.php?maps=languages")

# The API returns a list of features
features = response.json()

# Filter out features with inconsistent coordinate dimensionality
filtered_features = []
for feature in features:
    try:
        # Attempt to construct a shapely shape from the geometry
        shape(feature['geometry'])
        filtered_features.append(feature)
    except ValueError:
        # If the shape construction fails due to a ValueError, skip this feature
        pass

# Wrap filtered features in a dictionary to create a valid GeoJSON
```

``` python
data_geojson = {"type": "FeatureCollection", "features": filtered_features}

# Convert the GeoJSON to a GeoDataFrame
data_gdf = gpd.GeoDataFrame.from_features(data_geojson)

data_gdf.to_file("data.geojson", driver='GeoJSON')

# Plot the data
```

``` python
data_gdf.plot(figsize=(10, 10))
plt.show()
```

![](native_lands_digital_files/figure-gfm/unnamed-chunk-1-1.png)

## Lakȟótiyapi (Lakota)

The Lakȟótiyapi, also known as the Lakota, are a group of indigenous
people who are part of the Sioux Nation. Historically, the Lakota people
lived in a large region in the central part of North America, spanning
from the Great Lakes in the east to the Rocky Mountains in the west, and
from Canada in the north to the northern part of modern-day Texas in the
south.

A significant aspect of Lakota history is their close association with
the Great Plains of the United States. Originally settled in the upper
Mississippi Region in what is now Minnesota, the Lakota migrated
westward in the late 17th and early 18th centuries as European settlers
pushed inland. This migration led them to the Great Plains, the region
that is often most associated with them.

Their traditional territory on the Great Plains is characterized by vast
grasslands, interrupted by the occasional forest and mountain range,
which made it an ideal location for a hunting and gathering lifestyle.
The Lakota were known as skilled horsemen and hunters, especially of the
American bison.

Please note that while these historical ranges provide a broad overview
of the territories that the Lakota people have lived in, they do not
capture the full depth and complexity of the relationships that
indigenous peoples have with their lands. These relationships are often
dynamic and evolving, and they are shaped by a rich tapestry of history,
culture, language, and spirituality.

For more information about the Lakota people and their language, visit
Native Land Digital’s map at
https://native-land.ca/maps/languages/lakotayapi/.

``` r
library(sf)
library(dplyr)
library(USAboundaries)
library(tidyverse)

states <- us_states(map_date = NULL) # for contemporary boundaries
counties <- us_counties(map_date = NULL) # for contemporary boundaries

native_lands <- read_sf("data.geojson")

names(native_lands)

data_for_plot <- native_lands %>% 
  filter(Name == "Lakȟótiyapi (Lakota)" )
print(data_for_plot$description)

# Calculate the bounding box of data_for_plot
bbox <- st_bbox(data_for_plot)

# Extract the xmin, xmax, ymin, and ymax values
xmin <- bbox[1]
xmax <- bbox[3]
ymin <- bbox[2]
ymax <- bbox[4]

names(counties)[13] <- "state_name_2"
boulder_county <- counties %>%
  filter( namelsad =="Boulder County")

# Add the boundaries to the ggplot
ggplot() + 
  geom_sf(data=data_for_plot) +
  geom_sf(data=states, fill=NA, color="black", size=0.2) +
  geom_sf(data=counties, fill=NA, color="grey", size=0.1) +
  geom_sf(data=boulder_county, fill="Blue") +
  coord_sf(xlim=c(xmin, xmax), ylim=c(ymin, ymax)) + 
  
  theme_minimal()
```

![](native_lands_digital_files/figure-gfm/unnamed-chunk-2-1.png)

-   Blue polygon is Boulder County, Colorado
