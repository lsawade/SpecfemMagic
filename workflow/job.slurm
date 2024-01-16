#!/bin/bash
# Begin LSF Directives
#SBATCH -A GEO111
#SBATCH -t 01:01:00
#SBATCH -N 12
#SBATCH -J DatabaseMaking
#SBATCH --output=database.%J.o
#SBATCH --error=database.%J.e
#SBATCH --threads-per-core=1


module purge
module load PrgEnv-cray amd-mixed cray-mpich craype-accel-amd-gfx90a
module load core-personal adios2-personal hdf5-personal sf3dgf/8.0-GLAD-M35-256x256 sf3dgr/8.0-GLAD-M35-256x256

export MPLCONFIGDIR=${SCRATCH}/.matplotlib
export OMP_NUM_THREADS=1

source ~/miniconda3/bin/activate gf

python -c "from nnodes import root; root.run()"
