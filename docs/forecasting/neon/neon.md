NEON carbon
================
Ty Tuff, ESIIL Data Scientist
2023-05-21

``` r
library(neonUtilities)
library(ggplot2)

foliar <- loadByProduct(dpID="DP1.10026.001", site="all", 
                        package="expanded", check.size=F,
                        token=my_token)


names(foliar)

ggplot(foliar$cfc_carbonNitrogen, aes(x = carbonPercent, y = CNratio)) +
  geom_point() +
  labs(title = "Carbon to Nitrogen Ratio vs Carbon Concentration",
       x = "Carbon Concentration (percent)",
       y = "Carbon to Nitrogen Ratio") +
  theme_minimal()
```

![](neon_files/figure-gfm/unnamed-chunk-2-1.png)

``` python
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from neon_api_tools.api_tools import neon_api_tools

# Set your NEON API token
my_token = "your_neon_api_token_here"

# Instantiate the API tools object
neon_tools = neon_api_tools()

# Download the NEON foliar data
foliar = neon_tools.loadByProduct(dpID="DP1.10026.001", site="all",
                                  package="expanded", check_size=False,
                                  token=my_token)

# Get the foliar dataframe
foliar_df = foliar['cfc_carbonNitrogen']

# Plot the carbon to nitrogen ratio against the carbon concentration
fig, ax = plt.subplots()
ax.scatter(foliar_df['carbonPercent'], foliar_df['CNratio'])
ax.set_xlabel("Carbon Concentration (percent)")
ax.set_ylabel("Carbon to Nitrogen Ratio")
ax.set_title("Carbon to Nitrogen Ratio vs Carbon Concentration")
plt.show()
```
