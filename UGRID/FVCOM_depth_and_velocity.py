
# coding: utf-8

# # Access data from the NECOFS (New England Coastal Ocean Forecast System) via OPeNDAP

# Demonstration using the NetCDF4-Python library to access velocity data from a triangular grid ocean model (FVCOM) via OPeNDAP, specifying the desired URL, time, layer and lat/lon region of interest.  The resulting plot of forecast velocity vectors over color-shaded bathymetry is useful for a variety of recreational and scientific purposes. 
# 
# NECOFS (Northeastern Coastal Ocean Forecast System) is run by groups at the University of Massachusetts Dartmouth and the Woods Hole Oceanographic Institution, led by Drs. C. Chen, R. C. Beardsley, G. Cowles and B. Rothschild. Funding is provided to run the model by the NOAA-led Integrated Ocean Observing System and the State of Massachusetts.
# 
# NECOFS is a coupled numerical model that uses nested weather models, a coastal ocean circulation model, and a wave model. The ocean model is a volume-mesh model with horizontal resolution that is finer in complicated regions. It is layered (not depth-averaged) and includes the effects of tides, winds, and varying water densities caused by temperature and salinity changes.
# 
# * Model description: http://fvcom.smast.umassd.edu/research_projects/NECOFS/model_system.html
# * THREDDS server with other forecast and archive products: http://www.smast.umassd.edu:8080/thredds/catalog.html

# In[1]:

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.tri as Tri
import netCDF4
import datetime as dt
get_ipython().magic('matplotlib inline')


# In[2]:

# DAP Data URL
# MassBay GRID
url = 'http://www.smast.umassd.edu:8080/thredds/dodsC/FVCOM/NECOFS/Forecasts/NECOFS_FVCOM_OCEAN_MASSBAY_FORECAST.nc'
# GOM3 GRID
#url='http://www.smast.umassd.edu:8080/thredds/dodsC/FVCOM/NECOFS/Forecasts/NECOFS_GOM3_FORECAST.nc'
# Open DAP
nc = netCDF4.Dataset(url)
ncv = nc.variables
ncv.keys()


# In[4]:

# take a look at the "metadata" for the variable "u"
print(ncv['u'])


# In[5]:

ncv['temp'].shape


# In[6]:

ncv['nv'].shape


# In[7]:

# Desired time for snapshot
# ....right now (or some number of hours from now) ...
start = dt.datetime.utcnow() + dt.timedelta(hours=+4)
# ... or specific time (UTC)
#start = dt.datetime(2013,3,2,15,0,0)


# In[9]:

# Get desired time step  
time_var = ncv['time']
itime = netCDF4.date2index(start,time_var,select='nearest')

# Get lon,lat coordinates for nodes (depth)
lat = ncv['lat'][:]
lon = ncv['lon'][:]
# Get lon,lat coordinates for cell centers (depth)
latc = ncv['latc'][:]
lonc = ncv['lonc'][:]
# Get Connectivity array
nv = ncv['nv'][:].T - 1 
# Get depth
h = ncv['h'][:]  # depth 


# In[10]:

tm = netCDF4.num2date(time_var[itime],time_var.units)
daystr = tm.strftime('%Y-%b-%d %H:%M')
print(daystr)


# In[12]:

# round to nearest 10 minutes to make titles look better
tm += dt.timedelta(minutes=5)
tm -= dt.timedelta(minutes=tm.minute % 10,
                         seconds=tm.second,
                         microseconds=tm.microsecond)
daystr = tm.strftime('%Y-%b-%d %H:%M')
print(daystr)


# In[13]:

tri = Tri.Triangulation(lon,lat, triangles=nv)


# In[14]:

# get current at layer [0 = surface, -1 = bottom]
ilayer = 0
u = ncv['u'][itime, ilayer, :]
v = ncv['v'][itime, ilayer, :]


# In[15]:

#boston harbor
levels=np.arange(-34,2,1)   # depth contours to plot
ax= [-70.97, -70.82, 42.25, 42.35] # 
maxvel = 0.5
subsample = 3


# In[16]:

#woods hole
levels=np.arange(-30,2,1)
ax = [-70.7, -70.6, 41.48, 41.55]
ax = [-70.75, -70.6, 41.48, 41.56]
maxvel = 1.0
subsample = 2


# In[17]:

# find velocity points in bounding box
ind = np.argwhere((lonc >= ax[0]) & (lonc <= ax[1]) & (latc >= ax[2]) & (latc <= ax[3]))


# In[18]:

np.random.shuffle(ind)
Nvec = int(len(ind) / subsample)
idv = ind[:Nvec]


# In[19]:

# tricontourf plot of water depth with vectors on top
fig=plt.figure(figsize=(18,10))
plt.subplot(111,aspect=(1.0/np.cos(lat.mean()*np.pi/180.0)))
plt.tricontourf(tri, -h,levels=levels,shading='faceted',cmap=plt.cm.gist_earth)
plt.axis(ax)
plt.gca().patch.set_facecolor('0.5')
cbar = plt.colorbar()
cbar.set_label('Water Depth (m)', rotation=-90)
Q = plt.quiver(lonc[idv],latc[idv],u[idv],v[idv],scale=20)
maxstr='%3.1f m/s' % maxvel
qk = plt.quiverkey(Q,0.92,0.08,maxvel,maxstr,labelpos='W')
plt.title('NECOFS Velocity, Layer %d, %s UTC' % (ilayer, daystr));


# In[20]:

nc.filepath()


# In[21]:

nc.get_variables_by_attributes(standard_name='sea_water_salinity')


# In[ ]:



