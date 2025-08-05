Sentinel2 Multispectral Data on AWS
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
initialization of the boto3.session object will be different depending on the environment you are running this code in:  

- Using the AWS CLI from a personal computer to log in, the profile name will typically be default. 
- Using a federated access login, the profile name will typically be the name of the software. 
- Using S3 configured IAM profile, no profile name is required.  

Each of these arguments, if applicable, can be found in the aws credentials
file typically found at ~/.aws/credentials

``` {python}
session = boto3.Session(profile_name=profile)

# AWS CLI
session = boto3.Session(profile_name='default')

# Federated login (saml2aws example)
session = boto3.Session(profile_name='saml')

# S3 configured IAM profile on EC2 instance
session = boto3.Session()

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
  

NOTE: You will have to download the mgrs_lookup.geojson file from 
https://github.com/CU-ESIIL/data-library/blob/main/docs/remote_sensing/sentinel2_aws/mgrs_lookup.geojson
and place it into the working directory that this code is being run from.


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


def find_available_files(s3_client, bounds: List[float], start_date: datetime, end_date: datetime,
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
    ref_date = start_date
    while ref_date <= end_date:
        tt = ref_date.timetuple()
        date_paths.append(f'/{tt.tm_year}/{tt.tm_mon}/{tt.tm_mday}/')
        ref_date = ref_date + timedelta(days=1)

    info = []
    mgrs_grids = find_overlapping_mgrs(bounds)
    for grid_string in mgrs_grids:
        utm_code = grid_string[:2]
        latitude_band = grid_string[2]
        square = grid_string[3:5]
        grid = f'tiles/{utm_code}/{latitude_band}/{square}'
        response = s3_client.list_objects_v2(
            Bucket=SENTINEL_2_BUCKET_NAME,
            Prefix=grid + '/',
            MaxKeys=300,
            RequestPayer='requester'
        )
        if 'Contents' not in list(response.keys()):
            continue

        for date in date_paths:
            response = s3_client.list_objects_v2(
                Bucket=SENTINEL_2_BUCKET_NAME,
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

Next we will define the download function which will bring everything together and start
requesting data from s3. This function is designed to download the files in parallel, so a download_task
function is defined as well. 
Note that multiprocessing will not work as implemented here in
iPython (Jupyter notebooks, etc.) and so that block of code is commented out. If you are 
running this in a different environment and would like to download in parallel, un-comment this block 
and comment the sequential block below.

``` {python}
def download_task(namespace: Namespace) -> None:
    """
    Downloads a single file from the indicated s3 bucket. This function is intended to be spawned in parallel from the
    parent process.
    Args:
        namespace (Namespace): Contains the bucket name, s3 file name, and destination required for s3 download request.
        Each value in the namespace must be a pickle-izable type (i.e. str).
    """
    session = boto3.Session(profile_name=namespace.profile_name)
    s3 = session.client('s3')
    s3.download_file(namespace.bucket_name, namespace.available_file,
                     namespace.dest,
                     ExtraArgs={'RequestPayer': 'requester'}
                     )


def download(session, bounds: List[float], start_date: datetime, end_date: datetime,
             bands: List[float], out_dir: str, buffer: float = None) -> None:
    """
    Downloads a list of .jp2 files from the Sinergise Sentinel2 LC1 bucket given a bounding box defined in lat/long, a buffer in meters, and a start and end date. Only Bands 2-4 are requested.
     Args:
         bounds (list): Bounding box defined in lat / lon [min_lon, min_lat, max_lon, max_lat]
         buffer (float): Amount by which to extend the bounding box by, in meters
         start_date (str): Beginning of requested data creation date YYYY-MM-DD
         end_date (str): End of requested data creation date YYYY-MM-DD
         bands (list): The bands to download for each file. Ex. ['B02', 'B03', 'B04', 'B08'] for R, G, B, and
         near wave IR, respectively
         out_dir (str): Path to directory where downloaded files will be written to
    """
    # Convert the buffer from meters to degrees lat/long at the equator
    if buffer is not None:
        buffer /= 111000

        # Adjust the bounding box to include the buffer (subtract from min lat/long values, add to max lat/long values)
        bounds[0] -= buffer
        bounds[1] -= buffer
        bounds[2] += buffer
        bounds[3] += buffer
    
    s3_client = session.client('s3')
    available_files = find_available_files(s3_client, bounds, start_date, end_date, bands)

    args = []
    total_data = 0
    for file_info in available_files:
        file_path = file_info[0]
        if '/preview/' in file_path:
            continue

        created_file_path = os.path.join(out_dir, file_path.replace('_qi_', '').replace('/', '_').replace('tiles_', ''))

        # Skip if file is already local
        if os.path.exists(created_file_path):
            continue

        total_data += file_info[1]

        args.append(Namespace(available_file=file_path, bucket_name=SENTINEL_2_BUCKET_NAME, profile_name=session.profile_name,
                              dest=created_file_path))

    total_data /= 1E9
    print(f'Found {len(args)} files for download. Total size of files is'
          f' {round(total_data, 2)}GB and estimated cost will be ${round(0.09 * total_data, 2)}'
          )
  
    # For multiprocessing when being run in iPython (Jupyter notebook, etc.)
    # with mp.Pool(mp.cpu_count() - 1) as pool:
        # for _ in tqdm.tqdm(pool.imap_unordered(download_task, args), total=len(args)):
            # pass
            
    # Sequential download for use in iPython (Jupyter notebooks, etc.) 
    for _ in tqdm.tqdm(args, total=len(args)):
        download_task(args)
    
```

Once all of the above functions and variables are defined, we can now run download for a certain time range and region.
First make sure the directory corresponding to the out_dir parameter you pass in already exists. If not, create the directory.

``` {python}
out_dir = 'Uganda'
os.makedirs(out_dir, exist_ok=True)

# Download RGB band data from the Kibaale district of Uganda from June 15, 2017 - June 30, 2017  
download(session=session, bounds=[30.5887, 0.0536, 31.7697, 1.8028], start_date=datetime(2017, 6, 15),
         end_date=datetime(2017, 6, 30), bands=['B02', 'B03', 'B04'], out_dir=out_dir)

```

Cloud files will be downloaded alongside the band data. These cloud files can be used to create 
cloud-corrected composite images over a region. To learn more about creating cloud corrected composites, check out our tutorial on ESIIL's Analytics Library: https://analytics-library.esiil.org/remote_sensing/sentinel2_cloud_correction/sentinel_2_cloud_correction/


