##==============================================================================
## Created on: 15/03/2017
## Created By: Douglas Finch
## Python 2.7
## Get a rough estimation of global CH4 emissions
##==============================================================================
import numpy as np
import scipy.io as io
from datetime import datetime
import datetime as dt
from ch4_initial_flux_plots import get_fluxes
import math
from geopy import distance
import grid_area
##==============================================================================

def annual_sum_emissions(source = 'total'):
    flux, lat, lon, dates = get_fluxes(source)
    secs_in_year = 365 * 24 * 60 * 60 # Assumes not leap year
    global_surface = 5.101e14 # m^2

    gridbox_area = grid_area.area(lat,lon)

    print "*" * 80
    print "*** %s ***" % source
    print "*" * 80

    daily_emiss = np.zeros(flux.shape)

    for d in range(flux.shape[0]):
        daily_emiss[d,:,:] = flux[d,:,:] * gridbox_area * 24 * 60 * 60

    # mean_flux = np.mean(flux) # Get the mean flux of the whole year and whole global
    # print "The %s global mean flux is %r kg/m2/s" % (source, mean_flux)
    # year_flux = np.mean(flux,axis=(0)) * secs_in_year # kg / m2 / year
    # print "The mean yearly flux is %r kg/m2." % np.mean(year_flux)
    # emiss_per_box = year_flux * gridbox_area
    # # emiss = mean_flux * secs_in_year * global_surface # kg of CH4
    # # print "The %s CH4 emissions for one year are %r Tg." % (source, emiss / 1e9)
    # print "The %s CH4 emissions for one year are %r Tg." % (source, np.sum(emiss_per_box) / 1e9)

    print "The %s CH4 emissions for one year are %r Tg." % (source, np.sum(daily_emiss) / 1e9)

    pass

if __name__ == '__main__':
    sources = ['Agricultural','anthro','biomass','energy',
                'Industrial','ocean','other','soil','termite',
                'volcano','Waste','wetlands','total']

    for ss in sources:
        annual_sum_emissions(ss)


## =============================================================================
## END OF PROGRAM
## =============================================================================
