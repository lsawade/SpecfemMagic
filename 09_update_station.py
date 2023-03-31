#!/bin/env python

from gf3d.simulation import Simulation
import toml
import os


def read_toml(file) -> dict:
    return toml.load(file)


WORKFLOW_DIR = os.getenv("WORKFLOW_DIR")

if WORKFLOW_DIR is None:
    raise ValueError('CANT GET WORKFLOW_DIR!')

# Read config file
inputdict = read_toml(os.path.join(WORKFLOW_DIR, 'config.toml'))['root']['cfg']

# Add extra steps
inputdict['nstep'] = None
# inputdict['ndt'] = 7.0

###################################
# SIMULATION DIRECTORY CREATION  #
# Setup

inputdict['stationdir'] = os.path.join(
    WORKFLOW_DIR, '..', 'DB_test', 'II', 'BFO')
inputdict['network'] = 'II'
inputdict['station'] = 'BFO'
inputdict['station_burial'] = 160.0
inputdict['station_latitude'] = 48.3
inputdict['station_longitude'] = 8.3
S = Simulation(**inputdict)
S.update_forces_and_stations()
print(S)
