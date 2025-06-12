"""
This scripts sets up a base database for a station, so that simulations can be run subsequently for this stations
Either set the ENVIRONMENT variable WORKFLOW_DIR or run it when you are located in the workflow directory.
"""

#!/bin/env python

import os, sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from gf3d.simulation import Simulation
import toml

from python.read import read_stations, read_toml




if os.path.exists('config.toml'):
    WORKFLOW_DIR = './'
else:
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
station_file = os.path.join(root['station_file'])
net, sta, lat, lon, ele, bur, sen = read_stations(station_file)

# Setup
db = root['db']
stationdir = os.path.join(db, net[0], sta[0])
inputdict['network'] = net[0]
inputdict['station'] = sta[0]
inputdict['stationdir'] = stationdir
inputdict['station_latitude'] = lat[0]
inputdict['station_longitude'] = lon[0]
inputdict['station_burial'] = bur[0]
###################################

# SIMULATION DIRECTORY CREATION  #
S = Simulation(**inputdict)
S.create()
S.update_forces_and_stations()
print(S)

# dump config
with open(os.path.join(stationdir, 'config.toml'), 'w') as f:
    toml.dump(inputdict, f)
