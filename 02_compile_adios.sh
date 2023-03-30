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
          -DADIOS2_USE_Fortran=ON \
          -DADIOS2_USE_Python=ON \
          -DADIOS2_USE_BP5=ON \
          -DADIOS2_USE_HDF5=OFF \
          -DADIOS2_USE_HDF5=OFF \
	  -DADIOS2_USE_PYTHON=ON \
	  -DPython_EXECUTABLE=$(which python3) \
          ../adios

    make -j
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

cd $SFM_ROOT
