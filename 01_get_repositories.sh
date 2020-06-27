#!/bin/bash

# Get Variables
source 00_compilations_parameters.sh

# Launch this script once to get specfem3d_globe developement version,
# a patched asdf-library (pull-request is on-going) sources and adios 1 sources
CURRENT_DIR=$(pwd)
SPECFEM_DIR="specfem3d_globe"
PACKAGE_DIR="packages"

# First get specfem3d_globe repository
if [ ! -d $SPECFEM_DIR ]; then
        git clone https://github.com/geodynamics/specfem3d_globe.git
        cd specfem3d_globe
        git checkout -b devel origin/devel
        cd ..
fi

# Then get ASDF and ADIOS 1 repository
if [ ! -d $PACKAGE_DIR ]; then
        # Create package dir
        mkdir -p $PACKAGE_DIR
        cd $PACKAGE_DIR
	mkdir adios
	mkdir hdf5

        # Get ADIOS
	wget -O adios.tar.gz $ADIOS_LINK 
	tar -xzvf adios.tar.gz --strip-components=1 -C $ADIOS_DIR
	
	# Get HDF5
	wget -O hdf5.tar.gz $HDF5_LINK
	tar -xzvf hdf5.tar.gz --strip-components=1 -C $HDF5_DIR 

        # Get ASDF
        git clone $ASDF_LINK
fi

