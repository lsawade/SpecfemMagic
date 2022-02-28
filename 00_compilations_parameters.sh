#!/bin/bash

#########################
#     LOAD MODULES      #
#########################

# module load pgi/17.9/64
# module load openmpi/pgi-19.9/4.0.3rc1/64
if [[ $HOSTNAME == *"rhea"* ]]; then
    module purge
    module load gcc/4.8.5 openmpi/3.1.4
elif [[ $HOSTNAME == *"login"* ]]; then
    module purge
    module load gcc spectrum-mpi cuda
elif [[ $HOSTNAME == *"traverse"* ]]; then
    module purge
    module load openmpi/gcc cudatoolkit/11.6
elif [[ $HOSTNAME == "tigergpu.princeton.edu" ]]; then
    module purge
    module load openmpi/gcc cudatoolkit
else
    echo "HOST: ${HOSTNAME} not recognized."
fi


#########################
#   DIRECOTRIES INFOS   #
#########################
ROOT_DIR=$(pwd)
PACKAGES="${ROOT_DIR}/packages"
PATH_CUDA=$(which nvcc)
ASDF_DIR="${PACKAGES}/asdf-library"
ADIOS_DIR="${PACKAGES}/adios"
HDF5_DIR="${PACKAGES}/hdf5"

#########################
# Compilation variables #
#########################

# C/C++ compiler
CC=gcc
CXX=g++
MPICC=$(which mpicc)

# Fortran compiler
FC=gfortran
MPIFC=mpif90

# Compiler flags the CFLAG "-std=c++11" avoids the '''error: identifier "__ieee128" is undefined'''
CFLAGS="-std=c++11"
FCFLAGS=""

# CUDA (here CUDA 5 because my GPU cannot support more, poor boy)
CUDA_WITH="--with-cuda=cuda9"
CUDA_LIB="${PATH_CUDA/bin\/nvcc/lib64}"

# SPECFEM
SPECFEM_DIR="${ROOT_DIR}/specfem3d_globe"
SPECFEM_LINK="git@github.com:geodynamics/specfem3d_globe.git"

# HDF5
HDF5_LINK="https://support.hdfgroup.org/ftp/HDF5/releases/hdf5-1.12/hdf5-1.12.0/src/hdf5-1.12.0.tar.gz"
HDF5_DESTDIR="${HDF5_DIR}/build"
HDF5_FC="${HDF5_DESTDIR}/bin/h5pfc"
HDF5_CC="${HDF5_DESTDIR}/bin/h5pcc"
MPIFC_HDF5=$HDF5_FC

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
# ADIOS_CONFIG=$(which adios2-config)
