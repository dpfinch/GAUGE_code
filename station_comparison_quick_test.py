import gchem
import numpy as np
from matplotlib import pyplot as plt
import geos_info
import grid_area

dirc = '/home/dfinch/Documents/CH4/model_output/4x5/'
fname = '%sctm_4x5.bpch' % dirc

gr = gchem.bpch.open_file(fname)
ch4 = gr.filter(category = 'IJ-AVG-$')


longitude = -9.899
latitude = 53.326

model_lat = grid_area.get_model_lat(model_res='4x5')
model_lon = grid_area.get_model_lon(model_res='4x5')

station_lon=min(range(len(model_lon)), key=lambda i: abs(model_lon[i]-longitude))
station_lat=min(range(len(model_lat)), key=lambda i: abs(model_lat[i]-latitude))

# Start empty array to append dates and ch4 conc
monthly_date = []
monthly_ch4 = []

for m in range(len(ch4)):
    temp = np.mean(ch4[m].value[:,:,0:5],axis=2)
    rotated = np.rot90(temp,3)
    flipped = np.fliplr(rotated)
##        if station == 'MLO':
##            monthly_ch4.append(np.mean(new_array[station_lat,station_lon,18])*1e9)
##        else:
    print temp[station_lon,station_lat]*1e9, flipped[station_lat,station_lon]*1e9
    monthly_ch4.append(flipped[station_lat,station_lon]*1e9)
##      monthly_ch4.append(np.mean(temp[station_lon,station_lat,0:5])*1e9)
    monthly_date.append(ch4[m].times[0])

# Sort the data into chronological order
ch4_station = [x for y, x in sorted(zip(monthly_date, monthly_ch4))]
monthly_date.sort()
