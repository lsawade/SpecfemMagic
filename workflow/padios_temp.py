#!/usr/bin/env python

from gf3d.postprocess_mpi import Adios2HDF5
import sys


def processadios(h5file, Nfile, Efile, Zfile, config_file, precision, compression):



    # Processing I/O
    print("Processing I/O and Params", flush=True)
    print("-------------------------", flush=True)
    print("    H5", h5file, flush=True)
    print("     N", Nfile, flush=True)
    print("     E", Efile, flush=True)
    print("     Z", Zfile, flush=True)
    print("   CFG", config_file, flush=True)
    print("     P", precision, flush=True)
    print("     C", compression, flush=True)


    with Adios2HDF5(
            h5file,
            Nfile,
            Efile,
            Zfile,
            config_file, subspace=False,
            precision=precision,
            compression=compression,  # 'gzip',
            compression_opts=None,
            comm=None) as A2H:

        A2H.write()


# Get input!
if len(sys.argv) != 8:
    raise ValueError

h5file, Nfile, Efile, Zfile, config_file, precision, compression = \
    sys.argv[1:]

processadios(h5file, Nfile, Efile, Zfile,
             config_file, precision, compression)
