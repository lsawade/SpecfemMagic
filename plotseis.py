#!/usr/bin/env python
import sys
from obspy import read
st = read(sys.argv[1])
filename = f"{st[0].stats.network}.{st[0].stats.station}.pdf"
st.plot(outfile=filename)