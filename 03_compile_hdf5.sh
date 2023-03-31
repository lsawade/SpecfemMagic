#!/bin/bash

# Get Settings
if [[ -z $SFM_ROOT ]]
then
    echo SFM_ROOT not defined please: source 00_setup.sh
    stop
fi

# HDF5 directory
cd $HDF5_MAINDIR

# Get most recent config.guess/sub
# wget -O ./bin/config.guess 'https://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.guess;hb=HEAD'
# wget -O ./bin/config.sub 'https://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.sub;hb=HEAD'

if [ -d build ]; then
    rm -rf build
fi
mkdir build
pwd
cd build
pwd

# Configuration
CC=$MPICC \
  FC=$MPIFC \
  CXX=$MPICXX \
  cmake -G "Unix Makefiles" \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_INSTALL_PREFIX=$HDF5_ROOT \
  -DHDF5_ENABLE_PARALLEL=ON  \
  -DBUILD_SHARED_LIBS=ON \
  -DHDF5_BUILD_CPP_LIB=OFF \
  -DHDF5_BUILD_FORTRAN=ON \
  -DHDF5_BUILD_JAVA=OFF \
  -DHDF5_ENABLE_THREADSAFE=OFF \
  ../hdf5-1.12.2/



# Install
make -j install

