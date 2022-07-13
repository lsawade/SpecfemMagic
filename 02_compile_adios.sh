#!/bin/bash

# Get compiler options
source 00_compilations_parameters.sh



cd $ADIOS_DIR

# ADIOS2
if [ $ADIOS_VERSION == "2" ]
then
    cd $ADIOS_DIR
    mkdir $ADIOS_DESTDIR 
    cd $ADIOS_DESTDIR 
    cmake -DCMAKE_INSTALL_PREFIX=${ADIOS_DESTDIR}  \
          -DADIOS2_USE_MPI=ON \
          -DADIOS2_USE_FORTRAN=ON \
          -DADIOS2_USE_HDF5=OFF \
          -DCMAKE_Fortran_COMPILER="$FC" -DCMAKE_Fortran_FLAGS="$FCFLAGS" \
          -DCMAKE_C_COMPILER="$CC" -DCMAKE_C_FLAGS="$CFLAGS" \
          -DCMAKE_CXX_FLAGS="$CFLAGS" \
          ../adios
    make -j 16
    make install
else
    # Compile Adios1
    cd $ADIOS_DIR
    mkdir $ADIOS_DESTDIR
    mkdir build
    cd build
    ../configure CC=$CC CXX=$CXX FC=$FC  CFLAGS="$CFLAGS" --prefix="$ADIOS_DESTDIR"
    make -j
    make install
fi

cd $ROOT_DIR
