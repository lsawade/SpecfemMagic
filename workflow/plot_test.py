# %%
import os
import toml
import numpy as np
import matplotlib.pyplot as plt
import obspy
import cmt3d
from cmt3d.ioi.functions.utils import cmt3d2gf3d
import cmt3d.viz.utils as vutils
from gf3d.seismograms import GFManager

# %%
config = toml.load('config.toml')
fw = config['root']['forward_specfem']

# %%
# Read forward seismograms and event

network = 'II'
station = 'BFO'

cmt = cmt3d.CMTSource.from_CMTSOLUTION_file(os.path.join(fw, 'DATA', 'CMTSOLUTION'))

gf3dcmt = cmt3d2gf3d(cmt)

st = obspy.read(os.path.join(fw, 'OUTPUT_FILES', '*.sac')).select(network=network, station=station)

# %%
# Read reciprocal seismograms
gfm = GFManager('/lustre/orion/geo111/scratch/lsawade/subset_test.h5')
gfm.load()

rp = gfm.get_seismograms(gf3dcmt).select(network=network, station=station)

# %%

import obsplotlib.plot as opl
plt.figure(figsize=(8, 3.5))
opl.station([st, rp], components='NEZ', labels=['Forward', 'Reciprocal'], origin_time=cmt.origin_time,
            ls=['-', (0, (3, 1, 1, 1))], colors=['k', 'r'], nooffset=True, absmax=2e-3,
            limits=(0*60,238*60), clip_on=False, transparent_axes=True)

plt.subplots_adjust(left=0.05, right=0.95, top=0.925, bottom=0.2, wspace=0.2, hspace=-0.3)
plt.savefig('BFO_test.pdf')
plt.close('all')

# %%

import obsplotlib.plot as opl
starttime = obspy.UTCDateTime('2018-01-23T09:31:30.518999Z') + 5
endtime = obspy.UTCDateTime('2018-01-23T13:31:40.899635Z') - 5

st.interpolate(starttime=starttime, npts=int(endtime-starttime), sampling_rate=1.0)
rp.interpolate(starttime=starttime, npts=int(endtime-starttime), sampling_rate=1.0)


# %%
opl.X(st.select(component='Z')[0], rp.select(component='Z')[0])
# opl.trace([st.select(component='Z')[0], rp.select(component='Z')[0]])
# plt.savefig('BFO_test_Z.pdf')


# %%


def plotb(
    x,
    y,
    tensor,
    linewidth=0.25,
    width=100,
    facecolor="k",
    clip_on=False,
    alpha=1.0,
    normalized_axes=True,
    ax=None,
    **kwargs,
):

    from matplotlib import transforms
    from obspy.imaging.beachball import beach as obspy_beach

    if normalized_axes or ax is None:
        if ax is None:
            ax = plt.gca()
        pax = vutils.axes_from_axes(ax, 948230, extent=[0, 0, 1, 1], zorder=10)
        pax.set_xlim(0, 1)
        pax.set_ylim(0, 1)
        pax.axis("off")
    else:
        if ax is None:
            ax = plt.gca()
        pax = ax

    # Plot beach ball
    bb = obspy_beach(
        tensor,
        linewidth=linewidth,
        facecolor=facecolor,
        bgcolor="w",
        edgecolor="k",
        alpha=alpha,
        xy=(x, y),
        width=width,
        size=100,  # Defines number of interpolation points
        axes=pax,
        **kwargs,
    )
    bb.set(clip_on=clip_on)

    # # This fixes pdf output issue
    bb.set_transform(transforms.Affine2D(np.identity(3)))

    pax.add_collection(bb)

# %%
size = 3
plt.figure(figsize=(size, size))
ax = plt.gca()
ax.axis('off')
plt.plot([0,1], [0,1],'w')
dpi = 72
plt.rcParams['figure.dpi'] = dpi
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
plotb(
        0.5 * dpi * size,
        0.5 * dpi * size,
        cmt.tensor,
        linewidth=0.75,
        width=0.99 * dpi * size,
        facecolor='k',
        normalized_axes=False,
        ax=ax,
    )

plt.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01)
plt.savefig('beachball.pdf', dpi=dpi)
plt.close('all')