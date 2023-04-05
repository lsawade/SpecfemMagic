#!/bin/bash

# Get compilation options

if [ "${RECIPROCAL}" == "True" ]
then

    # Compile specfem
    cd $SPECFEM_RECIPROCAL_DIR
    #make specfem3D -j 40
    # make clean
    #make realclean
    make all -j
    cd ..

fi

if [ "${FORWARD}" == "True" ]
then
    echo "Syncing the source code"
    echo "------------------------------------------------------"
    rsync -av specfem3d_globe/src/ specfem3d_globe_forward/src
    echo "------------------------------------------------------"

    cd $SPECFEM_DIR
    # make clean
    make all -j
    cd ..
fi
