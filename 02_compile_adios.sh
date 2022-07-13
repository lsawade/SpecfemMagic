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
