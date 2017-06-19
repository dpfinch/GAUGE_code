##==============================================================================
## Created on: 15/03/2017
## Created By: Douglas Finch
## Python 2.7
## Gather all CH4 flux information and combine into one file
##==============================================================================
import numpy as np
import scipy.io as io
from datetime import datetime
import calendar
import datetime as dt
import total_ch4_flux
import grid_area
##==============================================================================

def all_anthro_flux():
    lat, lon = coords('anthro')
    dates = total_ch4_flux.get_anthro_dates()
    x = len(lat)
    y = len(lon)
    d = len(dates)

    total_anthro_flux = np.zeros([d,x,y])

    emiss_types = ['Agricultural','Energy','Industrial',
                            'Other','Waste']

    for et in emiss_types:
            total_anthro_flux += total_ch4_flux.get_anthro_emiss(et)

    return total_anthro_flux

def coords(emtype = 'biomass'):
    other_sources = ['termite','volcano','ocean','hydr']
    emtype = emtype.lower()
    dirc_name = '/home/dfinch/Documents/CH4/emissions/'
    if emtype == 'biomass':
        full_name = '%sCH4_flux_biomass_global_1997_2011.nc' % dirc_name
    elif emtype == 'anthro':
        full_name = '%sCH4_flux_anthro_ft2010_%s_global_2000_2010.nc' % (dirc_name,'Energy')
    elif emtype == 'wetlands':
        full_name = '%sCH4_flux_wetlands_rice_global_2003_2009.nc' % dirc_name
    elif emtype in other_sources:
        full_name = '%sCH4_flux_natural_global_climatology.nc' % dirc_name
    elif emtype == 'soil':
        full_name = '%sCH4_flux_soilssink_global_climatology.nc' % dirc_name
    else:
        print "Unknown emissions type '%s'" % emtype
        import sys
        sys.exit()
    file_vari = total_ch4_flux.get_variables(full_name)
    lat = file_vari.variables['latitude']
    lon = file_vari.variables['longitude']
    return lat.data, lon.data


def get_soil_sink():
    dirc_name = '/home/dfinch/Documents/CH4/emissions/'
    full_name = '%sCH4_flux_soilssink_global_climatology.nc' % dirc_name
    file_vari = total_ch4_flux.get_variables(full_name)
    lat = file_vari.variables['latitude']
    lon = file_vari.variables['longitude']
    soils = file_vari.variables['SOILS']

    return soils.data

def other_flux_sources(flux_type = 'ocean'):
    if flux_type == 'volcano':
        flux_file_name = 'VOLC'
    else:
        flux_file_name = flux_type.upper()

    dirc_name = '/home/dfinch/Documents/CH4/emissions/'
    full_name = '%sCH4_flux_natural_global_climatology.nc' % dirc_name
    file_vari = total_ch4_flux.get_variables(full_name)
    natural_flux = file_vari.variables[flux_file_name]

    return natural_flux.data

def get_flux(flux_name):
    if flux_name == 'anthro':
        return all_anthro_flux()
    if flux_name == 'biomass':
        return total_ch4_flux.get_biomass_flux()
    if flux_name == 'wetlands':
        return total_ch4_flux.get_wetland_flux()
    if flux_name == 'soil':
        return get_soil_sink()
    else:
        return other_flux_sources(flux_name)

def regrid(in_flux,flux_name):
    # Try and regrid everything to a 0.5 x 0.5 degree grid
    # This is purely fitting squares inside squares. Since its a flux
    # we don't have to worry about mass conservation (I think)
    # For the time being - keep the temporal resolution - we'll deal with that
    # later
    # Turn out we have to worry about the fact that different lat lon squares will
    # weight the mean differently and therefore give a wrong answer.
    orig_lat,orig_lon = coords(flux_name)
    orig_area  = grid_area.area(orig_lat,orig_lon)

    new_lat = np.linspace(-89.75,89.75,360)
    new_lon = np.linspace(-179.75,179.75,720)
    new_area = grid_area.area(new_lat,new_lon)

    old_shape = in_flux.shape
    out_flux = np.zeros([old_shape[0],len(new_lat),len(new_lon)])
    # print "Regridding from %r to %r" % (old_shape, out_flux.shape)
    # This is only really going to work if everything fits nicely
    lat_factor = float(len(orig_lat)) / len(new_lat)
    lon_factor = float(len(orig_lon)) / len(new_lon)

    # Convert from kg/m2/s to kg/gridbox/s
    grid_flux = in_flux * orig_area
    secs_in_year = 365 * 24 * 60 * 60
    # A check to see if we've kept a similarish emission mass
    annual_grid = grid_flux[-1,:,:] * secs_in_year
    orig_total = np.sum(annual_grid)

    # Lets assume both lat factor and lon factor are both either above or
    # below one. If one is and one isn't then we're buggered.
    # If lat factor is more than one we're going from a higher resolution to a lower
    if lat_factor > 1:
        lat_factor = int(lat_factor)
        lon_factor = int(lon_factor)
        n1, n2 = 0, lat_factor
        for x in range(len(new_lat)):
            m1, m2 = 0, lon_factor
            for y in range(len(new_lon)):
                for z in range(old_shape[0]):
                    out_flux[z,x,y] = np.sum(grid_flux[z,n1:n2,m1:m2])
                m1 += lon_factor
                m2 += lon_factor
            n1 += lat_factor
            n2 += lat_factor

    # If lat_factor is less than one we're going from a lower resolution to a higher
    if lat_factor < 1:
        # Make the lat lon factors inverse
        lat_factor = int(1 / lat_factor)
        lon_factor = int(1 / lon_factor)
        n1, n2 = 0, lat_factor
        for x in range(len(orig_lat)):
            m1, m2 = 0, lon_factor
            for y in range(len(orig_lon)):
                for z in range(old_shape[0]):
                    out_flux[z,n1:n2,m1:m2] = grid_flux[z,x,y] / (lat_factor * lon_factor)
                m1 += lon_factor
                m2 += lon_factor
            n1 += lat_factor
            n2 += lat_factor

    if lat_factor == 1:
        out_flux = grid_flux

    # convert back to kg/m2/s
    out_grid_flux = out_flux / new_area

    # Test if Kg of CH4 are the same (or reasonably close)
    new_annual_total = out_flux[-1,:,:] * secs_in_year
    new_total = np.sum(new_annual_total)

    # print flux_name, orig_total, new_total, new_total - orig_total

    return out_grid_flux

