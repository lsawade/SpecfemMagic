#!/bin/bash

# Get Settings
source ./00_compilations_parameters.sh

# Sets the following
# HDF5_LINK="https ://hdf -wordpress -1.s3.amazonaws.com/\wp -content/uploads/manual/HDF5/HDF5_1_10_6 /\source/hdf5 -1.10.6. tar"
# HDF5_INSTALL_DIR="/scratch/gpfs/lsawade/hdf5"
# PREFIX="$HDF5_INSTALL_DIR/build"

cd $HDF5_DIR
ls
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
make -j check
make -j install

