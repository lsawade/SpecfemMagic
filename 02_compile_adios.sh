#!/bin/bash

# Get compiler options
source 00_compilations_parameters.sh



cd $ADIOS_DIR

# ADIOS2
if [ $ADIOS_VERSION == "2" ]
then
    cd $ADIOS_DIR
    mkdir $ADIOS_BUILD 
    cd $ADIOS_BUILD 
    CC="$(which mpicc)" CXX="$(which mpicxx)" MPICC="$(which mpicc)" \
    cmake -DCMAKE_INSTALL_PREFIX=${ADIOS_INSTALL}  \
          -DADIOS2_USE_MPI=ON \
          -DADIOS2_USE_FORTRAN=ON \
          -DADIOS2_USE_HDF5=OFF \
          ../adios
    make -j 16
    make install
else
    # Compile Adios1
    cd $ADIOS_DIR
    mkdir $ADIOS_BUILD
    mkdir build
    cd build
    ../configure CC=$CC CXX=$CXX FC=$FC  CFLAGS="$CFLAGS" --prefix="$ADIOS_INSTALL"
    make -j
    make install
fi

cd $ROOT_DIR
