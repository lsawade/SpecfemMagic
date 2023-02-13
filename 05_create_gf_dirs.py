#!/bin/env python
from lwsspy.GF.simulation import Simulation
import toml
import os


def read_toml(file) -> dict:
    return toml.load(file)


WORKFLOW_DIR = os.getenv("WORKFLOW_DIR")

if WORKFLOW_DIR is None:
    raise ValueError('CANT GET WORKFLOW_DIR!')

# Import
inputdict = read_toml(
    os.path.join(WORKFLOW_DIR, "config.toml"))['root']['cfg']

###################################
#  SIMULATION DIRECTORY CREATION  #
# Setup

S = Simulation(**inputdict)
print(S)
S.create_specfem()
