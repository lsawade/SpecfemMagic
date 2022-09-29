#!/usr/bin/env python
import os
import sys
import numpy as np
import matplotlib.pyplot as plt

plt.switch_backend('agg')

s = []
f = []
labels = ['N', 'E', 'Z', 'forward']
for i in range(3):
    if os.path.exists(f'specfem3d_globe/run000{int(i+1)}/DATA/stf'):
        s.append(np.loadtxt(
            f'specfem3d_globe/run000{int(i+1)}/DATA/stf').T)

if os.path.exists(f'specfem3d_globe/run000{int(i+1)}/DATA/stf'):
    s.append(np.loadtxt(
        f'specfem3d_globe_forward/DATA/stf').T)

if len(s) == 0:
    try:
        for i in range(3):
            s.append(np.loadtxt(
                f'specfem3d_globe/run000{int(i+1)}/OUTPUT_FILES/plot_source_time_function.txt').T)
            f.append(np.loadtxt(
                f'specfem3d_globe/run000{int(i+1)}/OUTPUT_FILES/plot_source_spectrum.txt').T)

        s.append(np.loadtxt(
            f'specfem3d_globe_forward/OUTPUT_FILES/plot_source_time_function.txt').T)

        f.append(np.loadtxt(
            f'specfem3d_globe_forward/OUTPUT_FILES/plot_source_spectrum.txt').T)

    except Exception as e:
        print(e)

        sys.exit()

plt.figure(figsize=(10, 10))

if len(f) > 0:
    plt.subplot(211)
for i in range(len(s)):
    plt.plot(s[i][0, :], s[i][1, :], label=f'{labels[i]:s}', lw=0.25)
plt.xlim(-50, 50)
plt.xlabel('Time [s]')
plt.ylabel('Amplitude')
plt.legend()
plt.title('Source Time Function')

if len(f) > 0:
    plt.subplot(212)
    for i in range(len(f)):
        if i in [0, 1, 2]:
            factor = 1e14
        elif i == 3:
            factor = 2.14599e+25
        plt.plot(f[i][0, :], f[i][1, :]/factor,
                 label=f'{labels[i]:s}', lw=0.25)
    plt.xlabel('Frequency [Hz]')
    plt.ylabel('Amplitude')
    plt.title('Source Spectrum')

    plt.savefig('stf.pdf')
