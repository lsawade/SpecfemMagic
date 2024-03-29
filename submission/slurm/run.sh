#!/bin/bash
#SBATCH --job-name=run_sfem
#SBATCH --output=out.run
# # SBATCH --mail-type=ALL
# # SBATCH --mail-user=lsawade@princeton.edu
#SBATCH --nodes=2
#SBATCH --ntasks=6
#SBATCH --mem=100GB
#SBATCH --ntasks-per-node=3
#SBATCH --gres=gpu:4
#SBATCH --time=00:10:00
# # SBATCH --reservation=test

# Load everything necessary
source ../../00_compilations_parameters.sh

# change directory to build
cd ../../specfem3d_globe

# Run Solver
srun -n6 --gpus-per-task=1 ./bin/xspecfem3D
