#!/usr/bin/env python
import sys
import numpy as np
import matplotlib.pyplot as plt
plt.switch_backend('agg')

s = []
labels = ['N', 'E', 'Z', 'forward']
for i in range(3):
    s.append(np.loadtxt(
        f'specfem3d_globe/run000{int(i+1)}/DATA/stf').T)

s.append(np.loadtxt(
    f'specfem3d_globe_forward/DATA/stf').T)

# s = np.loadtxt(
#     'specfem3d_globe_forward/OUTPUT_FILES/plot_source_time_function.txt').T
# f = np.loadtxt(
#     'specfem3d_globe_forward/OUTPUT_FILES/plot_source_spectrum.txt').T


plt.figure()

# plt.subplot(211)
for i in range(4):
    plt.plot(s[i][0, :], s[i][1, :], label=f'{labels[i]:s}')
plt.xlabel('Time [s]')
plt.ylabel('Amplitude')
plt.legend()
plt.title('Source Time Function')
plt.savefig('stf.png', dpi=300)
# plt.subplot(212)
# plt.plot(f[0, :], f[1, :])
# plt.xlabel('Frequency [Hz]')
# plt.ylabel('Amplitude')
# plt.title('Source Spectrum')
