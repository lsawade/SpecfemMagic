#!/bin/bash
#SBATCH --job-name=mesh_sfem
#SBATCH --output=out.mesh
# SBATCH --mail-user=lsawade@princeton.edu
# SBATCH --nodes=2
#SBATCH --ntasks=24
#SBATCH --cpus-per-task=4
#SBATCH --ntasks-per-core=1
#SBATCH --mem=100GB
#SBATCH --time=00:20:00
# SBATCH --gres=gpu:1
#SBATCH --reservation=test


# Load modules
source ../../00_compilations_parameters.sh

# change directory to build
cd ../../specfem3d_globe

# Run Mesher
srun ./bin/xmeshfem3D
