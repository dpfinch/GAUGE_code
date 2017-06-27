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
import grid_area
import brewer2mpl
import sys
import os.path
##==============================================================================

def NOAA_flask_data(station, meas_type='MONTHLY'):
    if station.lower() == 'macehead':
        station = 'MHD'
    elif station.lower() == 'tacolneston':
        station = 'TAC'

    if station != 'TAC' and station != 'MHD':
        print "No data for %s" % station
        sys.exit()

    dirc = '/home/dfinch/Documents/CH4/NOAA_station_data/'

    fi = '%s%s_%s_CH4.dat' % (dirc, station, meas_type.upper())

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

    if meas_type == 'DISCRETE':
        for x in range(all_raw_data.shape[0]):
            year = int(all_raw_data[x,1])
            month = int(all_raw_data[x,2])
            day = int(all_raw_data[x,3])
            hour = int(all_raw_data[x,4])
            minute = int(all_raw_data[x,5])
            sample_dates.append(datetime(year,month,day,hour,minute))

            ch4_value.append(float(all_raw_data[x,11]))

    # As these are monthly means we'll set the date as the middle of the month
    elif meas_type == 'MONTHLY':
        for x in range(all_raw_data.shape[0]):
            year = int(all_raw_data[x,1])
            month = int(all_raw_data[x,2])
            day = 15
            hour = 12
            minute = 30
            sample_dates.append(datetime(year,month,day,hour,minute))

            ch4_value.append(float(all_raw_data[x,3]))

    return sample_dates, ch4_value

def GC_station_data(station):
    if station.lower() == 'mhd':
        station = 'macehead'
    elif station.lower() == 'tac':
        station = 'tacolneston'

    if station != 'macehead' and station != 'tacolneston':
        print "No data for %s" % station
        sys.exit()

    dirc = '/home/dfinch/Documents/CH4/GC_station_data/'

    fi = '%s%s_CH4_GEOS-Chem_%s.csv' % (dirc, station, '025x03125')

    if os.path.isfile(fi):
        print "Opening file: %s" % fi
    else:
        print "No file named: %s" % fi
        sys.exit()

    raw_data = np.loadtxt(fi, delimiter = ',')

    dates = []
    ch4_value = []

    for x in range(raw_data.shape[0]):
        year = int(raw_data[x,0])
        month = int(raw_data[x,1])
        day = int(raw_data[x,2])
        hour = int(raw_data[x,3])
        minute = int(raw_data[x,4])
        dates.append(datetime(year,month,day,hour,minute))

        ch4_value.append(float(raw_data[x,5]))

    return dates, ch4_value

def GC_4x5_data(station = 'MHD'):
    import gchem
    dirc = '/home/dfinch/Documents/CH4/model_output/4x5/'
    fname = '%sctm_4x5.bpch' % dirc

    gr = gchem.bpch.open_file(fname)
    ch4 = gr.filter(category = 'IJ-AVG-$')

    if station == 'MHD':
        longitude = -9.899
        latitude = 53.326
    if station == 'TAC':
        longitude = 1.139
        latitude = 52.518
    else:
        print "Station %s not known." % station
        sys.exit()

    model_lat = grid_area.get_model_lat(model_res='4x5')
    model_lon = grid_area.get_model_lon(model_res='4x5')

    station_lon=min(range(len(model_lon)), key=lambda i: abs(model_lon[i]-latitude))
    station_lat=min(range(len(model_lat)), key=lambda i: abs(model_lat[i]-longitude))

    # Start empty array to append dates and ch4 conc

    for m in range(len(ch4)):
        monthly_ch4 = ch4[m].value[station_lon,station_lat,0]
        monthly_date = ch4[m].times[0]

    # Sort the data into chronological order
    ch4_station = [y for y, x in sorted(zip(monthly_date, monthly_ch4))]
    monthly_date.sort()

    return monthly_date, ch4_station
    

def simple_plot(station = 'MHD'):
    noaa_dates, noaa_ch4 = NOAA_flask_data(station, meas_type = 'DISCRETE')
    gc_dates, gc_ch4 = GC_station_data(station, meas_type = 'DISCRETE')

    plt.plot(noaa_dates, noaa_ch4, color='blue', label='NOAA Flask')
    plt.plot(gc_dates, gc_ch4, color='green', label = 'GEOS-Chem CH$_4$')

    plt.xlabel('Date')
    plt.ylabel('CH$_4$ (ppb)')

    plt.legend()
    plt.show()

    pass

def measurement_compare(station = 'MHD'):
    monthly_dates, monthly_ch4 = NOAA_flask_data(station, meas_type = 'MONTHLY')

    discrete_dates, discrete_ch4 = NOAA_flask_data(station, meas_type = 'DISCRETE')

    plt.plot(discrete_dates, discrete_ch4, color='grey', label = 'Discrete Observations')
    plt.plot(monthly_dates, monthly_ch4, color='blue', label = 'Monthly Average Observations')

    plt.xlabel('Date')
    plt.ylabel('CH$_4$ (ppb)')
    plt.legend()
    plt.show()
    pass

if __name__ == '__main__':
    # simple_plot()
    measurement_compare()

## =============================================================================
## END OF PROGRAM
## =============================================================================
