#!/bin/env python

import os
from runsf import sfrun

# Current dir
cwd = os.path.abspath(os.getcwd())
specfemdir = 'specfem3d_globe'

print("Running the mesher reciprocal...")
os.chdir(specfemdir)
sfrun(rtype='m')
os.chdir(cwd)


if os.environ['FORWARD_TEST'] == 'True':
    specfemdir = 'specfem3d_globe_forward'

    os.chdir(specfemdir)
    print("Running the mesher forward test...")
    sfrun(rtype='m')
    os.chdir(cwd)
