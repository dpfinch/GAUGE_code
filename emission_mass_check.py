##==============================================================================
## Created on: 15/03/2017
## Created By: Douglas Finch
## Python 2.7
## Get the annual emissions (Tg/year) from the initial flux files to see what
## they are and if they match what I think they should be
##==============================================================================
import numpy as np
import grid_area
from total_ch4_flux_map import get_flux, coords
import total_ch4_flux
import calendar
##==============================================================================

def get_raw_emiss(source = 'anthro'):

    if source != 'Agricultural':
        raw_flux = get_flux(source)
        lat, lon = coords(source)
        area = grid_area.area(lat,lon)

    if source == 'anthro':
        flux = raw_flux[-1,:,:]

        num_secs = 365 * 24 * 60 * 60
        annual_emiss = flux * num_secs * area

    if source == 'Agricultural':

        lat, lon = coords('anthro')
        area = grid_area.area(lat,lon)
        raw_flux = total_ch4_flux.get_anthro_emiss(source)
        flux = raw_flux[-1,:,:]

        num_secs = 365 * 24 * 60 * 60
        annual_emiss = flux * num_secs * area

    if source == 'biomass':
        bb_dates = total_ch4_flux.get_biomass_dates()
        bb_climatology = np.zeros([12,raw_flux.shape[1],raw_flux.shape[2]])
        num_days_in_month = []
        for mon in range(12):
            num_days_in_month.append(calendar.monthrange(2013,mon+1)[1])
            bb_climatology[mon,:,:] = np.mean(raw_flux[mon::12,:,:],axis = 0)
        flux = bb_climatology

        for n,m in enumerate(num_days_in_month):
            num_secs = m * 24 * 60 * 60
            flux[n,:,:] = flux[n,:,:] * area * num_secs

        annual_emiss = flux

    if source == 'wetlands':
        flux = raw_flux[-366:-1,:,:]
        emiss_grid = np.zeros(flux.shape)
        for x in range(365):
            emiss_grid[x,:,:] = flux[x,:,:] * area * 24 * 60 * 60

        annual_emiss = emiss_grid


    print "Total for %s is: %r kg" % (source, np.sum(annual_emiss))

    pass

if __name__ == '__main__':
    get_raw_emiss(source = 'Agricultural')

## =============================================================================
## END OF PROGRAM
## =============================================================================
