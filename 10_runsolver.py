#!/bin/env python

import os
from python.runsf import sfrun, simultaneous_run
from python.read import read_stations, read_toml
import toml
import os


WORKFLOW_DIR = os.getenv("WORKFLOW_DIR")

if WORKFLOW_DIR is None:
    raise ValueError('CANT GET WORKFLOW_DIR!')

# Read config file
root = read_toml(os.path.join(WORKFLOW_DIR, 'config.toml'))['root']
db = root['db']
station_file = os.path.join(WORKFLOW_DIR, root['station_file'])
net, sta, lat, lon, ele, bur, sen = read_stations(station_file)

# Setup
stationdir = os.path.join(db, net[0], sta[0])
config = toml.load(os.path.join(stationdir, 'config.toml'))

db = config['stationdir']
rundirs = dict()
for comp in []: # 'N', 'E', 'Z'
    rundirs[comp] = os.path.join(db, comp, 'specfem')

# Current dir
cwd = os.path.abspath(os.getcwd())

if os.environ['RECIPROCAL'] == 'True':

    print("Running the solver reciprocal...")
    print(os.getcwd())

    for comp, rundir in rundirs.items():
        os.chdir(rundir)
        print(os.getcwd())
        sfrun(rtype='s', mps=6)
        os.chdir(cwd)

if os.environ['FORWARD'] == 'True':
    specfemdir = os.environ['SPECFEM_DIR']

    os.chdir(specfemdir)
    print("Running the solver forward test...")
    sfrun(rtype='s', mps=6)
    os.chdir(cwd)
