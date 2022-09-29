#!/bin/bash

# Get compilation options
source 00_compilations_parameters.sh

echo "PATH:\n$PATH"
echo "LD PATH:\n$LD_LIBRARY_PATH"
echo "LIB PATH:\n$LIBRARY_PATH"

if [ "${RECIPROCAL}" == "True" ]
then

    # Compile specfem
    cd specfem3d_globe
    #make specfem3D -j 40
    # make clean
    #make realclean
    make all -j
    cd ..

fi

if [ "${FORWARD_TEST}" == "True" ]
then
    echo "Syncing the source code"
    echo "------------------------------------------------------"
    rsync -av specfem3d_globe/src/ specfem3d_globe_forward/src
    echo "------------------------------------------------------"

    cd specfem3d_globe_forward
    # make clean
    make all -j
    cd ..
fi
