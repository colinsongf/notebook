# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <headingcell level=1>

# Convert CNR Wave Data to NetCDF DSG (CF-1.6)

# <markdowncell>

# From Davide Bonaldo at CNR-ISMAR :
#     here's a time series of wave data from Jesolo.
# * Columns 1 to 6: date (y m d h m s)
# * Column 7: Significant wave height (m)
# * Column 8: Mean period (s)
# * Column 9: Mean direction (deg)
# * Column 10: Sea surface elevation (m)

# <codecell>

import numpy as np
import urllib
%matplotlib inline

# <codecell>

url='https://www.dropbox.com/s/0epy3vsjgl1h8ld/ONDE_Jesolo.txt?dl=1'
local_file = '/usgs/data2/notebook/data/ONDE_Jesolo.txt'

# <codecell>

urllib.urlretrieve (url,local_file)

# <codecell>

from datetime import datetime

import pandas as pd

def date_parser(year, month, day, hour, minute, second):
    var = year, month, day, hour, minute, second
    var = [int(float(x)) for x in var]
    return datetime(*var)

df = pd.read_csv(local_file, header=None,
                 delim_whitespace=True, index_col='datetime',
                 parse_dates={'datetime': [0, 1, 2, 3, 4, 5]},
                 date_parser=date_parser)

# <codecell>

df.columns=['Hsig','Twave','Dwave','Wlevel']

# <codecell>

df[['Hsig','Wlevel']].plot()

# <codecell>

def pd_to_secs(df):
    """
    convert a pandas datetime index to seconds since 1970
    """
    return [x.total_seconds() for x in df.index.to_pydatetime()-pd.to_datetime('1970-01-01')]

# <codecell>

secs = pd_to_secs(df)

# <codecell>

z = np.zeros_like(secs)

# <codecell>

values = df['Hsig'].values

# <codecell>

times=np.asarray(secs, dtype=np.int64)

# <codecell>

from pytools.netcdf.sensors import create,ncml,merge,crawl

# <codecell>

sensor_urn='urn:it.cnr.ismar.ve:sensor:wave_height'
station_urn='urn:it.cnr.ismar.ve:station:onda'

# <codecell>

attributes={'units':'m'}

# <codecell>

create.create_timeseries_file(output_directory='/usgs/data2/notebook/data',
                              latitude=41.5,
                              longitude=-69.1,
                              full_station_urn=station_urn,
                              full_sensor_urn=sensor_urn,
                              sensor_vertical_datum=0.0,
                              times=times,
                              verticals=z, 
                              values=values,
                              attributes=attributes,
                              global_attributes={},
                              output_filename='wave_data.nc')

# <codecell>


