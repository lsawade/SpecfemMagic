#!/usr/bin/env python
import os
from glob import glob
from obspy import read
from numpy import *
from matplotlib.pyplot import *
from matplotlib.gridspec import GridSpec, GridSpecFromSubplotSpec
from lwsspy.plot_util.updaterc import updaterc
from lwsspy.plot_util.plot_label import plot_label
updaterc()

scriptdir = os.path.dirname(os.path.abspath(__file__))
maindir   = os.path.join(os.path.join(scriptdir, "seismograms"))

seisdirs  = glob(os.path.join(maindir, "*"))


names = []
streams = []

for sdir in seisdirs:
    try:    
        streams.append(read(os.path.join(sdir, "*.sac")))
        names.append(os.path.basename(sdir))

    except Exception as e:
        print(f"No seismograms in {sdir}")


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

filename = f"2nd_v_DD.pdf"
savefig(filename, format="pdf")        
show()

