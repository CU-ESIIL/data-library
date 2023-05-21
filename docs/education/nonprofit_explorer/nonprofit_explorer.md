Nonprofit organizations
================
Ty Tuff, ESIIL Data Scientist
2023-05-21

## Nonprofit Explorer API by ProPublica

The Nonprofit Explorer API by ProPublica offers an invaluable resource
to anyone interested in exploring the extensive landscape of tax-exempt
organizations in the United States. Launched by ProPublica, a renowned
non-profit newsroom specializing in investigative journalism, this API
provides extensive access to data collected from millions of tax filings
sent to the Internal Revenue Service (IRS).

<https://projects.propublica.org/nonprofits/api>

The data accessible through the Nonprofit Explorer API encompasses
information about each organization’s financial details, including
revenues and expenses, mission statements, lists of officers, and more.
This information, sourced from the IRS, has been carefully organized and
made searchable, bringing a wealth of data to your fingertips.

A particularly significant feature of this API is its ability to search
through the database using specific keywords. In the example we’re about
to delve into, we’ll use the keyword “education”. This functionality
opens up countless avenues for analysis, helping researchers,
journalists, policy makers, and curious individuals alike to investigate
patterns, identify trends, and uncover insightful details about the
non-profit sector’s contribution to education.

Through this exploration, we aim to unlock a better understanding of the
non-profit ecosystem, its role in our society, and particularly its
impact on education. The insights we gain may serve as a foundation for
future research, decision making, and strategy development for those
working in or with the non-profit sector.

## Education

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

In conclusion, both R and Python offer efficient ways to fetch and
process data from APIs like the Nonprofit Explorer API. The ‘httr’ and
‘jsonlite’ libraries in R provide a straightforward way to make HTTP
requests and parse JSON data, while the ‘requests’ library in Python
offers similar functionality. The ‘pandas’ library in Python can be used
for data manipulation and analysis, and R provides built-in functions
like table() for aggregating data. Depending on your preferred
programming language and environment, both options can be effective for
working with the Nonprofit Explorer API.
