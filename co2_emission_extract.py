##==============================================================================
## Created on: 14/03/2017
## Created By: Douglas Finch
## Python 2.7
## Try and get some information from Liangs CO2 emission files
##==============================================================================
import numpy as np
import scipy.io as io
from matplotlib import pyplot as plt
from datetime import datetime
import calendar
import gchem
##==============================================================================
emis_file = '/home/dfinch/Documents/CH4/co2_clean_code/run_4x5_co2/surface_flux/CO2_EMISSION.2013D001.4x5'

data = gchem.bpch.open_file(emis_file)
co2_flux = data.filter(category = 'CO2_FLUX')[0].value

## =============================================================================
## END OF PROGRAM
## =============================================================================
