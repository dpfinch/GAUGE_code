##==============================================================================
## Created on: 10/03/2017
## Created By: Douglas Finch
## Python 2.7
## Plot out the total emissions (both global and regional) of CH4 from
## emission files
##==============================================================================
import numpy as np
import scipy.io as io
from matplotlib import pyplot as plt
from datetime import datetime
import calendar
##==============================================================================
def get_variables(filename):
    open_file = io.netcdf_file(filename)
    return open_file

def get_anthro_emiss(anthro_type = 'Agricultural'):
    dirc_name = '/home/dfinch/Documents/CH4/emissions/'
    full_name = '%sCH4_flux_anthro_ft2010_%s_global_2000_2010.nc' % (dirc_name,anthro_type)
    #print full_name
    file_vari = get_variables(full_name)
    # print file_vari.variables.keys()
    CH4_flux = file_vari.variables['CH4_FLUX']
    CH4_data = CH4_flux.data
    return CH4_data

def get_anthro_dates(anthro_type = 'Agricultural'):
    dirc_name = '/home/dfinch/Documents/CH4/emissions/'
    full_name = '%sCH4_flux_anthro_ft2010_%s_global_2000_2010.nc' % (dirc_name,anthro_type)
    #print full_name
    file_vari = get_variables(full_name)
    date = file_vari.variables['date']
    dates_normal = []
    [dates_normal.append(datetime.strptime(str(x),'%Y%m%d')) for x in date.data]
    return dates_normal

def global_flux(raw_data):
    global_total = np.mean(raw_data,axis=(1,2))
    return global_total


def plot_all_anthro():
    anthro_emiss_types = ['Agricultural','Energy','Industrial',
                            'Other','Waste']

    anthro_dates = get_anthro_dates()
    total_anthro_flux = np.zeros(len(anthro_dates))
    for aet in anthro_emiss_types:
        raw_flux = get_anthro_emiss(anthro_type = aet)
        total_anthro_flux += global_flux(raw_flux)

    # Possibly need to divide flux by number of days in year if its a total
    # and not a mean - this is not what the units say but magnitudes are off
    # otherwise
    if False:
        total_anthro_flux  = anthro_flux_fix(total_anthro_flux)

    plt.figure(figsize = (10,5))
    plt.plot(anthro_dates,total_anthro_flux)
    # plt.xticks(anthro_dates, dates_trim)
    plt.ticklabel_format(style = 'sci', axis = 'y', scilimits = (0,0))
    plt.grid(True)
    plt.xlabel('Year')
    plt.ylabel('CH$_4$ Flux (kg m$^{-2}$ s$^{-1}$)')
    plt.title('Global Anthropogenic Flux of CH$_4$ (EDGAR)')
    save_dirc = '/home/dfinch/Documents/CH4/emissions/emission_plots/'
    out_filename = '%sAnthro_flux_plot.pdf' % save_dirc
    plt.savefig(out_filename)

def get_biomass_flux():
    dirc_name = '/home/dfinch/Documents/CH4/emissions/'
    full_name = '%sCH4_flux_biomass_global_1997_2011.nc' % dirc_name
    file_vari = get_variables(full_name)
    CH4_flux = file_vari.variables['CH4_FLUX']
    CH4_data = CH4_flux.data

    return CH4_data

def get_biomass_dates():
    dirc_name = '/home/dfinch/Documents/CH4/emissions/'
    full_name = '%sCH4_flux_biomass_global_1997_2011.nc' % dirc_name
    file_vari = get_variables(full_name)
    date = file_vari.variables['date']
    dates_normal = []
    [dates_normal.append(datetime.strptime(str(x),'%Y%m%d')) for x in date.data]
    return dates_normal

def plot_all_biomass():
    dates_normal = get_biomass_dates()
    raw_flux = get_biomass_flux()
    total_biomass_flux = global_flux(raw_flux)

    # Need to divide by number of days in month if the units given are wrong
    # Without this the magnitudes seem very wrong. - Need to check though
    if False:
        total_biomass_flux = biomass_flux_fix(total_biomass_flux)

    plt.figure(figsize = (10,5))
    plt.plot(dates_normal,total_biomass_flux)

    plt.ticklabel_format(style = 'sci', axis = 'y', scilimits = (0,0))
    plt.grid(True)
    plt.xlabel('Year')
    plt.ylabel('CH$_4$ Flux (kg m$^{-2}$ s$^{-1}$)')
    plt.title('Global Biomass Burning Flux of CH$_4$ (GFED)')
    save_dirc = '/home/dfinch/Documents/CH4/emissions/emission_plots/'
    out_filename = '%sBiomass_flux_plot.pdf' % save_dirc
    plt.savefig(out_filename)

def get_wetland_flux():
    dirc_name = '/home/dfinch/Documents/CH4/emissions/'
    full_name = '%sCH4_flux_wetlands_rice_global_2003_2009.nc' % dirc_name
    file_vari = get_variables(full_name)
    CH4_flux = file_vari.variables['CH4_FLUX']
    CH4_data = CH4_flux.data

    return CH4_data

def get_wetland_dates():
    dirc_name = '/home/dfinch/Documents/CH4/emissions/'
    full_name = '%sCH4_flux_wetlands_rice_global_2003_2009.nc' % dirc_name
    file_vari = get_variables(full_name)
    date = file_vari.variables['date']
    dates_normal = []
    [dates_normal.append(datetime.strptime(str(x),'%Y%m%d')) for x in date.data]
    return dates_normal

