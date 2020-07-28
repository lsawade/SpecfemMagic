#!/bin/bash
#SBATCH --job-name=mesh_sfem
#SBATCH --output=out.mesh
# SBATCH --mail-user=lsawade@princeton.edu
#SBATCH --nodes=1
#SBATCH --ntasks=4
#SBATCH --mem=100000
#SBATCH --time=01:00:00
# SBATCH --gres=gpu:1
#SBATCH --reservation=test

# Load modules
source ../00_compilations_parameters.sh

# change directory to build
cd ../specfem3d_globe

# Run Mesher
srun ./bin/xmeshfem3D
