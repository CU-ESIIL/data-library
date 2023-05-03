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
  print(data)
} else {
  cat(paste("Error:", status_code(response)), "\n")
}
```

    $name
    [1] "ns1:timeSeriesResponseType"

    $declaredType
    [1] "org.cuahsi.waterml.TimeSeriesResponseType"

    $scope
    [1] "javax.xml.bind.JAXBElement$GlobalScope"

    $value
    $value$queryInfo
    $value$queryInfo$queryURL
    [1] "http://waterservices.usgs.gov/nwis/iv/format=json&sites=01594440&parameterCd=00060&siteStatus=all"

    $value$queryInfo$criteria
    $value$queryInfo$criteria$locationParam
    [1] "[ALL:01594440]"

    $value$queryInfo$criteria$variableParam
    [1] "[00060]"

    $value$queryInfo$criteria$parameter
    list()


    $value$queryInfo$note
                                                                                                                       value
    1                                                                                                         [ALL:01594440]
    2                                                                                      [mode=LATEST, modifiedSince=null]
    3                                                                                                        methodIds=[ALL]
    4                                                                                               2023-05-03T02:07:26.793Z
    5                                                                                   40431c80-e957-11ed-a823-2cea7f5e5ede
    6 Provisional data are subject to revision. Go to http://waterdata.usgs.gov/nwis/help/?provisional for more information.
    7                                                                                                                 sdas01
                 title
    1     filter:sites
    2 filter:timeRange
    3  filter:methodId
    4        requestDT
    5        requestId
    6       disclaimer
    7           server


    $value$timeSeries
                sourceInfo.siteName  sourceInfo.siteCode
    1 PATUXENT RIVER NEAR BOWIE, MD 01594440, NWIS, USGS
      sourceInfo.timeZoneInfo.defaultTimeZone.zoneOffset
    1                                             -05:00
      sourceInfo.timeZoneInfo.defaultTimeZone.zoneAbbreviation
    1                                                      EST
      sourceInfo.timeZoneInfo.daylightSavingsTimeZone.zoneOffset
    1                                                     -04:00
      sourceInfo.timeZoneInfo.daylightSavingsTimeZone.zoneAbbreviation
    1                                                              EDT
      sourceInfo.timeZoneInfo.siteUsesDaylightSavingsTime
    1                                                TRUE
      sourceInfo.geoLocation.geogLocation.srs
    1                               EPSG:4326
      sourceInfo.geoLocation.geogLocation.latitude
    1                                     38.95592
      sourceInfo.geoLocation.geogLocation.longitude
    1                                     -76.69369
      sourceInfo.geoLocation.localSiteXY sourceInfo.note sourceInfo.siteType
    1                               NULL            NULL                NULL
                                            sourceInfo.siteProperty
    1 ST, 02060006, 24, 24003, siteTypeCd, hucCd, stateCd, countyCd
                             variable.variableCode  variable.variableName
    1 00060, NWIS, NWIS:UnitValues, 45807197, TRUE Streamflow, ft&#179;/s
          variable.variableDescription variable.valueType variable.unitCode
    1 Discharge, cubic feet per second      Derived Value             ft3/s
       variable.option variable.note variable.noDataValue variable.variableProperty
    1 Statistic, 00000          NULL              -999999                      NULL
      variable.oid
    1     45807197
                                                                                                            values
    1 340, P, 2023-05-02T21:45:00.000-04:00, P, Provisional data subject to revision., 0, NWIS, uv_rmk_cd, , 69783
                           name
    1 USGS:01594440:00060:00000


    $nil
    [1] FALSE

    $globalScope
    [1] TRUE

    $typeSubstituted
    [1] FALSE
