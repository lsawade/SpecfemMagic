#!/bin/env python

from gf3d.simulation import Simulation
import toml
import os
from python.read import read_stations


def read_toml(file) -> dict:
    return toml.load(file)


WORKFLOW_DIR = os.getenv("WORKFLOW_DIR")

if WORKFLOW_DIR is None:
    raise ValueError('CANT GET WORKFLOW_DIR!')

# Read config file
root = read_toml(os.path.join(WORKFLOW_DIR, 'config.toml'))['root']

inputdict = root['cfg']

# Add extra steps
inputdict['nstep'] = None
inputdict['par_file'] = os.path.join(WORKFLOW_DIR, inputdict['par_file'])
inputdict['target_file'] = os.path.join(WORKFLOW_DIR, inputdict['target_file'])
inputdict['cmtsolutionfile'] = os.path.join(WORKFLOW_DIR, inputdict['cmtsolutionfile'])

# Setup Station directory for test run
station_file = os.path.join(WORKFLOW_DIR, root['station_file'])
net, sta, lat, lon, ele, bur, sen = read_stations(station_file)

# Setup
db = root['db']
stationdir = os.path.join(db, net[0], sta[0])
inputdict['stationdir'] = stationdir

###################################
# SIMULATION DIRECTORY CREATION  #
S = Simulation(**inputdict)
S.update_forces_and_stations()
print(S)
