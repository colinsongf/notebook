# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <headingcell level=1>

# Using Iris to access data from US-IOOS models

# <codecell>

from IPython.display import HTML
HTML('<iframe src=http://scitools.org.uk/iris/ width=800 height=350></iframe>')

# <codecell>

import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
import time
import numpy.ma as ma

import iris
%matplotlib inline

# <codecell>

def time_near(cube,start):
    #    coord_names = [coord.name() for coord in cube.coords()]
    #    timevar = cube.coord(coord_names[0]))
    timevar=cube.coord('time')
    try:
        itime = timevar.nearest_neighbour_index(timevar.units.date2num(start))
    except:
        itime = -1
    return timevar.points[itime]

# <codecell>

def var_lev_date(url=None,var=None,mytime=None,lev=0,subsample=1):
    time0= time.time()
    cube = iris.load(url,iris.Constraint(name=var.strip()))[0]
#    cube = iris.load(url,var)[0]
#    print cube.coord('time')

    try:
        cube.coord(axis='T').rename('time')
    except:
        pass
    slice = cube.extract(iris.Constraint(time=time_near(cube,mytime)))
    slice = slice[lev,::subsample,::subsample]  
    print 'slice retrieved in %f seconds' % (time.time()-time0)
    return slice

# <codecell>

def myplot(myslice,model=None):
    # make the plot
    plt.figure(figsize=(12,8))
    lat=myslice.coord(axis='Y').points
    lon=myslice.coord(axis='X').points
    time=myslice.coord('time')[0]
    plt.subplot(111,aspect=(1.0/np.cos(lat.mean()*np.pi/180.0)))
    plt.pcolormesh(lon,lat,ma.masked_invalid(myslice.data));
    plt.colorbar()
    plt.grid()
    date=time.units.num2date(time.points)
    date_str=date[0].strftime('%Y-%m-%d %H:%M:%S %Z')
    plt.title('%s: %s: %s' % (model,myslice.long_name,date_str));

# <codecell>

# use contraints to select nearest time
#mytime=dt.datetime(2008,7,28,12)  #specified time...
mytime=dt.datetime.utcnow()      # .... or now

# <codecell>

model='USGS/COAWST'
url='http://geoport.whoi.edu/thredds/dodsC/coawst_4/use/fmrc/coawst_4_use_best.ncd'
var='sea_water_potential_temperature'
lev=-1
slice=var_lev_date(url=url,var=var, mytime=mytime, lev=lev, subsample=1)
myplot(slice,model=model)

# <codecell>

model='MARACOOS/ESPRESSO'
url='http://tds.marine.rutgers.edu/thredds/dodsC/roms/espresso/2013_da/his_Best/ESPRESSO_Real-Time_v2_History_Best_Available_best.ncd'
var='sea_water_potential_temperature'
lev=-1
slice=var_lev_date(url=url,var=var, mytime=mytime, lev=lev)
myplot(slice,model=model)

# <codecell>

model='SECOORA/NCSU'
url='http://omgsrv1.meas.ncsu.edu:8080/thredds/dodsC/fmrc/sabgom/SABGOM_Forecast_Model_Run_Collection_best.ncd'
var='sea_water_potential_temperature'
lev=-1
slice=var_lev_date(url=url,var=var, mytime=mytime, lev=lev)
myplot(slice,model=model)

# <codecell>

model='CENCOOS/UCSC'
url='http://oceanmodeling.pmc.ucsc.edu:8080/thredds/dodsC/ccsnrt/fmrc/CCSNRT_Aggregation_best.ncd'
var='potential temperature'
lev=-1
slice=var_lev_date(url=url,var=var, mytime=mytime, lev=lev)
myplot(slice,model=model)

# <codecell>

model='HIOOS'
url='http://oos.soest.hawaii.edu/thredds/dodsC/hioos/roms_assim/hiig/ROMS_Hawaii_Regional_Ocean_Model_Assimilation_best.ncd'
var='sea_water_potential_temperature'
lev=1
slice=var_lev_date(url=url,var=var, mytime=mytime, lev=lev)
myplot(slice,model=model)

# <codecell>

model='Global RTOFS/NCEP'
url='http://ecowatch.ncddc.noaa.gov/thredds/dodsC/hycom/hycom_reg1_agg/HYCOM_Region_1_Aggregation_best.ncd'
var='sea_water_temperature'  
lev=0
subsample=1
slice=var_lev_date(url=url,var=var, mytime=mytime, lev=lev, subsample=subsample)
myplot(slice,model=model)

# <codecell>

print slice

# <codecell>

model='MARACOOS/ESPRESSO'
url='http://tds.marine.rutgers.edu/thredds/dodsC/roms/espresso/2013_da/his_Best/ESPRESSO_Real-Time_v2_History_Best_Available_best.ncd'
cubes=iris.load(url)

# <codecell>

var='potential temperature'
cube = iris.load(url,iris.Constraint(name=var.strip()))

# <codecell>

cubes = iris.load(url)

# <codecell>

len(cube)

# <codecell>


