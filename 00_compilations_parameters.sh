#!/bin/bash

#########################
#     LOAD MODULES      #
#########################

# module load pgi/17.9/64
# module load openmpi/pgi-19.9/4.0.3rc1/64
if [[ $HOSTNAME == *"rhea"* ]]; then

    module purge
    module load gcc/4.8.5 openmpi/3.1.4
    export CUDA_WITH="--with-cuda=cuda8"

elif [[ $HOSTNAME == *"login"* ]] || [[ $HOSTNAME == *"batch"* ]]; then

    module purge
    module load xl spectrum-mpi cuda cmake boost

    # NVIDIA Tesla V100
    export CUDA_WITH="--with-cuda=cuda9"

elif [[ $HOSTNAME == *"traverse"* ]]; then

    module purge
    module load anaconda3
    conda activate gf
    # module load openmpi/gcc/4.1.1/64 cudatoolkit/11.1
    module load openmpi/gcc/4.0.4/64 cudatoolkit/11.1

    # NVIDIA Tesla V100
    export CUDA_WITH="--with-cuda=cuda9"

elif [[ $HOSTNAME == *"tiger"* ]]; then

    module purge
    module load openmpi/gcc cudatoolkit/10.2

    # NVIDIA P100
    export CUDA_WITH="--with-cuda=cuda8"

elif [[ $HOSTNAME == *"della-gpu"* ]]; then

    module purge
    module load anaconda3/2021.11
    module load gcc/8 openmpi/gcc/4.1.2 cudatoolkit/11.7
    conda activate gf

    # NVIDIA A100E
    export CUDA_WITH="--with-cuda=cuda11"

else
    echo "HOST: ${HOSTNAME} not recognized."
fi


#########################
#   DIRECOTRIES INFOS   #
#########################
export ROOT_DIR=$(pwd)
export PACKAGES="${ROOT_DIR}/packages"
export PATH_CUDA=$(which nvcc)
export ASDF_DIR="${PACKAGES}/asdf-library"
export ADIOS_DIR="${PACKAGES}/adios"
export HDF5_MAINDIR="${PACKAGES}/hdf5"
export WORKFLOW_DIR="${ROOT_DIR}/workflow"


#########################
# Green Function stuff  #
#########################

export RECIPROCAL=True
export FORWARD_TEST=True

#########################
# Compilation variables #
#########################

# C/C++ compiler
export CC=gcc
export CXX=g++
export MPICC=$(which mpicc)

# Fortran compiler
export FC=gfortran
export MPIFC=mpif90

# Compiler flags the CFLAG "-std=c++11" avoids the '''error: identifier "__ieee128" is undefined'''
# gfortran     ifort         effect
# ------------------------------------------------------
# -g           -g            Stores the code inside the binary
# -O0          -O0           Disables optimisation
# -fbacktrace  -traceback    More informative stack trace
# -Wall        -warn all     Enable all compile time warnings
# -fcheck=all  -check all    Enable run time checks

export CFLAGS=""
export CXXFLAGS="" # -std=c++11
export FCFLAGS="-g -O0 -fbacktrace -Wall -fcheck=all"

# CUDA (here CUDA 5 because my GPU cannot support more, poor boy)
export CUDA_LIB="${PATH_CUDA/bin\/nvcc/lib64}"

# SPECFEM
export SPECFEM_DIR="${ROOT_DIR}/specfem3d_globe"
export SPECFEM_LINK="git@github.com:lsawade/specfem3d_globe.git"
export SPECFEM_BRANCH="GF"

# HDF5
export HDF5_LINK="https://support.hdfgroup.org/ftp/HDF5/releases/hdf5-1.10/hdf5-1.10.9/src/hdf5-1.10.9.tar.gz"
export HDF5_DIR="${HDF5_MAINDIR}/build"
export HDF5_FC="${HDF5_DESTDIR}/bin/h5pfc"
export HDF5_CC="${HDF5_DESTDIR}/bin/h5pcc"

# HDF5 PLUGINS
export HDF5_PLUGINS_LINK="https://support.hdfgroup.org/ftp/HDF5/releases/hdf5-1.10/hdf5-1.10.9/plugins/hdf5_plugins-1_10_9.tar.gz"
export HDF5_PLUGINS_MAINDIR="${PACKAGES}/hdf5_plugins"
export LZF_MAINDIR="${PACKAGES}/lzflib"
export LZF_DIR="${PACKAGES}/lzflib/build"


export MPIFC_HDF5=$HDF5_FC
export PATH=${HDF5_DESTDIR}/bin:${PATH}

# ASDF
export ASDF_LINK="https://github.com/SeismicData/asdf-library.git"
export ASDF_DESTDIR="${ASDF_DIR}/build"
export ASDF_WITH="" #--with-asdf"
export ASDF_LIBS="-L${ASDF_DESTDIR}/usr/local/lib64 -lasdf"

# ADIOS
export ADIOS_VERSION="2"
export ADIOS_LINK="https://github.com/ornladios/ADIOS2.git"
export ADIOS_BUILD="${PACKAGES}/adios-build"
export ADIOS_INSTALL="${PACKAGES}/adios-install"

# ADIOS version specific things
if [ $ADIOS_VERSION == "2" ]
then
    ADIOS_WITH="--with-adios2"
    ADIOS_CONFIG="${ADIOS_INSTALL}/bin/adios2_config"
else
    ADIOS_WITH="--with-adios"
    ADIOS_CONFIG="${ADIOS_INSTALL}/bin/adios_config"
fi
export PATH=$PATH:${ADIOS_INSTALL}/bin

