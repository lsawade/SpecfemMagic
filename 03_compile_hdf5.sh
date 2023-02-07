#!/bin/bash

# Get Settings
source ./00_compilations_parameters.sh

# HDF5 directory
cd $HDF5_MAINDIR

# Get most recent config.guess/sub
# wget -O ./bin/config.guess 'https://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.guess;hb=HEAD'
# wget -O ./bin/config.sub 'https://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.sub;hb=HEAD'

if [ -d build ]; then
	rm -rf build
fi
mkdir build
pwd
echo $HDF5_DIR

# Configuration
./configure --enable-shared --enable-parallel --enable-trace --enable-debug \
    --enable-fortran --enable-fortran2003 \
    --prefix=$HDF5_DIR CC=$MPICC FC=$MPIF90

# Installation
make -j
# make -j check
make -j install

