#!/bin/bash

#########################
#     LOAD MODULES      #
#########################
#module purge
#module load xl spectrum-mpi cuda/9.2.148 hdf5/1.8.18 cmake boost

# module load boost
# module load pgi/19.9/64
# module load openmpi/pgi-19.9/4.0.3rc1/64
module load openmpi/gcc
module load cudatoolkit/10.0

#########################
#   DIRECOTRIES INFOS   #
#########################
ROOT_DIR=$(pwd)
PATH_CUDA=$(which nvcc)
ASDF_DIR="${ROOT_DIR}/packages/asdf-library"
ADIOS_DIR="${ROOT_DIR}/packages/adios"
HDF5_DIR="${ROOT_DIR}/packages/hdf5"

#########################
# Compilation variables #
#########################

# C/C++ compiler
CC=gcc
CXX=g++
MPICC=mpicc
FCFLAGS="-g"

# Fortran compiler
FC=gfortran
MPIFC=mpif90
CFLAGS=""

# CUDA (here CUDA 5 because my GPU cannot support more, poor boy)
CUDA_WITH="--with-cuda=cuda8"
CUDA_LIB=""

# HDF5
HDF5_LINK="https://support.hdfgroup.org/ftp/HDF5/releases/hdf5-1.8/hdf5-1.8.21/src/hdf5-1.8.21.tar"
HDF5_DESTDIR="${HDF5_DIR}/build"
HDF5_BIN="${HDF5_DESTDIR}/bin"
HDF5_LIB="${HDF5_DESTDIR}/lib"
HDF5_INCLUDE="${HDF5_DESTDIR}/include"
export PATH=$PATH:$HDF5_BIN:$HDF5_INCLUDE:$HDF5_LIB
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$HDF5_LIB:$HDF5_INCLUDE
export LIBRARY_PATH=$LIBRARY_PATH:$HDF5_LIB:$HDF5_INCLUDE

# ASDF
ASDF_LINK="https://github.com/SeismicData/asdf-library.git"
ASDF_DESTDIR="${ASDF_DIR}/build"
ASDF_WITH="--with-asdf"
ASDF_LIBS="-L${ASDF_DESTDIR}/usr/local/lib64 -lasdf"


# ADIOS
ADIOS_LINK="https://users.nccs.gov/~pnorbert/adios-1.13.1.tar.gz"
ADIOS_DESTDIR="${ADIOS_DIR}/build"
ADIOS_WITH="--with-adios"
ADIOS_CONFIG="$ADIOS_DESTDIR/bin/adios_config"
#ADIOS_CONFIG=$(which adios2-config)


