#!/bin/env python

from lwsspy.GF.simulation import Simulation
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


S = Simulation(**inputdict)
S.update_forces_and_stations()
print(S)
