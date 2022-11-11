#!/bin/env python
from lwsspy.GF.simulation import Simulation
import toml


def read_toml(file) -> dict:
    return toml.load(file)


# Import
inputdict = read_toml("reci.toml")

###################################
#  SIMULATION DIRECTORY CREATION  #
# Setup


S = Simulation(**inputdict)
print(S)
S.create()
