US Census
================

## Get data

Retrieving USA census data in R, R Tidy, and Python can be done using
different packages and libraries. Here are some working examples in code
for each language:

R:

To retrieve census data in R, we can use the tidycensus package. Here’s
an example of how to retrieve the total population for the state of
California:

R code:

``` r
library(tidycensus)
library(tidyverse)

# Set your Census API key
census_api_key("your_api_key")

# Get the total population for the state of California
ca_pop <- get_acs(
  geography = "state",
  variables = "B01003_001",
  state = "CA"
) %>% 
  rename(total_population = estimate) %>% 
  select(total_population)

# View the result
ca_pop
```

R Tidy:

To retrieve census data in R Tidy, we can also use the tidycensus
package. Here’s an example of how to retrieve the total population for
the state of California using pipes and dplyr functions:

R tidy code:

``` r
library(tidycensus)
library(tidyverse)

# Set your Census API key
census_api_key("your_api_key")

# Get the total population for the state of California
ca_pop <- get_acs(
  geography = "state",
  variables = "B01003_001",
  state = "CA"
) %>% 
  rename(total_population = estimate) %>% 
  select(total_population)

# View the result
ca_pop
```

Python:

To retrieve census data in Python, we can use the census library. Here’s
an example of how to retrieve the total population for the state of
California:

Python code:

``` python
from census import Census
from us import states
import pandas as pd

# Set your Census API key
c = Census("your_api_key")

# Get the total population for the state of California
ca_pop = c.acs5.state(("B01003_001"), states.CA.fips, year=2019)

# Convert the result to a Pandas DataFrame
ca_pop_df = pd.DataFrame(ca_pop)

# Rename the column
ca_pop_df = ca_pop_df.rename(columns={"B01003_001E": "total_population"})

# Select only the total population column
ca_pop_df = ca_pop_df[["total_population"]]

# View the result
ca_pop_df
```

## Public health example

``` r
# example code for downloading poverty measures from the American Community
# Survey through tidycensus and visualizing them through maps

# load the packages we'll use for this section
library(tidycensus)
library(tidyverse)
library(sf)
library(RColorBrewer)
library(mapview)

# download the data from the ACS using the get_acs method from tidycensus
# 
# the B05010_002E variable refers to the count of residents who live in
# households with household income below the poverty line; the B05010_001E
# variable refers to the count of residents for whom household income was
# ascertained by the ACS, e.g. the relevant denominator.
# 
poverty <- get_acs(
  state = 'MA',
  county = '025', # this is the FIPS code for Suffolk County, MA
  geography = 'tract',
  year = 2019, # this indicates the 2015-2019 5-year acs 
  geometry = TRUE,
  variables = c(
    in_poverty = 'B05010_002E', 
    total_pop_for_poverty_estimates = 'B05010_001E') 
)
```


      |                                                                            
      |                                                                      |   0%
      |                                                                            
      |=                                                                     |   1%
      |                                                                            
      |=                                                                     |   2%
      |                                                                            
      |==                                                                    |   2%
      |                                                                            
      |==                                                                    |   3%
      |                                                                            
      |===                                                                   |   4%
      |                                                                            
      |====                                                                  |   5%
      |                                                                            
      |====                                                                  |   6%
      |                                                                            
      |=====                                                                 |   6%
      |                                                                            
      |=====                                                                 |   7%
      |                                                                            
      |=====                                                                 |   8%
      |                                                                            
      |======                                                                |   9%
      |                                                                            
      |=======                                                               |  10%
      |                                                                            
      |=======                                                               |  11%
      |                                                                            
      |========                                                              |  11%
      |                                                                            
      |========                                                              |  12%
      |                                                                            
      |=========                                                             |  13%
      |                                                                            
      |==========                                                            |  14%
      |                                                                            
      |==========                                                            |  15%
      |                                                                            
      |===========                                                           |  15%
      |                                                                            
      |===========                                                           |  16%
      |                                                                            
      |============                                                          |  17%
      |                                                                            
      |=============                                                         |  18%
      |                                                                            
      |==============                                                        |  20%
      |                                                                            
      |===============                                                       |  21%
      |                                                                            
      |===============                                                       |  22%
      |                                                                            
      |================                                                      |  22%
      |                                                                            
      |================                                                      |  23%
      |                                                                            
      |=================                                                     |  24%
      |                                                                            
      |==================                                                    |  25%
      |                                                                            
      |==================                                                    |  26%
      |                                                                            
      |===================                                                   |  26%
      |                                                                            
      |===================                                                   |  27%
      |                                                                            
      |====================                                                  |  28%
      |                                                                            
      |====================                                                  |  29%
      |                                                                            
      |=====================                                                 |  29%
      |                                                                            
      |=====================                                                 |  30%
      |                                                                            
      |=====================                                                 |  31%
      |                                                                            
      |======================                                                |  31%
      |                                                                            
      |======================                                                |  32%
      |                                                                            
      |=======================                                               |  33%
      |                                                                            
      |=======================                                               |  34%
      |                                                                            
      |========================                                              |  34%
      |                                                                            
      |========================                                              |  35%
      |                                                                            
      |=========================                                             |  35%
      |                                                                            
      |==========================                                            |  37%
      |                                                                            
      |==========================                                            |  38%
      |                                                                            
      |===========================                                           |  39%
      |                                                                            
      |============================                                          |  40%
      |                                                                            
      |=============================                                         |  41%
      |                                                                            
      |=============================                                         |  42%
      |                                                                            
      |==============================                                        |  42%
      |                                                                            
      |==============================                                        |  43%
      |                                                                            
      |===============================                                       |  44%
      |                                                                            
      |================================                                      |  45%
      |                                                                            
      |================================                                      |  46%
      |                                                                            
      |=================================                                     |  47%
      |                                                                            
      |==================================                                    |  49%
      |                                                                            
      |===================================                                   |  50%
      |                                                                            
      |===================================                                   |  51%
      |                                                                            
      |====================================                                  |  51%
      |                                                                            
      |====================================                                  |  52%
      |                                                                            
      |=====================================                                 |  53%
      |                                                                            
      |======================================                                |  54%
      |                                                                            
      |======================================                                |  55%
      |                                                                            
      |=======================================                               |  55%
      |                                                                            
      |=======================================                               |  56%
      |                                                                            
      |========================================                              |  57%
      |                                                                            
      |========================================                              |  58%
      |                                                                            
      |=========================================                             |  58%
      |                                                                            
      |=========================================                             |  59%
      |                                                                            
      |==========================================                            |  60%
      |                                                                            
      |===========================================                           |  61%
      |                                                                            
      |============================================                          |  62%
      |                                                                            
      |============================================                          |  63%
      |                                                                            
      |=============================================                         |  64%
      |                                                                            
      |==============================================                        |  65%
      |                                                                            
      |==============================================                        |  66%
      |                                                                            
      |===============================================                       |  67%
      |                                                                            
      |=================================================                     |  69%
      |                                                                            
      |=================================================                     |  71%
      |                                                                            
      |==================================================                    |  72%
      |                                                                            
      |===================================================                   |  73%
      |                                                                            
      |====================================================                  |  74%
      |                                                                            
      |=====================================================                 |  75%
      |                                                                            
      |=====================================================                 |  76%
      |                                                                            
      |=======================================================               |  78%
      |                                                                            
      |========================================================              |  79%
      |                                                                            
      |=================================================================     |  93%
      |                                                                            
      |==================================================================    |  94%
      |                                                                            
      |==================================================================    |  95%
      |                                                                            
      |===================================================================   |  96%
      |                                                                            
      |===================================================================== |  98%
      |                                                                            
      |===================================================================== |  99%
      |                                                                            
      |======================================================================| 100%

