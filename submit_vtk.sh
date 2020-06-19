#!/bin/bash

mpirun --oversubscribe -np 1 ./bin/xcombine_vol_data_vtk_adios all alpha_kl ./kernel_smooth.bp DATABASES_MPI/solver_data.bp ./ 1 1 
#mpirun --oversubscribe -np 1 ./bin/xcombine_vol_data_vtk_adios all alpha_kl ./OUTPUT_FILES/kernels.bp DATABASES_MPI/solver_data.bp ./ 1 1 
