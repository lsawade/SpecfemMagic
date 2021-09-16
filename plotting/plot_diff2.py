#!/usr/bin/env python
'''
This script relies/d on the 'run_frechet_simulation.sh'
which created event directories containing both an event
and subdirectories for seismograms of s single station.
it then proceeds to create plots comparing the difference
between the seismograms at the station component-wise.

eventdir/
|--CMTSOLUTION
|--seismograms/
   |--2nd/
      |--*.sac
      |--..
   |--DD
      |--*.sac
      |--..

To generalize this function, some small changes have to be made.
It places the created figure in the event directory

2021.09.11 11:00 -- Lucas Sawade

'''


import os
import sys
from glob import glob
from obspy import read
from numpy import *
from matplotlib.pyplot import *
from matplotlib.gridspec import GridSpec, GridSpecFromSubplotSpec
from lwsspy.seismo.source import CMTSource
from lwsspy.plot_util.updaterc import updaterc
from lwsspy.plot_util.plot_label import plot_label

updaterc()

# Locations
scriptdir = os.path.dirname(os.path.abspath(__file__))
eventdir = sys.argv[1]
event = os.path.join(eventdir, "CMTSOLUTION")
seismograms = os.path.join(eventdir, "seismograms")
seisdirs = glob(os.path.join(seismograms, "*"))
filename = os.path.join(eventdir, "2nd_v_DD.pdf")

# Read source
cmtsource = CMTSource.from_CMTSOLUTION_file(event)
lat = cmtsource.latitude
lon = cmtsource.longitude
dep = cmtsource.depth_in_m/1000.0

# Read seismograms
names = []
streams = []
for sdir in seisdirs:
    try:    
        streams.append(read(os.path.join(sdir, "*.sac")))
        names.append(os.path.basename(sdir))

    except Exception as e:
        print(f"No seismograms in {sdir}")

# Plot
fig = figure(figsize=(8, 8))
subplots_adjust(top=0.925, bottom=0.075, left=0.1, right=0.9)
outer = GridSpec(ncols=2, nrows=3, wspace=0.1, height_ratios = [1,1,1], width_ratios=[4,1]) 

nt = max(streams[0][0].times())

xlims = (2900, 3100)
for _j in range(2):

    for _i, _comp in enumerate(['N', 'E', 'Z']):

        inner = GridSpecFromSubplotSpec(ncols=1, nrows=2, subplot_spec = outer[_i, _j], hspace=0.275, height_ratios = [2,1])

        # Comparison plot
        ax = fig.add_subplot(inner[0])

        for _st, _n, _c, _ls in zip(streams, names, ['k', 'r'], ['-', '--']):

            try:
                tr = _st.select(component=_comp)[0]
                plot(tr.times(), tr.data, label=_n, lw=0.75, c=_c, ls=_ls)

            except Exception as e:
                print(e)
                plot([], [])

        if _i == 0 and _j == 0:
            legend(loc='lower left', ncol=2, frameon=False)

        ax.set_xlim(0, nt)
        ax.xaxis.set_ticks_position('top')
        ax.xaxis.set_ticklabels([])

        if _j == 1:
            ax.set_xlim(xlims)
            ax.yaxis.set_ticklabels([])
            ax.yaxis.set_ticks_position('right')
        else:
            plot_label(ax, _comp, location=1, dist=0.01, box=False)
            ax.yaxis.set_ticks_position('left')

        # Difference Plot
        ax = fig.add_subplot(inner[1])

        try:
            tr0 = streams[0].select(component=_comp)[0]
            tr1 = streams[1].select(component=_comp)[0]
            plot(tr.times(), (tr1.data - tr0.data), 'k', lw=0.75)

        except Exception as e:
            print(e)

        ax.set_xlim(0, nt)
        ax.xaxis.set_ticks_position('bottom')

        if _i != 2:
            ax.xaxis.set_ticklabels([])
        
        if _j == 1:
            ax.set_xlim(xlims)
            ax.yaxis.set_ticklabels([])
            ax.yaxis.set_ticks_position('right')
        else:
            plot_label(ax, _comp + ' diff', location=1, dist=0.01, box=False)
            ax.yaxis.set_ticks_position('left')

suptitle(f"(Lat, Lon, Depth) = ({lat:.2f}, {lon:.2f}, {dep:.2f} km)")            
savefig(filename, format="pdf")        
show()

