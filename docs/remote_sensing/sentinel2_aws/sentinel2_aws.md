Sentinel2 Hyperspectral Data on AWS
================
Erick Verleye, ESIIL Software Developer
2023-08-08

SENTINEL-2 is a high-resolution, multi-spectral Earth imaging mission comprised
of twin satellites. Together their payloads sample 13 different spectral bands:
four bands at 10 m, six bands at 20 m and three bands at 60 m spatial
resolution. Sentinel2 data is particularly useful for mapping changes
or cloud corrected swaths of land cover. 

SENTINEL-2 data can be accessed on the web at the Copernicus Open Access Hub,
however data rate limits can significantly increase download times for large requests. 
Alternatively, Sentinel-2 data can be downloaded from publicly available AWS S3 buckets much faster, 
but for a small data transfer cost.

This write up will show how to download Sentinel Level-1 C data from S3 with 
Python for a given latitude, longitude, and date range. Please note that as the 
download charges are 'Requester-pays', you will need an AWS account and will be charged (a small amount)
for any data downloaded.

We must first import some packages, the versions for the non-native packages
used at the time of writing are:  

- boto3==1.26.131  
- geojson==3.0.1  
- tqdm==4.65.0  
- shapely==2.0.1  

``` {python}
import json

import multiprocessing as mp
import os

from argparse import Namespace
from datetime import datetime, timedelta
from typing import List, Tuple, Union

import boto3
import geojson
import tqdm
from shapely.geometry import Polygon
```

Next, we must use boto3 to create a connection to our AWS account. The 
initialization of the boto3.client object will be different depending on the environment you are running this code in:  

- Using the AWS CLI from a personal computer to log in, the aws_access_key_id 
and aws_secret_access_key arguments are required.  
- Using a federated access login like saml2aws, the aws_access_key_id, aws_secret_access_key, and aws_session_token are required.  
- From an EC2 instance with an IAM profile configured with s3 permissions,
none of the optional arguments are required.  

Each of these arguments, if applicable, can be found in the aws credentials
file typically found at ~/.aws/credentials

``` {python}
def intialize_client(aws_access_key_id: str = None, aws_secret_access_key: str = None, aws_session_token: str = None):
    return boto3.client(
        's3',
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        aws_session_token=aws_session_token
    )

# AWS CLI
s3_client = initialize_client(aws_access_key_id='my_access_key', aws_secret_access_key='my_secret_access_key')

# Federated login
s3_client = initialize_client(aws_access_key_id='my_access_key', aws_secret_access_key='my_secret_access_key', aws_session_token='my_session_token')

# S3 configured IAM profile on EC2 instance
s3_client = initialize_client()

```

Now that a connection to the AWS account has been created through the client 
object, let's define some constants. We will also define several functions to
make downloading the data easier:  

- find_available_files   
  -- finds the set of available files in the s3 bucket given a date range,
  lat/lon bounds, and list of bands.  
  
- find_overlapping_mgrs  
  -- The Sentinel-2 data is organized depending on which Military Grid Reference System (MGRS)
  square that it belongs to. This function converts a bounding box defined in
  lat/lon as [min_lon, min_lat, max_lon, max_lat] to the military grid squares that is overlaps.
  More information on the MGRS can be found at https://www.maptools.com/tutorials/mgrs/quick_guide



``` {python}
SENTINEL_2_BUCKET_NAME = 'sentinel-s2-l1c'  # Name of the s3 bucket on AWS hosting the sentinel-2 data


def find_overlapping_mgrs(bounds: List[float]) -> List[str]:
    """
    Files in the Sinergise Sentinel2 S3 bucket are organized by which military grid they overlap. Thus, the
    military grids that overlap the input bounding box defined in lat / lon must be found. A lookup table that
    includes each grid name and its geometry is used to find the overlapping grids.
    Args:
        bounds (list): Bounding box definition as [min_lon, min_lat, max_lon, max_lat]
    """
    print('Finding overlapping tiles... ')
    input_bounds = Polygon([(bounds[0], bounds[1]), (bounds[2], bounds[1]), (bounds[2], bounds[3]),
                            (bounds[0], bounds[3]), (bounds[0], bounds[1])])
    with open('mgrs_lookup.geojson', 'r') as f:
        ft = geojson.load(f)
        return [i['properties']['mgs'] for i in ft[1:] if
                input_bounds.intersects(Polygon(i['geometry']['coordinates'][0]))]


def find_available_files(self, bounds: List[float], start_date: datetime, end_date: datetime,
bands: List[str]) -> List[Tuple[str, str]]:
    """
    Given a bounding box and start / end date, finds which files are available on the bucket and
    meet the search criteria
    Args:
        bounds (list): Lower left and top right corner of bounding box defined in 
        lat / lon [min_lon, min_lat, max_lon, max_lat]
        start_date (str): Beginning of requested data creation date YYYY-MM-DD
        end_date (str): End of requested data creation date YYYY-MM-DD
    """
    date_paths = []
    while start_date <= end_date:
        tt = ref_date.timetuple()
        date_paths.append(f'/{tt.tm_year}/{tt.tm_mon}/{tt.tm_mday}/')
        ref_date = ref_date + timedelta(days=1)

    info = []
    mgrs_grids = self.find_overlapping_mgrs(bounds)
    for grid_string in mgrs_grids:
        utm_code = grid_string[:2]
        latitude_band = grid_string[2]
        square = grid_string[3:5]
        grid = f'tiles/{utm_code}/{latitude_band}/{square}'
        response = self._s3.list_objects_v2(
            Bucket=self._bucket_name,
            Prefix=grid + '/',
            MaxKeys=300,
            RequestPayer='requester'
        )
        if 'Contents' not in list(response.keys()):
            continue

        for date in date_paths:
            response = self._s3.list_objects_v2(
                Bucket=self._bucket_name,
                Prefix=grid + date + '0/',  # '0/' is for the sequence, which in most cases will be 0
                MaxKeys=100,
                RequestPayer='requester'
            )
            if 'Contents' in list(response.keys()):
                info += [
                    (v['Key'], v['Size']) for v in response['Contents'] if
                    any([band + '.jp2' in v['Key'] for band in bands]) or 'MSK_CLOUDS_B00.gml' in v['Key']
                ]

    return info
```



