#!/usr/bin/env python
import sys
from obspy import read
import matplotlib.pyplot as plt
plt.switch_backend('pdf')
st = read(sys.argv[1])
print(len(st))
for tr in st:
    tr.data /= 1e23
filename = f"{st[0].stats.network}.{st[0].stats.station}.pdf"
st.plot(outfile=filename)
