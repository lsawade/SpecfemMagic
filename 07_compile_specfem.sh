#!/bin/bash

# Get compilation options
source 00_compilations_parameters.sh

echo "PATH:\n$PATH"
echo "LD PATH:\n$LD_LIBRARY_PATH"
echo "LIB PATH:\n$LIBRARY_PATH"

# Compile specfem
cd specfem3d_globe
#make specfem3D -j 40
#make clean
#make realclean
make all -j
cd ..

