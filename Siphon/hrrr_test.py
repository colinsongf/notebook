# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import matplotlib.pyplot as plt
import numpy as np
%matplotlib inline

# <headingcell level=2>

# Extract HRRR data using Unidata's Siphon package

# <codecell>

# Resolve the latest HRRR dataset
from siphon.catalog import TDSCatalog
latest_hrrr = TDSCatalog('http://thredds-jumbo.unidata.ucar.edu/thredds/catalog/grib/HRRR/CONUS_3km/surface/latest.xml')
hrrr_ds = list(latest_hrrr.datasets.values())[0]

# Set up access via NCSS
from siphon.ncss import NCSS
ncss = NCSS(hrrr_ds.access_urls['NetcdfSubset'])

# Create a query to ask for all times in netcdf4 format for
# the Temperature_surface variable, with a bounding box
query = ncss.query()

# <codecell>

query.all_times().accept('netcdf4').variables('Temperature_surface')
query.lonlat_box(45, 41., -63, -71.5)

# Get the raw bytes and write to a file.
data = ncss.get_data_raw(query)
with open('test.nc', 'wb') as outf:
    outf.write(data)

# <headingcell level=2>

# Try reading extracted data with Iris

# <codecell>

import iris
cubes = iris.load('test.nc')
cubes

# <codecell>

cubes[0].coords()

# <codecell>

import iris.quickplot as qplt
qplt.contourf(cubes[0][0,:,:])

# <headingcell level=2>

# Try reading extracted data with Xray

# <codecell>

import xray

# <codecell>

nc = xray.open_dataset('test.nc')

# <codecell>

nc

# <codecell>

ncvar = nc['Temperature_surface']
ncvar

# <headingcell level=2>

# Try plotting the LambertConformal data with Cartopy

# <codecell>

import cartopy
import cartopy.crs as ccrs

# <codecell>

# I got these values from the netCDF file
crs = ccrs.LambertConformal(central_longitude=262.5, central_latitude=38.5)

# <codecell>

print(ncvar.x.data.shape)
print(ncvar.y.data.shape)
print(ncvar.data.shape)

# <codecell>

fig = plt.figure(figsize=(12,8))
ax = plt.axes(projection=ccrs.PlateCarree())
ax.pcolormesh(ncvar.x.data,ncvar.y.data,ncvar[0,:,:].data, transform=crs,zorder=0)
ax.coastlines(resolution='10m',color='black',zorder=1)
ax.gridlines(draw_labels=True);

# <codecell>

crs2 = ccrs.PlateCarree()
x,y = np.meshgrid(ncvar.x.data, ncvar.y.data)
a = crs2.transform_points(crs,x,y)
print(a.shape)

# <codecell>

fig = plt.figure(figsize=(12,8))
ax = plt.axes(projection=ccrs.PlateCarree())
ax.pcolormesh(a[:,:,0],a[:,:,1],ncvar[0,:,:].data, transform=crs,zorder=0)
ax.coastlines(resolution='10m',color='black',zorder=1)
ax.gridlines(draw_labels=True);

# <codecell>