def plot_all_wetlands():
    dates_normal = get_wetland_dates()
    raw_flux = get_wetland_flux()
    total_wetlands_flux = global_flux(raw_flux)

    plt.figure(figsize = (10,5))
    plt.plot(dates_normal,total_wetlands_flux)

    plt.ticklabel_format(style = 'sci', axis = 'y', scilimits = (0,0))
    plt.grid(True)
    plt.xlabel('Year')
    plt.ylabel('CH$_4$ Flux (kg m$^{-2}$ s$^{-1}$)')
    plt.title('Global Wetlands Flux of CH$_4$ ')
    save_dirc = '/home/dfinch/Documents/CH4/emissions/emission_plots/'
    out_filename = '%sWetlands_flux_plot.pdf' % save_dirc
    plt.savefig(out_filename)

def  anthro_flux_fix(flux):
    dates = get_anthro_dates()
    for n,d in enumerate(dates):
        if calendar.isleap(d.year):
            flux[n] = flux[n] / 366
        else:
            flux[n] = flux[n] / 365
    return flux

def biomass_flux_fix(flux):
    dates = get_biomass_dates()
    for n,d in enumerate(dates):
        num_dates = calendar.monthrange(d.year,d.month)[1]
        flux[n] = flux[n] / num_dates
    return flux

def plot_all_flux(bio = True, wetl = True, anthro = True):
    anthro_emiss_types = ['Agricultural','Energy','Industrial',
                            'Other','Waste']
    # Can return only on anthro type if required
    # anthro_emiss_types = ['Industrial']


    anthro_dates = get_anthro_dates()
    total_anthro_flux = np.zeros(len(anthro_dates))
    for aet in anthro_emiss_types:
        raw_flux = get_anthro_emiss(anthro_type = aet)
        # print "Total flux for %s: %f" % (aet, np.sum(raw_flux))
        total_anthro_flux += global_flux(raw_flux)

    # Possibly need to divide flux by number of days in year if its a total
    # and not a mean - this is not what the units say but magnitudes are off
    # otherwise
    if False:
        total_anthro_flux  = anthro_flux_fix(total_anthro_flux)

    wetlands_dates = get_wetland_dates()
    raw_flux = get_wetland_flux()
    total_wetlands_flux = global_flux(raw_flux)

    biomass_dates = get_biomass_dates()
    raw_flux = get_biomass_flux()
    total_biomass_flux = global_flux(raw_flux)

    # Need to divide by number of days in month if the units given are wrong
    # Without this the magnitudes seem very wrong. - Need to check though
    # NOT TRUE! Was previously summing over globe not averaging over globe
    if False:
        total_biomass_flux = biomass_flux_fix(total_biomass_flux)

    plt.figure(figsize = (10,5))
    if anthro:
        plt.plot(anthro_dates,total_anthro_flux, label = 'Anthropogenic')
    if wetl:
        plt.plot(wetlands_dates,total_wetlands_flux, label = 'Wetlands')
    if bio:
        plt.plot(biomass_dates, total_biomass_flux , label = 'Biomass Burning')
    plt.legend(frameon = False)
    plt.ticklabel_format(style = 'sci', axis = 'y', scilimits = (0,0))
    plt.grid(True)
    plt.xlabel('Year')
    plt.ylabel('CH$_4$ Flux (kg m$^{-2}$ s$^{-1}$)')
    plt.title('Global Flux of CH$_4$ ')
    save_dirc = '/home/dfinch/Documents/CH4/emissions/emission_plots/'
    out_filename = '%sAll_sources_flux_plot.pdf' % save_dirc
    plt.savefig(out_filename)

def plot_individual_anthro():
    anthro_emiss_types = ['Agricultural','Energy','Industrial',
                            'Other','Waste']

    anthro_dates = get_anthro_dates()
    plt.figure(figsize = (10,5))
    for aet in anthro_emiss_types:
        raw_flux = get_anthro_emiss(anthro_type = aet)
        anthro_flux = global_flux(raw_flux)

    # Possibly need to divide flux by number of days in year if its a total
    # and not a mean - this is not what the units say but magnitudes are off
    # otherwise
        if False:
            total_anthro_flux  = anthro_flux_fix(anthro_flux)

        plt.plot(anthro_dates,anthro_flux, label = aet)

    plt.legend(frameon = False, loc = 'center left', bbox_to_anchor = (0.8,0.6))
    plt.ticklabel_format(style = 'sci', axis = 'y', scilimits = (0,0))
    plt.grid(True)
    plt.xlabel('Year')
    plt.ylabel('CH$_4$ Flux (kg m$^{-2}$ s$^{-1}$)')
    plt.title('Global Anthropogenic Flux of CH$_4$ ')
    save_dirc = '/home/dfinch/Documents/CH4/emissions/emission_plots/'
    out_filename = '%sAnthro_sources_split_flux_plot.pdf' % save_dirc
    # plt.tight_layout()
    plt.savefig(out_filename)
    pass

if __name__ == '__main__':

    plot_all_anthro()
    # plot_all_biomass()
    # plot_all_wetlands()
    # plot_all_flux(anthro = True, bio = True, wetl = True)
    # plot_individual_anthro()

## ==============================================================================
## END OF PROGRAM
## ==============================================================================