def wetlands_mean(raw_flux):
    # Make a climatology from wetlands before hand to reduce number of days
    # This makes the regridding a lot quicker
    # Remove leap years first then makes things a bit easier
    dates = total_ch4_flux.get_wetland_dates()
    leap_index = []
    for n,d in enumerate(dates):
        if d.month == 2 and d.day == 29:
            leap_index.append(n)

    trim_flux = np.delete(raw_flux,leap_index,axis = 0)

    year_flux = np.zeros([365,raw_flux.shape[1],raw_flux.shape[2]])
    for num_day in range(365):
        year_flux[num_day,:,:] = np.mean(raw_flux[num_day::365],axis = 0)

    return year_flux

def time_regrid(in_flux,flux_name):
    # Take whatever time step the raw emissions were at then process
    # them to be daily - this will just be means spread out so nothing
    # crazy fancy
    out_array = np.zeros([365,360,720]) # Currently hard-coded for ease
    # print in_flux.shape
    old_shape = in_flux.shape
    if old_shape == out_array.shape:
        out_array = in_flux
        return out_array

    # Lukily nothing is less than a day so slightly simpler
    # Anthro just using latest year and one value for all days
    if flux_name == 'anthro':
        out_array[:,:,:] = in_flux[-1,:,:]
        return out_array

    # Now the only emissions that is more than one year
    if flux_name == 'biomass':
            bb_dates = total_ch4_flux.get_biomass_dates()
            bb_climatology = np.zeros([12,in_flux.shape[1],in_flux.shape[2]])
            for mon in range(12):
                bb_climatology[mon,:,:] = np.mean(in_flux[mon::12,:,:],axis = 0)
            in_flux = bb_climatology

    # Everything should be monthly average fluxes now and be 12x36x720
    day_of_year = 0
    for m in range(12):
        days_in_month = calendar.monthrange(2013,m + 1)[1]
        out_array[day_of_year:day_of_year + days_in_month] = in_flux[m,:,:]
        day_of_year += days_in_month

    return out_array

def write_flux_to_disk(flux, flux_name):

    latitude =  np.linspace(-89.75,89.75,360)
    longitude = np.linspace(-179.75,179.75,720)
    st_date = datetime(2013,01,01)
    dates = [st_date + dt.timedelta(days=x) for x in range(365)]
    dates_str = [y.strftime('%Y%m%d') for y in dates]

    out_dirc = '/home/dfinch/Documents/CH4/emissions/regridded_emissions/'
    out_filename = '%sGlobal_CH4_flux_daily_05x05_%s.nc' % (out_dirc, flux_name.upper())

    nc_file = io.netcdf_file(out_filename,'w')

    nc_file.createDimension('latitude',len(latitude))
    nc_file.createDimension('longitude',len(longitude))
    nc_file.createDimension('date',len(dates))

    lons_out = nc_file.createVariable('longitude','f4',('longitude',))
    lats_out = nc_file.createVariable('latitude','f4',('latitude',))
    date_out = nc_file.createVariable('date','i',('date',))
    flux_out = nc_file.createVariable('CH4_Flux','f8',('date','latitude','longitude',))

    lats_out.units = 'Degrees North'
    lons_out.units = 'Degrees East'
    date_out.units = 'Date YYYYMMDD'
    flux_out.units = 'kg m-2 s-1'

    lats_out[:] = latitude
    lons_out[:] = longitude
    date_out[:] = dates_str
    flux_out[:] = flux

    nc_file.flush()
    nc_file.close()

    print "Written %s" % out_filename
    pass

def all_fluxes():
    flux_names = ['anthro','biomass','wetlands','soil',
                    'ocean','termite','volcano']

    total_global_flux = np.zeros([365,360,720])

    for fn in flux_names:
        raw_flux = get_flux(fn)
        if fn == 'wetlands':
            raw_flux = wetlands_mean(raw_flux)
        regridded = regrid(raw_flux,fn)
        new_time_flux = time_regrid(regridded,fn)
        # print "%s flux has %r shape" % (fn,new_time_flux.shape)
        total_global_flux += new_time_flux
        write_flux_to_disk(new_time_flux,fn)

    write_flux_to_disk(total_global_flux,'total')
    pass

def anthro_split_fluxes():

    emiss_types = ['Agricultural','Energy','Industrial',
                            'Other','Waste']

    fn = 'anthro'

    for flux_type in emiss_types:
        flux = total_ch4_flux.get_anthro_emiss(flux_type)

        regridded = regrid(flux,fn)
        new_time_flux = time_regrid(regridded,fn)
        write_flux_to_disk(new_time_flux,flux_type)

if __name__ == '__main__':
    all_fluxes()
    anthro_split_fluxes()

## =============================================================================
## END OF PROGRAM
## =============================================================================
