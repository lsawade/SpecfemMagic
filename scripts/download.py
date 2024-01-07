"""
Download the specfem3d_globe package to $SFG3DF (and/or $SF3DGR if reciprocal
wanted)
"""

import os
import toml
import asyncio
from asyncio.subprocess import PIPE, STDOUT

# Get common valus from config
filedirectory = os.path.dirname(os.path.realpath(__file__))
configfile = os.path.join(filedirectory, '..', 'config.toml')
fcfg = toml.load(configfile)
modulepath = fcfg['MAIN']['MODULE_PATH']
packagepath = fcfg['MAIN']['PACKAGE_DIR']

cfg = fcfg['SPECFEM']
version = cfg['VERSION']
tag = cfg['TAG']
link = cfg['LINK']
branch = cfg['BRANCH']

async def download(sf_dir, link, dtype='forward'):

    print(f'--> Downloading SPECFEM3D_GLOBE for {dtype} directory')


    # Download SPECFEM if it doesnt exist
    cmd = f'git clone {link} {sf_dir}'

    # Create process
    proc = await asyncio.create_subprocess_shell(
        cmd, stdout=PIPE, stderr=PIPE)

    # Await process
    stdout, stderr = await proc.communicate()

    # Print output if there was an error
    if proc.returncode != 0:
        print(f'[{cmd!r} exited with {proc.returncode}]')
        if stdout:
            print(f'[stdout]\n{stdout.decode()}')
        if stderr:
            print(f'[stderr]\n{stderr.decode()}')

    print(f'    Downloading {dtype} done.')

async def checkout(sf_dir, branch, ctype='forward'):

    print(f'--> Checking out {ctype} branch: {branch}')


    # Download SPECFEM if it doesnt exist
    cmd = f'git checkout {branch}'

    # Create process
    proc = await asyncio.create_subprocess_shell(
        cmd, stdout=PIPE, stderr=PIPE, cwd=sf_dir)

    # Await process
    stdout, stderr = await proc.communicate()

    # Print output if there was an error
    if proc.returncode != 0:
        print(f'[{cmd!r} exited with {proc.returncode}]')
        if stdout:
            print(f'[stdout]\n{stdout.decode()}')
        if stderr:
            print(f'[stderr]\n{stderr.decode()}')

    print(f'    Checking out {ctype} branch done.')


async def forward():

    if not cfg['FORWARD']:
        print('Not download SPECFEM for forward module file')
        return

    # Get environment variables from environment variables
    sf_dir = os.environ['SF3DGF']

    # Download SPECFEM if it doesnt exist and checkout branch
    await download(sf_dir, link, dtype='forward')
    await checkout(sf_dir, branch, ctype='forward')


async def reciprocal():

    if not cfg['RECIPROCAL']:
        print('Not download SPECFEM for reciprocal module file')
        return

    # Get environment variables from environment variables
    sf_dir = os.environ['SF3DGR']

    # Download SPECFEM if it doesnt exist and checkout branch
    await download(sf_dir, link, dtype='reciprocal')
    await checkout(sf_dir, branch, ctype='reciprocal')

async def main():

    print('Getting specfem3d_globe')

    async with asyncio.TaskGroup() as tg:
        fw_task = tg.create_task(forward())
        rc_task = tg.create_task(reciprocal())

    print("Downloads done")


if __name__ == '__main__':

    asyncio.run(main())