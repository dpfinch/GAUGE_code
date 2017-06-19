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
import ch4_initial_flux_plots as get_fluxes
import grid_area
import sys
import os.path
import gp_axis as gax
##==============================================================================

def regrid_4x5(infile = 0):
    if infile == 0:
        print "No source entered"
        sys.exit()


    orig_flux, orig_lat, orig_lon, orig_dates = get_fluxes.get_fluxes(infile)
    orig_area = grid_area.area(orig_lat,orig_lon)

    grid_flux = orig_flux * orig_area

    # Can't use the GEOS-Chem normal grid because its not regular for a reason
    # only known to the Gods.
    new_lat = grid_area.get_model_lat('4x5')
    new_lon = grid_area.get_model_lon('4x5')
    new_area = grid_area.area(new_lat,new_lon)
    out_flux = np.zeros([len(orig_dates),len(new_lat),len(new_lon)])

    lat_edges = grid_area.get_model_lat_edge('4x5')
    lon_edges = grid_area.get_model_lon_edge('4x5')

    # Takes a 0.5x0.5 degree resolution to a coarser res
    n1 = 0
    for n,x in enumerate(lat_edges):
        if n == len(lat_edges) -1 :
            continue
        grid_diff_lat = int(lat_edges[n+1] - x)
        boxes_into_lat = int(grid_diff_lat / 0.5)
        m1 = 0
        for m, y in enumerate(lon_edges):
            if m == len(lon_edges) -1 :
                continue
            grid_diff_lon = int(lon_edges[m+1] - y)
            boxes_into_lon = int(grid_diff_lon / 0.5)
            for z in range(len(orig_dates)):
                out_flux[z,n,m] = np.sum(grid_flux[z,n1:(n1+boxes_into_lat),m1:(m1+boxes_into_lon)])
            m1 += boxes_into_lon
        n1 += boxes_into_lat


    outgrid_flux = out_flux / new_area

    return outgrid_flux

def regrid_025x03125(infile = 0):
    # Global doesn't seem to be needed to be trimmed down for GEOS-Chem nested region
    if infile == 0:
        print "No source entered"
        sys.exit()


    orig_flux, orig_lat, orig_lon, orig_dates = get_fluxes.get_fluxes(infile)
    orig_area = grid_area.area(orig_lat,orig_lon)

    grid_flux = orig_flux * orig_area

    new_lat = grid_area.get_model_lat('0.25x0.3125')
    new_lon = grid_area.get_model_lon('0.25x0.3125')
    new_area = grid_area.area(new_lat,new_lon)
    out_flux = np.zeros([len(orig_dates),len(new_lat),len(new_lon)])

    lat_edges = grid_area.get_model_lat_edge('0.25x0.3125')
    lon_edges = grid_area.get_model_lon_edge('0.25x0.3125')

    # Regrid 0.5x0.5 to a higher resolution
    # 0.25 in the latitude dimension is easy enough but 0.3125 into 0.5 is not so
    # easy - have to make it 0.5x1 first (not sure this is the right thing to do)
    #orig_dates = orig_dates[:3]

    out_flux = np.zeros([len(orig_dates),len(new_lat),len(new_lon)])

    for dd in range(len(orig_dates)):
        flux_area = np.rot90(orig_flux[dd,:,:],3)
        new_flux = regrid_data(flux_area, orig_lon,orig_lat, new_lon,new_lat)

        rotated_flux = np.rot90(new_flux)

        out_flux[dd,:,:] = rotated_flux

    return out_flux

def regrid_data(data, lon, lat, new_lon, new_lat, do_filter=True):

    ax_lat=gax.gp_axis('lat', lat)
    ax_lon=gax.gp_axis('lat', lon)
    lonp1, lonp2, lonw=ax_lon.getwgt(new_lon)
    latp1, latp2, latw=ax_lat.getwgt(new_lat)
    new_ix=np.size(new_lon)
    new_jx=np.size(new_lat)
    # print new_ix, new_jx

    new_data1=lonw[:,np.newaxis]*data[lonp1, :]+(1.0-lonw[:,np.newaxis])*data[lonp2,:]
    new_data=latw[np.newaxis, :]*new_data1[:,latp1]+(1.0-latw[np.newaxis, :])*new_data1[:,latp2]

    if (do_filter):
        idx=np.where(new_lon<lon[0])
        idx=np.squeeze(idx)
        new_data[idx,:]=0

        idx=np.where(new_lon>lon[-1])
        idx=np.squeeze(idx)
        new_data[idx,:]=0


        idy=np.where(new_lat<lat[0])
        idy=np.squeeze(idy)
        new_data[:,idy]=0

        idy=np.where(new_lat>lat[-1])
        idy=np.squeeze(idy)
        new_data[:, idy]=0

    return new_data

def write_to_netcdf(flux,flux_name, res = '4x5'):
    latitude =  grid_area.get_model_lat(res)
    longitude = grid_area.get_model_lon(res)
    st_date = datetime(2013,01,01)
    dates = [st_date + dt.timedelta(days=x) for x in range(365)]
    #dates = [st_date + dt.timedelta(days=x) for x in range(3)]
    dates_str = [y.strftime('%Y%m%d') for y in dates]

    out_dirc = '/home/dfinch/Documents/CH4/emissions/regridded_emissions/'
    out_filename = '%sGlobal_CH4_flux_daily_%s_%s.nc' % (out_dirc, res,flux_name.upper())

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

if __name__ == '__main__':

    new_flux = regrid_025x03125('total')
    write_to_netcdf(new_flux, 'TOTAL', res = '0.25x0.3125')
## =============================================================================
## END OF PROGRAM
## =============================================================================
