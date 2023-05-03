USGS Water Services
================

``` r
library(httr)
library(jsonlite)


site <- "01594440"  # USGS site number for a specific location
url <- paste0("https://waterservices.usgs.gov/nwis/iv/?format=json&sites=", site, "&parameterCd=00060&siteStatus=all")

response <- GET(url)

if (status_code(response) == 200) {
  data <- fromJSON(content(response, "text", encoding = "UTF-8"))
  kable(data)
} else {
  cat(paste("Error:", status_code(response)), "\n")
}
```

    Warning in `[<-.data.frame`(`*tmp*`, , j, value = structure(list(siteName =
    structure("PATUXENT RIVER NEAR BOWIE, MD", class = "AsIs"), : provided 14
    variables to replace 1 variables

    Warning in `[<-.data.frame`(`*tmp*`, , j, value = structure(list(variableCode =
    structure("00060, NWIS, NWIS:UnitValues, 45807197, TRUE", class = "AsIs"), :
    provided 10 variables to replace 1 variables

<table class="kable_wrapper">
<tbody>
<tr>
<td>

| x                          |
|:---------------------------|
| ns1:timeSeriesResponseType |

</td>
<td>

| x                                         |
|:------------------------------------------|
| org.cuahsi.waterml.TimeSeriesResponseType |

</td>
<td>

| x                                       |
|:----------------------------------------|
| javax.xml.bind.JAXBElement\$GlobalScope |

</td>
<td>
<table class="kable_wrapper">
<tbody>
<tr>
<td>
<table class="kable_wrapper">
<tbody>
<tr>
<td>

| x                                                                                                 |
|:--------------------------------------------------------------------------------------------------|
| http://waterservices.usgs.gov/nwis/iv/format=json&sites=01594440&parameterCd=00060&siteStatus=all |

</td>
<td>
<table class="kable_wrapper">
<tbody>
<tr>
<td>

| x                |
|:-----------------|
| \[ALL:01594440\] |

</td>
<td>

| x         |
|:----------|
| \[00060\] |

</td>
<td>
<table class="kable_wrapper">
<tbody>
<tr>
<td>
</td>
</tr>
</tbody>
</table>
</td>
</tr>
</tbody>
</table>
</td>
<td>

| value                                                                                                                  | title            |
|:-----------------------------------------------------------------------------------------------------------------------|:-----------------|
| \[ALL:01594440\]                                                                                                       | filter:sites     |
| \[mode=LATEST, modifiedSince=null\]                                                                                    | filter:timeRange |
| methodIds=\[ALL\]                                                                                                      | filter:methodId  |
| 2023-05-03T02:11:35.876Z                                                                                               | requestDT        |
| d4ba2930-e957-11ed-af61-005056beda50                                                                                   | requestId        |
| Provisional data are subject to revision. Go to http://waterdata.usgs.gov/nwis/help/?provisional for more information. | disclaimer       |
| caas01                                                                                                                 | server           |

</td>
</tr>
</tbody>
</table>
</td>
<td>

| sourceInfo                    | variable                                     | values                                                                                                              | name                      |
|:------------------------------|:---------------------------------------------|:--------------------------------------------------------------------------------------------------------------------|:--------------------------|
| PATUXENT RIVER NEAR BOWIE, MD | 00060, NWIS, NWIS:UnitValues, 45807197, TRUE | 340 , P , 2023-05-02T21:45:00.000-04:00 , P , Provisional data subject to revision., 0 , NWIS , uv_rmk_cd , , 69783 | USGS:01594440:00060:00000 |

</td>
</tr>
</tbody>
</table>
</td>
<td>

| x     |
|:------|
| FALSE |

</td>
<td>

| x    |
|:-----|
| TRUE |

</td>
<td>

| x     |
|:------|
| FALSE |

</td>
</tr>
</tbody>
</table>
