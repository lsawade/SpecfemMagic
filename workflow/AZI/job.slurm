#!/bin/bash
# Begin LSF Directives
#SBATCH -A GEO111
#SBATCH -t 00:70:00
#SBATCH -N 225
#  # SBATCH -N 2016
#SBATCH --mem=0
#SBATCH --requeue
#SBATCH -J DatabaseMaking
#SBATCH --output=database.%J.o
#SBATCH --error=database.%J.e
#SBATCH --threads-per-core=1
#SBATCH --mail-type=begin,end
#SBATCH --mail-user=lsawade@princeton.com

echo "==========================================="
echo "+++++++++++++++++++++++++++++++++++++++++++"
echo "Initializing Job"
echo "+++++++++++++++++++++++++++++++++++++++++++"
echo [$(date '+%Y-%m-%d %H:%M:%S')] "--> Purging modules"
module purge

echo [$(date '+%Y-%m-%d %H:%M:%S')] "--> Loading modules"
module load PrgEnv-cray amd-mixed cray-mpich craype-accel-amd-gfx90a
module load core-personal adios2-personal/2.9.2 hdf5-personal sf3dgf/8.0-GLAD-M50-160x160 sf3dgr/8.0-GLAD-M50-160x160

echo [$(date '+%Y-%m-%d %H:%M:%S')] "--> Activating conda environment"
source ~/miniconda3/bin/activate gf

export MPLCONFIGDIR=${SCRATCH}/.matplotlib
export OMP_NUM_THREADS=1
export PYTHONPATH=$PYTHONPATH:$ADIOS_INSTALL/lib/python3.11/site-packages/

echo "+++++++++++++++++++++++++++++++++++++++++++"
echo "Start job"
echo "+++++++++++++++++++++++++++++++++++++++++++"
echo "Running on $(hostname)"
echo "Running on [$(date '+%Y-%m-%d %H:%M:%S')]"
echo "Directory: $(pwd)"
echo "==========================================="

python -c "from nnodes import root; root.run()"

echo "==========================================="
echo "Running on $(hostname)"
echo "Running on [$(date '+%Y-%m-%d %H:%M:%S')]"
echo "Directory: $(pwd)"
echo "+++++++++++++++++++++++++++++++++++++++++++"
echo "End job"
echo "==========================================="
