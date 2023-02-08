#!/usr/bin/env python
'''
This script relies/d on the 'run_frechet_simulation.sh'
which created event directories containing both an event
and subdirectories for seismograms of s single station.
It then proceeds to create map plots of the event and the
station.

eventdir/
|--CMTSOLUTION
|--seismograms/
   |--2nd/
      |--*.sac
      |--..
   |--DD
      |--*.sac
      |--..

To generalize this function, some small changes have to be made,
e.g., generalize it to work with multiple stations.

It places the created figure in the event directory.

2021.09.11 11:00 -- Lucas Sawade

'''

import matplotlib.pyplot as plt
from lwsspy.maps.plot_map import plot_map
from lwsspy.maps.map_axes import map_axes
from lwsspy.maps.gctrack import gctrack

import os
import sys
from glob import glob
from cartopy.crs import PlateCarree
from obspy import read
from numpy import *
from matplotlib.pyplot import *
from matplotlib.gridspec import GridSpec, GridSpecFromSubplotSpec
from lwsspy.seismo.source import CMTSource
from lwsspy.plot_util.updaterc import updaterc
from lwsspy.plot_util.axes_from_axes import axes_from_axes
from lwsspy.plot_util.plot_label import plot_label

updaterc()

# Locations
scriptdir = os.path.dirname(os.path.abspath(__file__))
eventdir = sys.argv[1]
event = os.path.join(eventdir, "CMTSOLUTION")
seismograms = os.path.join(eventdir, "seismograms")
seisdirs = glob(os.path.join(seismograms, "*"))
filename = os.path.join(eventdir, "map.png")

# Read Source
cmtsource = CMTSource.from_CMTSOLUTION_file(event)
lat = cmtsource.latitude
lon = cmtsource.longitude
dep = cmtsource.depth_in_m/1000.0

# Station lat/lon
tr = read(os.path.join(seisdirs[0], "*.sac"))[0]
stlat = tr.stats.sac['stla']
stlon = tr.stats.sac['stlo']          

# Central Longitude
clon = (stlon + lon)/2.0

# Plot
plt.figure(figsize=(6,3), facecolor='none')
ax = map_axes(central_longitude=clon)
ax.set_global()
ax.spines['geo'].set_linewidth(0.25)
ax.patch.set_facecolor([1.0, 1.0, 1.0])
ax.patch.set_alpha(1.0)

plot_map()


# Track between station and event
tlats, tlons, _ = gctrack([stlat, lat], [stlon, lon], dist=0.5)
plt.plot(tlons, tlats, 'k-', transform=PlateCarree())

# Station
plt.plot(stlon, stlat, 'rv', markeredgecolor='k', transform=PlateCarree())

# Event
plt.plot(lon, lat, 'b*', markeredgecolor='k', transform=PlateCarree())

plt.subplots_adjust(top=1.0, bottom=0.0, left=0.0, right=1.0)
plt.savefig(filename, format='png', dpi=600)
plt.show()

