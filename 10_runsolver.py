#!/bin/env python

import os
import sys
from runsf import sfrun, simultaneous_run

# Current dir
cwd = os.path.abspath(os.getcwd())

if os.environ['RECIPROCAL'] == 'True':
    specfemdir = 'specfem3d_globe'

    print("Running the solver reciprocal...")
    os.chdir(specfemdir)
    print(os.getcwd())

    if simultaneous_run():
        sfrun(rtype='s')
        os.chdir(cwd)
    else:
        for rundir in ['run0001', 'run0002', 'run0003']:
            os.chdir(rundir)
            print(os.getcwd())
            sfrun(rtype='s')
            os.chdir('..')
        os.chdir(cwd)

# sys.exit()

if os.environ['FORWARD_TEST'] == 'True':
    specfemdir = 'specfem3d_globe_forward'

    os.chdir(specfemdir)
    print("Running the solver forward test...")
    sfrun(rtype='s')
    os.chdir(cwd)
