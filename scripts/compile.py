import os
import sys
import toml
import asyncio
from asyncio.subprocess import PIPE, STDOUT
import subprocess


GFMAGIC_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
DATA_default = os.path.join(GFMAGIC_DIR, 'DATA_default')

# Get common valus from config
if len(sys.argv) > 1:
    configfile = sys.argv[1]
    cfg = toml.load(configfile)['SPECFEM']
else:
    configfile = os.path.join(GFMAGIC_DIR, 'config.toml')
    cfg = toml.load(configfile)['SPECFEM']


def sync_src(sfdir_1: str, sfdir_2: str):
    """Syncs the src folder between two specfem directories"""

    subprocess.run(f'rsync -Pcauv {sfdir_1}/src/ {sfdir_2}/src/', shell=True, check=True)
    subprocess.run(f'rsync -Pcauv {sfdir_2}/src/ {sfdir_1}/src/', shell=True, check=True)


async def run_cmd(cmd):

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


async def compile_task(sf_dir, cmd, ctype='forward'):

    print(f'--> Compiling SPECFEM3D_GLOBE for {ctype} directory')

    # Download SPECFEM if it doesnt exist
    cmd = f'cd {sf_dir} && {cmd}'

    await run_cmd(cmd)

    print(f'    Compiling {ctype} done.')



async def compile():

    print('Starting compilations')

    if cfg['FORWARD']:
        sf3dgf_dir = os.environ['SF3DGF']
    
    if cfg['RECIPROCAL']:
        sf3dgr_dir = os.environ['SF3DGR']

    if cfg['FORWARD'] and cfg['RECIPROCAL']:
        sync_src(sf3dgf_dir, sf3dgr_dir)

    cmd = 'make -j 10 all'

    async with asyncio.TaskGroup() as tg:
        if cfg['FORWARD']:
            fw_task = tg.create_task(compile_task(sf3dgf_dir, cmd, ctype='forward'))
        if cfg['RECIPROCAL']:
            rc_task = tg.create_task(compile_task(sf3dgr_dir, cmd, ctype='reciprocal'))

    print("Compilation done.")

if __name__ == '__main__':

    asyncio.run(compile())