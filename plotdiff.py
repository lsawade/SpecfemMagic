#!/usr/bin/env python
from obspy import read
from matplotlib.pyplot import *

st0 = read("../seismograms/original/*.sac")
tr0 = st0.select(component="Z")[0]
stp = read("../seismograms/forward/*.sac")
trp = stp.select(component="Z")[0]
stm = read("../seismograms/backward/*.sac")
trm = stm.select(component="Z")[0]

dx = 0.5
xmin,xmax = 200, 500

figure(figsize=(10, 5))
subplot(211)
plot(tr0.times(), tr0.data, "k", label="0")
plot(trp.times(), trp.data, "--", c=(0.8, 0.2, 0.2), label="+")
plot(trm.times(), trm.data, ":", c=(0.2, 0.2, 0.8), label="-")
xlim(xmin,xmax)
# ylim(-2e-3,2e-3)
legend()
subplot(212)
plot(tr0.times(), (trp.data - tr0.data)/dx, "-", label="forward", c=(0.2, 0.8, 0.2))
plot(tr0.times(), (tr0.data - trm.data)/dx, "--", label="backward", c=(0.2, 0.2, 0.8))
plot(tr0.times(), (trp.data - trm.data)/(2*dx), ":", label="centered", c=(0.8, 0.2, 0.2))
legend()
# ylim(-1e-9,1e-9)
xlim(xmin,xmax)
filename = f"{tr0.stats.network}.{tr0.stats.station}_diff.pdf"

savefig(filename, format="pdf")