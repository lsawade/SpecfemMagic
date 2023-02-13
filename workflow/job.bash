#!/bin/bash
#SBATCH -J Database-maker
#SBATCH -t 03:00:00
#SBATCH -N 2
#SBATCH --ntasks-per-node=32
#SBATCH --cpus-per-task=4
#SBATCH --ntasks-per-core=1
#SBATCH --gres=gpu:4
#SBATCH --mem=200GB
#SBATCH -o db.slurm.%J.o.txt
#SBATCH -e db.slurm.%J.e.txt

cd /scratch/gpfs/lsawade/SpecfemMagicGF/
source ./00_compilations_parameters.sh
cd /home/lsawade/thirdparty/python/ph5py-testing
source vars.sh
cd /scratch/gpfs/lsawade/SpecfemMagicGF/workflow


python -c "from nnodes import root; root.run()"
