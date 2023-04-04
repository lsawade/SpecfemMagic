#!/bin/env python

import os
from python.runsf import sfrun

# Current dir
cwd = os.path.abspath(os.getcwd())
specfemdir = os.environ['SPECFEM_RECIPROCAL_DIR']

print("Running the mesher reciprocal...")
os.chdir(specfemdir)
# sfrun(rtype='m')./
os.chdir(cwd)


if os.environ['FORWARD'] == 'True':
    specfemdir = os.environ['SPECFEM_DIR']

    os.chdir(specfemdir)
    print("Running the mesher forward test...")
    sfrun(rtype='m')
    os.chdir(cwd)
