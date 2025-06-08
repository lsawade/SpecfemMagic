#!/bin/bash

#########################
#     LOAD MODULES      #
#########################

# module load pgi/17.9/64
# module load openmpi/pgi-19.9/4.0.3rc1/64

EMC_WITH="--with-emc"
COMPILER=INTEL

if [[ $HOSTNAME == *"tiger"* ]]; then
    
    module purge
    

    if [[ $COMPILER == "GNU" ]]; then
    
        module load openmpi/gcc

        # C
        CC=gcc
        MPICC=$(which mpicc)    

        # C++
        CXX=g++
        MPICXX=$(which mpicxx)

        # Fortran compiler
        FC=gfortran
        MPIFC=$(which mpif90)

    else
        echo "Compiler ${COMPILER} not recognized for ${HOSTNAME}. Please set it to GNU."
        unset CC CXX FC MPICC MPICXX MPIFC
        module purge
        echo "Exiting..."
        exit 1
    fi

    module load cudatoolkit/10.2

    # NVIDIA P100
    CUDA_WITH="--with-cuda=cuda8"


# DELLA and EMC that is compile with netcdf
elif [[ ( $HOSTNAME == *"della-gpu"* ) && ( $EMC_WITH == "--with-emc" ) ]]; then
     
    module purge
    
    if [[ $COMPILER == "INTEL" ]]; then
    
        module load intel-oneapi/2024.2
        module load intel-mpi/oneapi/2021.13
        module load hdf5/oneapi-2024.2/1.14.4
        module load netcdf/oneapi-2024.2/hdf5-1.14.4/4.9.2
    
        # C
        CC=icx
        MPICC=$(which mpicc)    
    
        # C++
        CXX=icx
        MPICXX=$(which mpicxx)
        
        # Fortran compiler
        FC=ifx
        MPIFC=$(which mpif90)

     
    elif [[ $COMPILER == "GNU" ]]; then
    
        module load gcc-toolset/14
        module load openmpi/gcc/4.1.6
        module load hdf5/gcc/1.14.4             
        module load netcdf/gcc/hdf5-1.14.4/4.9.2

        # C
        CC=gcc
        MPICC=$(which mpicc)    

        # C++
        CXX=g++
        MPICXX=$(which mpicxx)

        # Fortran compiler
        FC=gfortran
        MPIFC=$(which mpif90)

    else
        echo "Compiler ${COMPILER} not recognized. Please set it to INTEL or GNU."
        unset CC CXX FC MPICC MPICXX MPIFC
        module purge
        echo "Exiting..."
        exit 1
    fi

    module load cudatoolkit/12.8
    
    # NVIDIA Ampere A100 
    CUDA_WITH="--with-cuda=cuda11"

    # NETCDF SETUP
    NETCDF_WITH="--with-netcdf"
    NETCDF_INC="${NETCDFDIR}/include"
    NETCDF_LIBS="-L${NETCDFDIR}/lib"
    FCFLAGS="-lnetcdff -lnetcdf ${FCFLAGS}"
    
elif [[ $HOSTNAME == *"della-gpu"* ]]; then

    module purge
    module load anaconda3/2021.11
    
    conda activate gf
    # NVIDIA A100E 
    CUDA_WITH="--with-cuda=cuda11"


    module purge
    
    if [[ $COMPILER == "INTEL" ]]; then
    
        module load intel-oneapi/2024.2
        module load intel-mpi/oneapi/2021.13
    
        # C
        CC=icx
        MPICC=$(which mpicc)    
    
        # C++
        CXX=icx
        MPICXX=$(which mpicxx)
        
        # Fortran compiler
        FC=ifx
        MPIFC=$(which mpif90)

     
    elif [[ $COMPILER == "GNU" ]]; then
    
        module load gcc-toolset/14
        module load openmpi/gcc/4.1.6

        # C
        CC=gcc
        MPICC=$(which mpicc)    

        # C++
        CXX=g++
        MPICXX=$(which mpicxx)

        # Fortran compiler
        FC=gfortran
        MPIFC=$(which mpif90)

    else
        echo "Compiler ${COMPILER} not recognized. Please set it to INTEL or GNU."
        unset CC CXX FC MPICC MPICXX MPIFC
        module purge
        echo "Exiting..."
        exit 1
    fi

    module load cudatoolkit/12.8
    
    # NVIDIA Ampere A100 
    CUDA_WITH="--with-cuda=cuda11"
 
    
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
# Green Function stuff  #
#########################

export RECIPROCAL=True
export FORWARD_TEST=True

#########################
# Compilation variables #
#########################



# Compiler flags the CFLAG "-std=c++11" avoids the '''error: identifier "__ieee128" is undefined'''
# gfortran     ifort         effect
# ------------------------------------------------------
# -g           -g            Stores the code inside the binary
# -O0          -O0           Disables optimisation
# -fbacktrace  -traceback    More informative stack trace
# -Wall        -warn all     Enable all compile time warnings
# -fcheck=all  -check all    Enable run time checks


CFLAGS=""
#FCFLAGS="-g -O0 -fbacktrace -Wall -fcheck=all"
FCFLAGS="${FCFLAGS} -g -O0 -fbacktrace"

# CUDA (here CUDA 5 because my GPU cannot support more, poor boy)

CUDA_LIB="${PATH_CUDA/bin\/nvcc/lib64}"

# SPECFEM
SPECFEM_DIR="${ROOT_DIR}/specfem3d_globe"
SPECFEM_LINK="git@github.com:SPECFEM/specfem3d_globe.git"
SPECFEM_BRANCH="devel"

# HDF5
HDF5_LINK="https://support.hdfgroup.org/ftp/HDF5/releases/hdf5-1.12/hdf5-1.12.0/src/hdf5-1.12.0.tar.gz"
HDF5_DESTDIR="${HDF5_DIR}/build"
HDF5_FC="${HDF5_DESTDIR}/bin/h5pfc"
HDF5_CC="${HDF5_DESTDIR}/bin/h5pcc"
MPIFC_HDF5=$HDF5_FC
export PATH=$PATH:${HDF5_DESTDIR}/bin

# ASDF
ASDF_LINK="https://github.com/SeismicData/asdf-library.git"
ASDF_DESTDIR="${ASDF_DIR}/build"
ASDF_WITH="" #--with-asdf"
ASDF_LIBS="-L${ASDF_DESTDIR}/usr/local/lib64 -lasdf"

# ADIOS
ADIOS_VERSION="2"

ADIOS_BUILD="${PACKAGES}/adios-build"
ADIOS_INSTALL="${PACKAGES}/adios-install"

# ADIOS version specific things
if [ $ADIOS_VERSION == "2" ]
then
    ADIOS_WITH="--with-adios2"
    ADIOS_CONFIG="${ADIOS_INSTALL}/bin/adios2-config"
    ADIOS_LINK="https://github.com/ornladios/ADIOS2.git"
else
    ADIOS_WITH="--with-adios"
    ADIOS_CONFIG="${ADIOS_INSTALL}/bin/adios_config"
    ADIOS_LINK="http://users.nccs.gov/~pnorbert/adios-1.13.1.tar.gz"
fi
export PATH=$PATH:${ADIOS_INSTALL}/bin

