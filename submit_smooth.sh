#!/bin/bash

mpirun --oversubscribe -np 6 ./bin/xlaplacian_smoothing_sem_adios 200. 200.  alpha_kl OUTPUT_FILES/kernels.bp DATABASES_MPI/ ./kernel_smooth.bp  
