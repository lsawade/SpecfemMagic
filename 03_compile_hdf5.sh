#!/bin/bash

# Get Settings
source ./00_compilations_parameters.sh

# HDF5 directory
cd $HDF5_DIR

# Get most recent config.guess/sub
# wget -O ./bin/config.guess 'https://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.guess;hb=HEAD'
# wget -O ./bin/config.sub 'https://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.sub;hb=HEAD'

if [ -d build ]; then
	rm -rf build
fi
mkdir build

echo $HDF5_DESTDIR

# Configuration
./configure --enable-shared --enable-parallel \
    --enable-fortran --enable-fortran2003 \
    --prefix=$HDF5_DESTDIR CC=$MPICC FC=$MPIF90

# Installation
make -j
# make -j check
make -j install

