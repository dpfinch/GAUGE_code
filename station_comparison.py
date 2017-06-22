##==============================================================================
## Created on: 22/06/2017
## Created By: Douglas Finch
## Python 2.7
## Compare NOAA station data for Ch4 against GEOS-Chem Methane
##==============================================================================
import numpy as np
import scipy.io as io
from datetime import datetime
import datetime as dt
from matplotlib import pyplot as plt
from mpl_toolkits.basemap import Basemap
import geos_info
import brewer2mpl
import sys
import os.path
##==============================================================================

def NOAA_flask_data(station):
    if station.lower() == 'macehead':
        station = 'MHD'
    elif station.lower() == 'tacolneston':
        station = 'TAC'

    if station != 'TAC' and station != 'MHD':
        print "No data for %s" % station
        sys.exit()

    dirc = '/home/dfinch/Documents/CH4/NOAA_station_data/'

    fi = '%s%s_DISCRETE_CH4.dat' % (dirc, station)

    if os.path.isfile(fi):
        print "Opening file: %s" % fi
    else:
        print "No file named: %s" % fi
        sys.exit()

    # This uses the assumption that the NOAA station data files have
    # comments at the beginning of the file commented with a '#'
    # This seems to hold true for all there station data files
    all_raw_data = np.loadtxt(fi,dtype=str, comments = '#')

    sample_dates = []
    ch4_value = []

    for x in range(all_raw_data.shape[0]):
        year = int(all_raw_data[x,1])
        month = int(all_raw_data[x,2])
        day = int(all_raw_data[x,3])
        hour = int(all_raw_data[x,4])
        minute = int(all_raw_data[x,5])
        sample_dates.append(datetime(year,month,day,hour,minute))

        ch4_value.append(float(all_raw_data[x,11]))

    return sample_dates, ch4_value

def simple_plot(dates,data):

    pass

## =============================================================================
## END OF PROGRAM
## =============================================================================
