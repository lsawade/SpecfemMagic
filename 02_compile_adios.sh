#!/bin/bash

# Get compiler options
source 00_compilations_parameters.sh

# Compile Adios
cd $ADIOS_DIR
mkdir $ADIOS_DESTDIR
mkdir build
cd build
../configure CC=$CC CXX=$CXX FC=$FC  CFLAGS="$CFLAGS" --prefix="$ADIOS_DESTDIR"
make -j
make install
cd $ROOT_DIR


