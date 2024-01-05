#!/bin/bash
# Begin LSF Directives
#BSUB -P GEO111
#BSUB -W 02:00
#BSUB -nnodes 48
#BSUB -J Database
#BSUB -o lsf.%J.o
#BSUB -e lsf.%J.e
#BSUB -alloc_flags "gpumps smt1"

export MPLCONFIGDIR=${SCRATCH}/.matplotlib

module purge
module load sfmagic/reciprocal/glad-m25/128
module load sfm sfm-hdf5 sfm-adios sfm-asdf

python -c "from nnodes import root; root.run()"
