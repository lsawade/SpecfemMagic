#!/bin/bash
#SBATCH --job-name=run_sfem
#SBATCH --output=out.run
# SBATCH --mail-type=ALL
# SBATCH --mail-user=lsawade@princeton.edu
# SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --gpus-per-task=1
#SBATCH --mem=160000
# SBATCH --ntasks-per-node=3
# SBATCH --gres=gpu:1
#SBATCH --time=00:10:00
#SBATCH --reservation=test
#SBATCH -C rh8

# Load everything necessary
source ../00_compilations_parameters.sh

# change directory to build
cd ../specfem3d_globe

# Run Solver
srun ./bin/xspecfem3D
