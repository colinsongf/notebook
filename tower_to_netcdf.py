# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <headingcell level=1>

# Save Tower CSV data as NetCDF

# <codecell>

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import netCDF4
import datetime as dt
import urllib
%matplotlib inline

# <codecell>

url='http://geoport.whoi.edu/thredds/fileServer/usgs/data2/notebook/data/CR3000_SN3557_Table1_MainTowerCR3000_ground_V6.CR3.txt'
input_data="/usgs/data2/notebook/data/CR3000_SN3557_Table1_MainTowerCR3000_ground_V6.CR3.dat"
output_dir="/usgs/data2/notebook/data"
output_file="julia.nc"

# <codecell>

urllib.urlretrieve (url,input_data)

# <codecell>

df = pd.read_csv(input_data,skiprows=[0,2,3],parse_dates=True,index_col=0,low_memory=False)

# <codecell>

df.head()

# <codecell>

df[['Tsoil10cmTree_Avg','Tsoil20cmTree_Avg']].plot(figsize=(12,4));

# <markdowncell>

# Now we use some tools from pytools to write a single time series to a netCDF file.  Right now it is set up to only handle one variable, so it's the total solution for dataframes with more than one column of time series data.   Each variable could be written to a separate file and then merged together using NCO (or NcML). 
# 
# To use the timeseries create tool, we pass in a list of tuples data=[(time, vertical, value)] or three numpy arrays times=, verticals=, values=, where time is seconds since epoch, and the verticals are the heights.  The code was written for tide gauge data, and writes the vertical as positive down, and relative to sea surface.  So it should be modified for land applications. 

# <codecell>

#from pytools.netcdf.sensors import create,ncml,merge,crawl
from pyaxiom.netcdf.sensors import create,ncml,merge,crawl

# <codecell>

def pd_to_secs(df):
    """
    convert a pandas datetime index to seconds since 1970
    """
    import calendar
    return np.asarray([ calendar.timegm(x.timetuple()) for x in df.index ], dtype=np.int64)

# <codecell>

secs = pd_to_secs(df)

# <codecell>

# set sensor height to 10 m
z = 10.0*np.ones_like(secs)

# <codecell>

# add units 
attributes={'units':'Celcius'}

# <codecell>

values = df['Tsoil10cmTree_Avg'].values

# <codecell>

sensor_urn='urn:edu.princeton.ecohydrolab:sensor:Tsoil10cmTree_Avg'
station_urn='urn:edu.princeton.ecohydrolab:station:MainTower'

# <codecell>

create.create_timeseries_file(output_directory=output_dir,
                              latitude=0.39,
                              longitude=36.7,
                              full_station_urn=station_urn,
                              full_sensor_urn=sensor_urn,
                              times=secs,
                              verticals=z, 
                              values=values,
                              attributes=attributes,
                              global_attributes={},
                              output_filename=output_file)