``` r
# we're going to recode the variable names to more human-readable names to 
# make it easier to work with the data in subsequent steps
poverty <- poverty %>% 
  mutate(
    variable = recode(variable,
                     # you may notice that tidycensus drops the 'E' from the 
                     # end of the variable code names
                     B05010_002 = 'in_poverty',
                     B05010_001 = 'total_pop_for_poverty_estimates'))

# pivot the data wider so that the in_poverty and
# total_pop_for_poverty_estimates; this follows the "tidy" format and approach
# where each row corresponds to an observation.
# 
# because the pivot_wider method can mess up your data when your data contains
# geometry/shapefile information, we will remove the geomemtry information
# and add it back in later
poverty_geometry <- poverty %>% select(GEOID) %>% unique() # save the geometry data
poverty <- poverty %>% 
  sf::st_drop_geometry() %>% # remove geometry data
  tidyr::pivot_wider(
    id_cols = GEOID,
    names_from = variable,
    values_from = c(estimate, moe))

# calculate the proportion in poverty
poverty <- poverty %>% 
  mutate(
    proportion_in_poverty = estimate_in_poverty / estimate_total_pop_for_poverty_estimates,
    percent_in_poverty = proportion_in_poverty * 100)

# add the geometry back in -- 
# make sure to merge the data into the sf object with the sf object on the 
# left hand side so the output has the sf type including your geometry data
poverty <- poverty_geometry %>% 
  left_join(poverty)

# visualize our point estimates 
ggplot(poverty, aes(fill = proportion_in_poverty)) +
  geom_sf() +
  scale_fill_viridis_c(label = scales::percent_format(),
                       limits = c(0, 1)) +
  labs(fill = "Percent in Poverty") +
  ggtitle("Poverty Estimates in Suffolk County, Massachusetts",
          subtitle = "Based on American Community Survey 2015-2019 Estimates")
```

![](US_Census_files/figure-gfm/unnamed-chunk-4-1.png)

``` r
# visualize the denominator counts -- 
# of significance, note that there are several census tracts where the
# denominator is 0 resulting in NaN estimates for the percent in poverty.
ggplot(poverty, aes(fill = estimate_total_pop_for_poverty_estimates)) + 
  geom_sf() + 
  scale_fill_viridis_c(label = scales::comma_format(), direction = -1, 
                       breaks = c(0, 10, 100, 1000), trans = "log1p") + 
  labs(fill = "Number of People") + 
  ggtitle("Number of People in Denominator for Poverty Estimates", 
          paste0("Suffolk County, Massachusetts\n",
          "Based on American Community Survey 2015-2019 Estimates"))
```

![](US_Census_files/figure-gfm/unnamed-chunk-4-2.png)
