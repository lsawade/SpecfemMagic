#!/bin/env python

import os
from subprocess import check_call


def simultaneous_run() -> bool:
    try:
        with open('DATA/Par_file', 'r') as f:
            for line in f.readlines():

                if len(line.strip()) == 0 or line.strip()[0] == '#':
                    continue

                if '=' in line:
                    key, val = line.split('=')[:2]

                    if key.replace(' ', '') == 'NUMBER_OF_SIMULTANEOUS_RUNS':
                        if '#' in val:
                            val = val.split('#')[0]

                        if int(val) > 1:
                            return True
                        else:
                            return False
    except Exception as e:
        print('WARNING:', e, '--')
        return False


def sfrun(rtype: str = 's'):
    """
    rtype: m: mesh, s: spec
    """

    HOSTNAME = os.environ['HOSTNAME']
    nprocs = 1

    with open('DATA/Par_file', 'r') as f:
        for line in f.readlines():
            if '=' in line:
                key, val = line.split('=')[:2]

                if key.replace(' ', '') in ('NCHUNKS', 'NPROC_XI', 'NPROC_ETA'):
                    if '#' in val:
                        val = val.split('#')[0]

                    nprocs *= int(val)

    if "traverse" in HOSTNAME:
        if rtype == 'm':
            check_call(f'srun -n {nprocs} bin/xmeshfem3D', shell=True)
        if rtype == 's':
            check_call(f'srun -n {nprocs} bin/xspecfem3D', shell=True)

    if "batch" in HOSTNAME:
        if rtype == 'm':
            check_call(f'jsrun -n {nprocs} bin/xmeshfem3D', shell=True)
        if rtype == "s":
            check_call(f'jsrun -n {nprocs} -g 1 bin/xspecfem3D', shell=True)
