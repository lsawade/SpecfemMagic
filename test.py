import numpy as np
import sys
import adios2
from mpi4py.MPI import COMM_WORLD as comm
import h5py

infile, outfile = sys.argv[1], sys.argv[2]

rank = comm.Get_rank()
size = comm.Get_size()
i = rank

NSTEPS = 3725
# To access rank specific variables
# Only store things if there are points

with (adios2.open(infile, 'r', comm) as F, h5py.File(outfile, 'w', driver='mpio', comm=comm) as G):



    if rank == i:

        NGLOBSLICES = F.read(f'NGLOB')
        NGLOBTOTAL = np.sum(NGLOBSLICES)
        NGLOB = NGLOBSLICES[i]
        CNGLOB = np.hstack((np.array([0]), np.cumsum(NGLOBSLICES)))

        displacement_ds = G.create_dataset(
            f'displacement/N/array', (3, NGLOBTOTAL, NSTEPS),
            dtype=np.float16)


        displacement = np.zeros(
            (3, NGLOB, NSTEPS),
            dtype=np.float16)

        key = f'displacement'

        local_dim = F.read(f'{key}/local_dim')[i]
        offset = F.read(f'{key}/offset')[i]

        displacement_ds[:, CNGLOB[i]:CNGLOB[i+1], :] = F.read(
            f'{key}/array', start=[offset],
            count=[3*NGLOB],
            step_start=0, step_count=NSTEPS,
            block_id=0).transpose().reshape(3, NGLOB,NSTEPS, order='F')

        print(f"RANK {i:03d} -- NG: {NGLOB:7d} :: ", np.mean(displacement), flush=True)



