#!/bin/bash

#!/bin/bash
if [[ -n $SFM_ROOT ]]
then
    echo "'SFM_ROOT' is already set to $SFM_ROOT"
    echo "check the loaded modules using module list"

else
    echo "Loading all module and setting environment variables."

    thisdir=$(realpath $(dirname "${BASH_SOURCE[0]}"))
    export MODULEPATH=$thisdir/modules:$MODULEPATH

    module load sfm sfm-hdf5 sfm-adios sfm-asdf

fi