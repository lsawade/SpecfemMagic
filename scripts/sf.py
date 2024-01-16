import os
import click
from math import ceil
@click.group()
def cli():
    pass


@cli.command('create')
@click.argument('specfemdir', type=click.Path(exists=True))
@click.argument('simdir', type=click.Path(exists=False))
@click.option('--parfile', type=click.Path(exists=True), default=None)
@click.option('--stationsfile', type=click.Path(exists=True), default=None)
@click.option('--cmtfile', type=click.Path(exists=True), default=None)
@click.option('--forcefile', type=click.Path(exists=True), default=None)
def create(specfemdir, simdir,
           parfile=None,
           stationsfile=None,
           cmtfile=None,
           forcefile=None):

    import subprocess

    # Create simdir
    import shutil
    shutil.rmtree(simdir, ignore_errors=True)
    os.makedirs(simdir, exist_ok=True)
    os.makedirs(os.path.join(simdir, 'DATA'), exist_ok=True)
    os.makedirs(os.path.join(simdir, 'OUTPUT_FILES'), exist_ok=True)

    # Link database files and binaries
    subprocess.run(f'ln -s {specfemdir}/bin {simdir}/bin', shell=True, check=True)
    subprocess.run(f'ln -s {specfemdir}/DATABASES_MPI {simdir}/DATABASES_MPI', shell=True, check=True)

    # Copy Parfile
    if parfile is not None:
        subprocess.run(f'cp {parfile} {simdir}/DATA/Par_file', shell=True, check=True)
    else:
        if os.path.exists(f'{specfemdir}/DATA/Par_file'):
            subprocess.run(f'cp {specfemdir}/DATA/Par_file {simdir}/DATA/Par_file', shell=True, check=True)
        else:
            print('No Par_file file found in specfemdir, so not copied!!!')

    # Copy station file either from new file or from directory
    if stationsfile is not None:
        subprocess.run(f'cp {stationsfile} {simdir}/DATA/STATIONS', shell=True, check=True)
    else:
        if os.path.exists(f'{specfemdir}/DATA/STATIONS'):
            subprocess.run(f'cp {specfemdir}/DATA/STATIONS {simdir}/DATA/STATIONS', shell=True, check=True)
        else:
            print('No STATIONS file found in specfemdir, so not copied!!!')

    # Copy cmtfile file either from new file or from directory
    if cmtfile is not None:
        subprocess.run(f'cp {cmtfile} {simdir}/DATA/CMTSOLUTION', shell=True, check=True)
    else:
        if os.path.exists(f'{specfemdir}/DATA/CMTSOLUTION'):
            subprocess.run(f'cp {specfemdir}/DATA/CMTSOLUTION {simdir}/DATA/CMTSOLUTION', shell=True, check=True)
        else:
            print('No CMTSOLUTION file found in specfemdir, so not copied!!!')

    # Copy cmtfile file either from new file or from directory
    if forcefile is not None:
        subprocess.run(f'cp {forcefile} {simdir}/DATA/FORCESOLUTION', shell=True, check=True)
    else:
        if os.path.exists(f'{specfemdir}/DATA/FORCESOLUTION'):
            subprocess.run(f'cp {specfemdir}/DATA/FORCESOLUTION {simdir}/DATA/FORCESOLUTION', shell=True, check=True)
        else:
            print('No FORCE file found in specfemdir, so not copied!!!')


@cli.command('run')
@click.argument('specfemdir', type=click.Path(exists=True))
@click.option('--runtype', type=str, default='s', help='m: mesh, s: spec')
def run(specfemdir: str, runtype: str):
    import os

    # Get currentdir
    curr_dir = os.getcwd()

    # Go to specfemdir
    os.chdir(specfemdir)
    print(f"Enter: {specfemdir}")

    # Run
    sfrun(rtype=runtype)

    # Return to original dir
    os.chdir(curr_dir)
    print(f"Going back to: {curr_dir}")


def sfrun(rtype: str = 's', mps: int | None = None):
    """
    rtype: m: mesh, s: spec
    """
    from subprocess import run

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

    print(f"HOSTNAME: {HOSTNAME}; NPROC: {nprocs}; RUNTYPE: {rtype}")

    if "traverse" in HOSTNAME:
        if rtype == 'm':
            run(f'srun -n {nprocs} bin/xmeshfem3D', shell=True, check=True)
        if rtype == 's':
            run(f'srun -n {nprocs} bin/xspecfem3D', shell=True, check=True)

    if 'frontier' in HOSTNAME or 'login' in HOSTNAME:

        print(HOSTNAME, nprocs, rtype)

        if rtype == 'm':
            N = int(ceil(nprocs/62))
            run(f'srun -n {nprocs} -c1 --cpu-bind=cores bin/xmeshfem3D', shell=True, check=True)
        if rtype == 's':
            N = int(ceil(nprocs/7))
            run(f'srun -n {nprocs} -c1 --distribution=*:block --ntasks-per-gpu=7 --cpu-bind=cores --gpu-bind=closest bin/xspecfem3D', shell=True, check=True)

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
    cli()