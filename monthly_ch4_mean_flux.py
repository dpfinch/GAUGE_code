##==============================================================================
## Created on: 06/04/2017
## Created By: Douglas Finch
## Python 2.7
## Take daily CH4 fluxes and make monthly mean netcdf
## Also regrid to 4x5
##==============================================================================
import numpy as np
import scipy.io as io
from datetime import datetime
import calendar
import datetime as dt
##==============================================================================
dirc = '/home/dfinch/Documents/CH4/emissions/regridded_emissions/'
orig_file = '%sGlobal_CH4_flux_daily_05x05_TOTAL.nc' % dirc
new_file = '%sGlobal_CH4_flux_monthly_4x5_TOTAL.nc' % dirc

open_f = io.netcdf_file(orig_file)
lat = open_f.variables['latitude'].data
lon = open_f.variables['longitude'].data
flux = open_f.variables['CH4_Flux'].data

month_grid = np.zeros[12,flux.shape[1],flux.shape[2]]
total_days = 0
for m in range(12):
    month_len = calendar.monthrange(2013,m+1)[1]
    month_grid[m,:,:] = np.mean(flux[total_days:total_days+month_len,:,:],axis = 0)

new_lat = np.arange(-90,94,4)
new_lat[0] = -88.
new_lat[-1] = 88
new_lon = np.arange(-177.5,178.5,5)
course_grid = np.zeros([12,len(new_lat),len(new_lon)])




## =============================================================================
## END OF PROGRAM
## =============================================================================
