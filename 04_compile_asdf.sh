#!/bin/bash

# Get compiler options
if [[ -z $SFM_ROOT ]]
then
    echo SFM_ROOT not defined please: source 00_setup.sh
    stop
fi

# Install ASDF
cd $ASDF_DIR
ls

if [ -d build ]; then
	rm -rf build
fi

mkdir build
cd build

cmake .. -DCMAKE_Fortran_COMPILER="$HDF5_FC" -DCMAKE_Fortran_FLAGS="$FCFLAGS" \
      -DCMAKE_C_COMPILER="$HDF5_CC" -DCMAKE_C_FLAGS="$CFLAGS" \
      -DCMAKE_CXX_FLAGS="$CFLAGS"

make
make doc
make install DESTDIR="$ASDF_DESTDIR"

cd $SFM_ROOT

