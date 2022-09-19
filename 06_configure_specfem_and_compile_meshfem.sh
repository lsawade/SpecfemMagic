#!/bin/bash

# Get compilation options
source 00_compilations_parameters.sh


if [ "${RECIPROCAL}" == "True" ]
then

    # Specfem repository
    cd specfem3d_globe

    make clean
    make realclean

    # Change ADIOS BUFFER SIZE in constant.h.in
    # ini='  integer, parameter :: ADIOS_BUFFER_SIZE_IN_MB'
    # new='  integer, parameter :: ADIOS_BUFFER_SIZE_IN_MB = 15000'
    # sed -i "s/.*${ini}.*/$new/g" setup/constants.h.in

    #ini='  double precision,parameter :: COURANT_SUGGESTED = 0.55d0'
    #new='  double precision,parameter :: COURANT_SUGGESTED = 0.35d0'
    #sed -i "s/.*${ini}.*/$new/g" setup/constants.h.in

    if [ "$ASDF_WITH" == "--with-asdf" ]
    then
        FC="${HDF5_FC}"
        CC="${HDF5_CC}"
        MPIFC="${HDF5_FC}"
        MPICC="${HDF5_CC}"
        echo "ASDF enabled."
        echo "MPIFC:____$MPIFC"
        echo "MPICC:____$MPICC"
    else
        echo "No ASDF."
        echo "MPIFC:____$MPIFC"
        echo "MPICC:____$MPICC"
    fi

    # Configure
    ./configure CC=$CC CXX=$CXX FC=$FC MPIFC=$MPIFC \
    CFLAGS="$CFLAGS" FCLAGS="$FCFLAGS" \
    $CUDA_WITH CUDA_LIB="$CUDA_LIB" \
    $ASDF_WITH ASDF_LIBS="$ASDF_LIBS" \
    $ADIOS_WITH ADIOS_CONFIG="$ADIOS_CONFIG"

    # Compilation
    mpif90 -v

    ini='FLAGS_CHECK = -std=gnu -fimplicit-none -fmax-errors=10 -pedantic -pedantic-errors -Waliasing -Wampersand -Wcharacter-truncation -Wline-truncation -Wsurprising -Wno-tabs -Wunderflow -ffpe-trap=invalid,zero,overflow -Wunused -O3 -finline-functions'
    new='FLAGS_CHECK = -std=gnu -fimplicit-none -fmax-errors=10 -pedantic -pedantic-errors -Waliasing -Wampersand -Wcharacter-truncation -Wline-truncation -Wsurprising -Wno-tabs -Wunderflow -ffpe-trap=invalid,zero,overflow -Wunused -O3 -finline-functions -fbacktrace -O0 -Wall -fcheck=all'
    sed -i "s/.*${ini}.*/$new/g" Makefile

    make -j meshfem3D
    cd ..

fi


if [ "${FORWARD_TEST}" == "True" ]
then

    # Specfem repository
    cd specfem3d_globe_forward

    make clean
    make realclean

    # Change ADIOS BUFFER SIZE in constant.h.in
    # ini='  integer, parameter :: ADIOS_BUFFER_SIZE_IN_MB'
    # new='  integer, parameter :: ADIOS_BUFFER_SIZE_IN_MB = 15000'
    # sed -i "s/.*${ini}.*/$new/g" setup/constants.h.in

    #ini='  double precision,parameter :: COURANT_SUGGESTED = 0.55d0'
    #new='  double precision,parameter :: COURANT_SUGGESTED = 0.35d0'
    #sed -i "s/.*${ini}.*/$new/g" setup/constants.h.in

    if [ "$ASDF_WITH" == "--with-asdf" ]
    then
        FC="${HDF5_FC}"
        CC="${HDF5_CC}"
        MPIFC="${HDF5_FC}"
        MPICC="${HDF5_CC}"
        echo "ASDF enabled."
        echo "MPIFC:____$MPIFC"
        echo "MPICC:____$MPICC"
    else
        echo "No ASDF."
        echo "MPIFC:____$MPIFC"
        echo "MPICC:____$MPICC"
    fi

    # Configure
    ./configure CC=$CC CXX=$CXX FC=$FC MPIFC=$MPIFC \
    CFLAGS="$CFLAGS" FCLAGS="$FCFLAGS" \
    $CUDA_WITH CUDA_LIB="$CUDA_LIB" \
    $ASDF_WITH ASDF_LIBS="$ASDF_LIBS" \
    $ADIOS_WITH ADIOS_CONFIG="$ADIOS_CONFIG"

    # Compilation
    mpif90 -v

    ini='FLAGS_CHECK = -std=gnu -fimplicit-none -fmax-errors=10 -pedantic -pedantic-errors -Waliasing -Wampersand -Wcharacter-truncation -Wline-truncation -Wsurprising -Wno-tabs -Wunderflow -ffpe-trap=invalid,zero,overflow -Wunused -O3 -finline-functions'
    new='FLAGS_CHECK = -std=gnu -fimplicit-none -fmax-errors=10 -pedantic -pedantic-errors -Waliasing -Wampersand -Wcharacter-truncation -Wline-truncation -Wsurprising -Wno-tabs -Wunderflow -ffpe-trap=invalid,zero,overflow -Wunused -O3 -finline-functions -fbacktrace -O0 -Wall -fcheck=all'
    sed -i "s/.*${ini}.*/$new/g" Makefile

    make -j meshfem3D
    cd ..

fi