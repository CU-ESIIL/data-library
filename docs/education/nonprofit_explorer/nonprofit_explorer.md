Nonprofit organizations
================

## Nonprofit Explorer API by ProPublica

The Nonprofit Explorer API by ProPublica provides data on tax-exempt
organizations in the United States. In this example, we’ll search for
organizations with the keyword “education” and analyze the results.

R: In R, we’ll use the ‘httr’ and ‘jsonlite’ packages to fetch and
process data from the Nonprofit Explorer API.

R code:

``` r
# Install and load necessary libraries
library(httr)
library(jsonlite)

# Fetch data for organizations with the keyword "education"
url <- "https://projects.propublica.org/nonprofits/api/v2/search.json?q=education"
response <- GET(url)

# Check if the request was successful
if (http_status(response)$category == "Success") {
  data <- content(response, "parsed")
  organizations <- data$organizations
  
  # Count the number of organizations per state
  state_counts <- table(sapply(organizations, function(x) x$state))
  print(state_counts)
} else {
  print(http_status(response)$message)
}
```


         AZ      CA      CO      DC      FL      GA      HI      IA      ID      IL 
          3      19       6       2       4       1       1       1       1       5 
    Indiana      LA      MA      MD      MI      MN      MO      MP      MS      NC 
          1       2       1       1       2       5       3       1       2       2 
         ND      NE      NJ      NY      OH  Oregon      PA      TX      UT      VA 
          1       1       3       1       6       1       2      13       2       3 
         WA      ZZ 
          2       2 

Python: In Python, we’ll use the ‘requests’ library to fetch data from
the Nonprofit Explorer API and ‘pandas’ library to process the data.

Python code:

``` python
# Install necessary libraries
import requests
import pandas as pd

# Fetch data for organizations with the keyword "education"
url = "https://projects.propublica.org/nonprofits/api/v2/search.json?q=education"
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    data = response.json()
    organizations = data["organizations"]
    
    # Count the number of organizations per state
    state_counts = pd.DataFrame(organizations)["state"].value_counts()
    print(state_counts)
else:
    print(f"Error: {response.status_code}")
```

    CA         19
    TX         13
    OH          6
    CO          6
    IL          5
    MN          5
    FL          4
    MO          3
    NJ          3
    VA          3
    AZ          3
    DC          2
    MS          2
    WA          2
    MI          2
    UT          2
    NC          2
    LA          2
    PA          2
    ZZ          2
    Indiana     1
    NE          1
    NY          1
    Oregon      1
    HI          1
    GA          1
    MP          1
    MD          1
    IA          1
    ID          1
    ND          1
    MA          1
    Name: state, dtype: int64

In conclusion, both R and Python offer efficient ways to fetch and
process data from APIs like the Nonprofit Explorer API. The ‘httr’ and
‘jsonlite’ libraries in R provide a straightforward way to make HTTP
requests and parse JSON data, while the ‘requests’ library in Python
offers similar functionality. The ‘pandas’ library in Python can be used
for data manipulation and analysis, and R provides built-in functions
like table() for aggregating data. Depending on your preferred
programming language and environment, both options can be effective for
working with the Nonprofit Explorer API.
