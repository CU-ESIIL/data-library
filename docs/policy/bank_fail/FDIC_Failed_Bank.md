FDIC Failed Banks
================

The FDIC Failed Bank List dataset from data.gov provides a list of banks
that have failed since October 1, 2000. The Federal Deposit Insurance
Corporation (FDIC) is a United States government corporation providing
deposit insurance to depositors in U.S. commercial banks and savings
institutions. This dataset includes details such as the bank name, city,
state, certification number, acquisition institution, closing date, and
updated date.

Here is the code in R and Python to download and wrangle this dataset:

R code:

``` r
library(dplyr)
# Define dataset URL
data <- read.csv("https://www.fdic.gov/resources/resolutions/bank-failures/failed-bank-list/banklist.csv", check.names = F)

names(data) <- c("Bank Name","City","State","Cert","Acquiring Institution", "Closing Date","Fund" )

filtered_data <- data %>%
  dplyr::filter(State == "CO")

filtered_data
```

                             Bank Name              City State  Cert
    1                     Premier Bank            Denver    CO 34112
    2      Community Banks of Colorado Greenwood Village    CO 21132
    3                   Bank of Choice           Greeley    CO  2994
    4                   Signature Bank           Windsor    CO 57835
    5            Colorado Capital Bank       Castle Rock    CO 34522
    6                    FirsTier Bank        Louisville    CO 57646
    7              United Western Bank            Denver    CO 31293
    8  Southern Colorado National Bank            Pueblo    CO 57263
    9                New Frontier Bank           Greeley    CO 34881
    10          Colorado National Bank  Colorado Springs    CO 18896
                     Acquiring Institution Closing Date  Fund
    1            United Fidelity Bank, fsb    10-Jul-15 10515
    2                   Bank Midwest, N.A.    21-Oct-11 10405
    3                   Bank Midwest, N.A.    22-Jul-11 10380
    4           Points West Community Bank     8-Jul-11 10375
    5  First-Citizens Bank & Trust Company     8-Jul-11 10373
    6                          No Acquirer    28-Jan-11 10334
    7  First-Citizens Bank & Trust Company    21-Jan-11 10331
    8                          Legacy Bank     2-Oct-09 10123
    9                          No Acquirer    10-Apr-09 10050
    10                        Herring Bank    20-Mar-09 10045
