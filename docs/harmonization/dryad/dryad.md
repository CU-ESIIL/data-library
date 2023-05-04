dryad
================

Dryad is a repository of curated, open access, data files associated
with published articles in the sciences and social sciences. To access a
dataset, you’ll first need to choose a dataset and get its DOI (Digital
Object Identifier) or a direct link to download the dataset. In this
example, we’ll use a dataset called “The phantom chorus: birdsong boosts
human well-being in protected areas” by Dr. Clinton Francis with DOI:
10.5061/dryad.vmcvdncs3.

R code:

``` r
install.packages("rdryad")
install.packages("ggplot2")
```

``` r
library(rdryad)
library(ggplot2)


search_results <- dryad_datasets()
print(search_results$data)
```

    # A tibble: 20 × 27
       identifier       id storageSize relatedPublicationISSN title authors abstract
       <chr>         <int>       <dbl> <chr>                  <chr> <list>  <chr>   
     1 doi:10.5061/…    93   999931789 0960-9822              "Dis… <df>    "<p>Ove…
     2 doi:10.5061/…    94   997532058 0960-9822              "Dat… <df>    "The st…
     3 doi:10.5061/…    95   997366561 0962-1083              "Dat… <df>    "Adapti…
     4 doi:10.5061/…    96   996067863 0003-0147              "Dat… <df>    "Unders…
     5 doi:10.5061/…    97   994990868 1439-4227              "Dat… <df>    "[No ab…
     6 doi:10.5061/…    98   994682183 1755-098X              "Dat… <df>    "To adv…
     7 doi:10.5061/…    99   994533047 0305-0270              "Dat… <df>    "Aim: C…
     8 doi:10.5061/…   100   992698314 2047-217X              "Dat… <df>    "Backgr…
     9 doi:10.5061/…   101   991316188 2054-5703              "Dat… <df>    "Severa…
    10 doi:10.5061/…   102   990328081 0014-3820              "Dat… <df>    "Groups…
    11 doi:10.5061/…   103   989481164 0092-8674              "Dat… <df>    "Phenot…
    12 doi:10.5061/…   104  9994758981 1932-6203              "Dat… <df>    "Backgr…
    13 doi:10.5061/…   105  9924107495 2052-4463              "Dat… <df>    "The hi…
    14 doi:10.5061/…   106  9921153994 1365-294X              "Dat… <df>    "Phylog…
    15 doi:10.5061/…   107  9907875274 1091-6490              "Dat… <df>    "Modula…
    16 doi:10.5061/…   108  9899272735 1755-098X              "Dat… <df>    "<p>Gra…
    17 doi:10.5061/…   109  9891854826 0962-8452              "Dat… <df>    "When t…
    18 doi:10.5061/…   110  9880500050 1544-9173              "Dat… <df>    "Given …
    19 doi:10.5061/…   111  9876101678 0962-8452              "Dat… <df>    "Climat…
    20 doi:10.5061/…   112  9858763736 2399-3421              "Dat… <df>    "Tens o…
    # ℹ 20 more variables: funders <list>, keywords <list>, locations <list>,
    #   relatedWorks <list>, versionNumber <int>, versionStatus <chr>,
    #   curationStatus <chr>, versionChanges <chr>, publicationDate <chr>,
    #   lastModificationDate <chr>, visibility <chr>, sharingLink <chr>,
    #   userId <int>, license <chr>, usageNotes <chr>, `_links.curies` <list>,
    #   `_links.self.href` <chr>, `_links.stash:versions.href` <chr>,
    #   `_links.stash:version.href` <chr>, `_links.stash:download.href` <chr>

``` r
# Get the first DOI from the search results
doi <-  "https://doi.org/10.5061/dryad.wwpzgmsgx"
clean_doi <- gsub("https://doi.org/", "", doi)

files <- dryad_download(clean_doi)
```

    using cached file: ~/Library/Caches/R/rdryad/10_5061_dryad_wwpzgmsgx.zip

    date created (size, mb): 2023-05-03 21:55:53 (0.308)

``` r
print(files)
```

    $`10.5061/dryad.wwpzgmsgx`
    [1] "/Users/ty/Library/Caches/R/rdryad/10_5061_dryad_wwpzgmsgx/Ferraro_etal_point_count_readme.rtf"            
    [2] "/Users/ty/Library/Caches/R/rdryad/10_5061_dryad_wwpzgmsgx/Ferraro_etal_pointcounts.csv"                   
    [3] "/Users/ty/Library/Caches/R/rdryad/10_5061_dryad_wwpzgmsgx/Ferraro_etal_survey_IdentifyerMasked_readme.rtf"
    [4] "/Users/ty/Library/Caches/R/rdryad/10_5061_dryad_wwpzgmsgx/Ferraro_etal_survey_IdentifyerMasked.csv"       
    [5] "/Users/ty/Library/Caches/R/rdryad/10_5061_dryad_wwpzgmsgx/Ferraro_PhanChorus_Sound.csv"                   
    [6] "/Users/ty/Library/Caches/R/rdryad/10_5061_dryad_wwpzgmsgx/ReadMe_Ferraro_PhanChorus_Sound.rtf"            

``` r
a <- unlist(files)
short_files <- as.data.frame(a)[,1]

# Identify the CSV file from the extracted files
csv_file <- list.files("/Users/ty/Library/Caches/R/rdryad/10_5061_dryad_wwpzgmsgx", pattern = ".csv", full.names = TRUE)[2]

# Read the CSV data
data <- read.csv(csv_file)

ggplot(data=data, aes(y=Perceivedrestoration, Sound_Comp)) +
  geom_point()
```

![](dryad_files/figure-gfm/unnamed-chunk-2-1.png)

``` python
import requests
import pandas as pd
import matplotlib.pyplot as plt
import io

# Search for datasets related to the term "habitat"
base_url = "https://datadryad.org/api/v2/datasets?"
params = {"query": "habitat"}

response = requests.get(base_url, params=params)
search_results = response.json()
print(search_results)

# Get the first DOI from the search results
doi = "https://doi.org/10.5061/dryad.wwpzgmsgx"
clean_doi = doi.replace("https://doi.org/", "")

# Download the dataset
files_url = f"https://datadryad.org/api/v2/datasets/{clean_doi}/download"
response = requests.get(files_url)
files = response.json()
print(files)

# Identify the CSV file from the extracted files
csv_file_url = None
for file in files['data']:
    if '.csv' in file['attributes']['name']:
        csv_file_url = file['links']['download']
        break

# Read the CSV data
response = requests.get(csv_file_url)
data = pd.read_csv(io.StringIO(response.text))

# Plot the data using pandas and matplotlib
# Replace 'Perceivedrestoration' and 'Sound_Comp' with the actual column names in your dataset
ax = data.plot(x='Perceivedrestoration', y='Sound_Comp', kind='scatter')
ax.set_xlabel('Perceivedrestoration')
ax.set_ylabel('Sound_Comp')
plt.show()
```
