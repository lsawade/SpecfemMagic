#!/bin/bash
#SBATCH --job-name=run_sfem
#SBATCH --output=../out.both
# SBATCH --mail-type=ALL
#SBATCH --mail-user=lsawade@princeton.edu
# SBATCH --nodes=2
#SBATCH --ntasks=6
#SBATCH --gpus-per-task=1
#SBATCH --mem=160000
# SBATCH --ntasks-per-node=3
# SBATCH --gres=gpu:3
#SBATCH --time=00:30:00

# Load everything necessary
source ../00_compilers_and_such.sh

# Read specfem directory
if [ -z "$1" ]
then
    echo "No argument supplied. Specfem directory taken from source file"
else
    DIR=$1
fi

# change directory to build
cd $DIR

# Run Solver
srun ./bin/xmeshfem3D
srun ./bin/xspecfem3D
