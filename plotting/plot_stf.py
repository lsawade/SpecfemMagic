#!/usr/bin/env python
import sys
import numpy as np
import matplotlib.pyplot as plt
plt.switch_backend('agg')
s = np.loadtxt('specfem3d_globe/OUTPUT_FILES/plot_source_time_function.txt').T
f = np.loadtxt('specfem3d_globe/OUTPUT_FILES/plot_source_spectrum.txt').T


plt.figure()
plt.subplot(211)
plt.plot(s[0,:], s[1,:])
plt.xlabel('Time [s]')
plt.ylabel('Amplitude')
plt.title('Source Time Function')
plt.subplot(212)
plt.plot(f[0,:], f[1,:])
plt.xlabel('Frequency [Hz]')
plt.ylabel('Amplitude')
plt.title('Source Spectrum')
plt.savefig('stf.png', dpi=300)