#!/bin/env python

from lwsspy.GF.simulation import Simulation
import toml


def read_toml(file) -> dict:
    return toml.load(file)


# Read config file
inputdict = read_toml('reci.toml')['root']['cfg']

# Add extra steps
inputdict['nstep'] = None
# inputdict['ndt'] = 7.0

###################################
# SIMULATION DIRECTORY CREATION  #
# Setup


S = Simulation(**inputdict)
S.update_forces_and_stations()
print(S)
