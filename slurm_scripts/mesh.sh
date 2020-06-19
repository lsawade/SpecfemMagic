#!/bin/bash
#SBATCH --job-name=mesh_sfem
#SBATCH --output=out.mesh
# SBATCH --mail-user=lsawade@princeton.edu
#SBATCH --nodes=1
#SBATCH --ntasks=6
#SBATCH --mem=100000
#SBATCH --time=03:00:00
# SBATCH --gres=gpu:1

# Load modules
source ../00_compilations_parameters.sh

# change directory to build
cd ../specfem3d_globe

# Run Mesher
srun ./bin/xmeshfem3D
