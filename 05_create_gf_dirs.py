#!/bin/env python

from lwsspy.GF.simulation import Simulation

inputdict = dict(
    # Specfem directory
    specfemdir = "specfem3d_globe",

    # Station
    network = "II",
    station = "BFO",
    station_latitude = 48.3319,
    station_longitude = 8.3311,
    station_burial = 0.0,

    # GF locations
    target_latitude = 35.0300,
    target_longitude = 26.8500,
    target_depth = 24.0000,

    #
    t0 = 0.0,
    tc = 0.0,
    duration_in_min = 20.0,
    nstep = 0.0,
    ndt = 0.0,

    # Forward parameters
    forward_test = True,
    cmtsolutionfile = CMTSOLUTION,

    # Simultaneous writing
    broadcast_mesh_model = False,
    simultaneous_runs = False
)

###################################
#  SIMULATION DIRECTORY CREATION  #
###################################


S = Simulation(**inputdict)
S.create()
