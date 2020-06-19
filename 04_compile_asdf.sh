#!/bin/bash

# Get compiler options
source 00_compilations_parameters.sh

H5PFC="${HDF5_DESTDIR}/bin/h5pfc"
H5PCC="${HDF5_DESTDIR}/bin/h5pcc"

# Install ASDF
cd $ASDF_DIR
ls
if [ -d build ]; then
	rm -rf build
fi
mkdir build
cd build

echo $LD_LIBRARY_PATH

cmake .. -DCMAKE_Fortran_COMPILER="${H5PFC}" -DCMAKE_Fortran_FLAGS="$FCFLAGS"\
         -DCMAKE_C_COMPILER="${H5PCC}" -DCMAKE_C_FLAGS="$CFLAGS" \
         -DCMAKE_CXX_FLAGS="$CFLAGS" \
         -DBoost_NO_SYSTEM_PATHS=TRUE
make
make doc
make install DESTDIR="$ASDF_DESTDIR"

cd $ROOT_DIR

