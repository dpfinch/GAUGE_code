##==============================================================================
## Created on: 15/03/2017
## Created By: Douglas Finch
## Python 2.7
## Plot out the regridded emissions both globally and regionally
##==============================================================================
import numpy as np
import scipy.io as io
from datetime import datetime
import datetime as dt
from matplotlib import pyplot as plt
from mpl_toolkits.basemap import Basemap
import geos_info
import brewer2mpl
##==============================================================================

def get_fluxes(source = 'total'):
    source_name = source.upper()
    emiss_dirc = '/home/dfinch/Documents/CH4/emissions/regridded_emissions/'

    flux_file = '%sGlobal_CH4_flux_daily_05x05_%s.nc' % (emiss_dirc, source_name)

    open_file = io.netcdf_file(flux_file)
    flux = open_file.variables['CH4_Flux']
    lat = open_file.variables['latitude']
    lon = open_file.variables['longitude']
    dates = open_file.variables['date']

    dates_normal = []
    [dates_normal.append(datetime.strptime(str(x),'%Y%m%d')) for x in dates.data]

    return flux.data, lat.data, lon.data, dates_normal

def get_region(source = 'total', lat1 = 32.75, lat2 = 61.25 , lon1 = -15.00 , lon2 = 40.00):
    # Default set to EU grid
    # ( taken from co2_clean_code/ensemble_flux_4x5/eu_lon_lat.npz)

    flux, lat, lon, dates  = get_fluxes(source)

    lat1_coord = min(range(len(lat)), key=lambda i: abs(lat[i]-lat1))
    lat2_coord = min(range(len(lat)), key=lambda i: abs(lat[i]-lat2))
    lon1_coord = min(range(len(lon)), key=lambda i: abs(lon[i]-lon1))
    lon2_coord = min(range(len(lon)), key=lambda i: abs(lon[i]-lon2))

    regional_lats = lat[lat1_coord:lat2_coord]
    regional_lons = lon[lon1_coord:lon2_coord]

    regional_flux = flux[:,lat1_coord:lat2_coord,lon1_coord:lon2_coord]

    return regional_flux,regional_lats, regional_lons, dates

def time_series(domain = 'eu',source = 'total'):
    if domain == 'eu':
        flux, lats, lons, dates = get_region(source)
        regionname = 'EU_regional'
    else:
        flux, lats, lons, dates = get_fluxes(source)
        regionname = 'Global'

    ts_flux = np.mean(flux, axis = (1,2))

    plt.figure(figsize = (10,5))
    plt.plot(dates, ts_flux)
    plt.ticklabel_format(style = 'sci', axis = 'y', scilimits = (0,0))
    plt.grid(True)
    plt.xlabel('Date')
    plt.ylabel('CH$_4$ Flux (kg m$^{-2}$ s$^{-1}$)')
    # plt.title('')
    save_dirc = '/home/dfinch/Documents/CH4/emissions/emission_plots/regridded/'
    out_filename = '%s%s_%s_CH4_flux.pdf' % (save_dirc, regionname,source)
    plt.savefig(out_filename)
    plt.close()

    pass

def mean_flux_map(domain = 'eu',source = 'total'):
    if domain == 'eu':
        flux, lats, lons, dates = get_region(source)
        regionname = 'EU_regional'
    else:
        flux, lats, lons, dates = get_fluxes(source)
        regionname = 'Global'

    plt.figure(figsize=(10,6))
    m=Basemap(llcrnrlon=lons[0],llcrnrlat=lats[0],urcrnrlon=lons[-1],
              urcrnrlat=lats[-1],projection='cyl', resolution='i')

    m.drawparallels(np.arange(-90,90,10),labels=[1,0,0,0],alpha = 0.75)
    m.drawmeridians(np.arange(-180,180,10),labels=[0,0,0,1], alpha = 0.75)
    m.drawcoastlines(linewidth=0.5)
    m.drawcountries(linewidth=0.75)

    mlon,mlat = m.makegrid(len(lons),len(lats))

    xx,yy = m(mlon,mlat)

    if source == 'anthro' or source == 'total':
        clevs = np.linspace(np.min(flux),1.5e-9,9)
        extend = 'max'
    else:
        clevs = np.linspace(np.min(flux),np.max(flux),9)
        extend = 'neither'
    cmap = brewer2mpl.get_map('OrRd','Sequential',9).mpl_colormap

    cs = m.contourf(xx,yy,np.mean(flux,axis = 0),clevs,cmap=cmap, extend = extend)
    cb = m.colorbar(cs, location = 'bottom', pad = "10%")
    cb.set_label('CH$_4$ Flux (kg m$^{-2}$ s$^{-1}$)')
    plt.title(source.title())

    save_dirc = '/home/dfinch/Documents/CH4/emissions/emission_plots/regridded/'
    out_filename = '%s%s_%s_CH4_flux_map.pdf' % (save_dirc, regionname,source)
    plt.savefig(out_filename)
    plt.close()

    pass

def all_dates_flux_map(domain = 'eu',source = 'total'):
    if domain == 'eu':
        flux, lats, lons, dates = get_region(source)
        regionname = 'EU_regional'
    else:
        flux, lats, lons, dates = get_fluxes(source)
        regionname = 'Global'

    for n_step in range(flux.shape[0]):

        plt.figure(figsize=(10,6))
        m=Basemap(llcrnrlon=lons[0],llcrnrlat=lats[0],urcrnrlon=lons[-1],
                urcrnrlat=lats[-1],projection='cyl', resolution='i')

        m.drawparallels(np.arange(-90,90,10),labels=[1,0,0,0],alpha = 0.75)
        m.drawmeridians(np.arange(-180,180,10),labels=[0,0,0,1], alpha = 0.75)
        m.drawcoastlines(linewidth=0.5)
        m.drawcountries(linewidth=0.75)

        mlon,mlat = m.makegrid(len(lons),len(lats))

        xx,yy = m(mlon,mlat)

        if source == 'anthro' or source == 'total':
            clevs = np.linspace(np.min(flux),1.5e-9,9)
            extend = 'max'
        else:
            clevs = np.linspace(np.min(flux),np.max(flux),9)
            extend = 'neither'
        cmap = brewer2mpl.get_map('OrRd','Sequential',9).mpl_colormap

        cs = m.contourf(xx,yy,flux[n_step,:,:],clevs,cmap=cmap, extend = extend)
        cb = m.colorbar(cs, location = 'bottom', pad = "10%")
        cb.set_label('CH$_4$ Flux (kg m$^{-2}$ s$^{-1}$)')
        plt.title(source.title() + ' CH$_4$ Flux ' + str(dates[n_step].date()))

        save_dirc = '/home/dfinch/Documents/CH4/emissions/emission_plots/regridded/daily_contours/'
        out_filename = '%s%s_%s_CH4_flux_map_%s.png' % (save_dirc, regionname,source,str(n_step).zfill(3))
        plt.savefig(out_filename)
        plt.close()

    pass

if __name__ == '__main__':
    # time_series(domain = 'eu',source = 'total')
    # mean_flux_map(domain = 'eu',source = 'total')
    all_dates_flux_map(domain = 'eu',source = 'total')
## =============================================================================
## END OF PROGRAM
## =============================================================================
