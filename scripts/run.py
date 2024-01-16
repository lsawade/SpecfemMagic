#!/bin/env python

import os
from subprocess import check_call, run


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


def sfrun(rtype: str = 's', mps: int | None = None):
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

    print(f"HOSTNAME: {HOSTNAME}")
    print(f"Number of processors: {nprocs}")

    if "traverse" in HOSTNAME:
        if rtype == 'm':
            run(f'srun -n {nprocs} bin/xmeshfem3D', shell=True, check=True)
        if rtype == 's':
            run(f'srun -n {nprocs} bin/xspecfem3D', shell=True, check=True)

    if 'frontier' in HOSTNAME or 'login' in HOSTNAME:

        print(HOSTNAME)

        if rtype == 'm':
            run(f'srun -n {nprocs} bin/xmeshfem3D', shell=True, check=True)
        if rtype == 's':
            run(f'srun -n {nprocs} --gpus-per-task=1 --gpu-bind=closest bin/xspecfem3D', shell=True, check=True)

    if "batch" in HOSTNAME:

        if mps is not None:
            r = mps
            n = int(nprocs/r)
            g = 1
        else:
            r, n, g = nprocs, 1, 1

        if rtype == 'm':
            run(f'jsrun -n {nprocs} bin/xmeshfem3D', shell=True, check=True)
        if rtype == "s":
            run(f'jsrun -n {r} -a {n} -c {n} -g {g} bin/xspecfem3D', shell=True, check=True)



if __name__ == '__main__':

    import os,sys

    # Get currentdir
    curr_dir = os.getcwd()


    # Get Specfem dir from command line
    sfdir = sys.argv[1]

    # Go to specfemdir
    os.chdir(sfdir)
    print(f"Enter: {sfdir}")

    # Get sim type m, or s
    simtype = sys.argv[2]

    # Run
    sfrun(rtype=simtype)

    # Return to original dir
    os.chdir(curr_dir)
    print(f"Going back to: {sfdir}")