#!/bin/env python

import os
import sys
from python.runsf import sfrun, simultaneous_run
import toml
import os


sfmagic = "/scratch/gpfs/lsawade/SpecfemMagicGF"
stationdir = os.path.join(sfmagic, 'DB', 'II', 'BFO')
config = toml.load(os.path.join(stationdir, 'config.toml'))
db = config['stationdir']
rundirs = dict()
for comp in ['N', 'E', 'Z']:
    rundirs[comp] = os.path.join(db, comp, 'specfem')

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
        for comp, rundir in rundirs.items():
            os.chdir(rundir)
            print(os.getcwd())
            sfrun(rtype='s')
            os.chdir(cwd)

if os.environ['FORWARD_TEST'] == 'True':
    specfemdir = 'specfem3d_globe_forward'

    os.chdir(specfemdir)
    print("Running the solver forward test...")
    sfrun(rtype='s')
    os.chdir(cwd)
