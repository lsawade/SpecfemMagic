#!/bin/bash

# Get Variables
source 00_compilations_parameters.sh

# Download ADIOS if it doesnt exist
if [ ! -d $ADIOS_DIR ]; then

    cd $PACKAGES
    mkdir adios

    # Get ADIOS
    wget --no-check-certificate -O adios.tar.gz $ADIOS_LINK
    tar -xzvf adios.tar.gz --strip-components=1 -C $ADIOS_DIR

    cd $ROOT_DIR

fi

# Download HDF5 if it doesn't exist
if [ ! -d $HDF5_DIR ]; then

    cd $PACKAGES
    mkdir hdf5

    # Get HDF5
    wget -O hdf5.tar.gz $HDF5_LINK
    tar -xzvf hdf5.tar.gz --strip-components=1 -C $HDF5_DIR

    cd $ROOT_DIR
fi

