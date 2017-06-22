##
##==============================================================================
##Created on: 26/1/2015
##Created By: Douglas Finch
##Python 2.7
## Get timeseries of CO at certain place
##==============================================================================
import geos_info
import tau_mod
import csv
import bpch
import os
import calendar
import glob
##==============================================================================

years = range(2014,2015)
years = [str(i) for i in years]
months = range(1,13)
months = [str(i).zfill(2) for i in months]

station_names= ['macehead','tacolneston']

class station_info(object):
    def __init__(self, station_name):
        self.station_name = station_name
        self.get_latitude()
        self.get_longitude()

    def get_latitude(self):
        station_name = self.station_name
        if station_name.lower() == 'macehead':
            self.latitude = 53.326
        elif station_name.lower() == 'tacolneston':
            self.latitude = 52.518

        return self

    def get_longitude(self):
        station_name = self.station_name
        if station_name.lower() == 'macehead':
            self.longitude = -9.899
        elif station_name.lower() == 'tacolneston':
            self.longitude = 1.139

        return self

## =============================================================================
## END OF PROGRAM
## =============================================================================
