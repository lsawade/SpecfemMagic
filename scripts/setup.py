"""

This file sets specfem3d for forward and reciprocal compilation. That is, it
will update the config and Par_file for specfem3d_globe so that configuration
can be done swiftly.


"""

import os
import sys
import toml
import utils

GFMAGIC_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
DATA_default = os.path.join(GFMAGIC_DIR, 'DATA_default')

# Get common valus from config
if len(sys.argv) > 1:
    configfile = sys.argv[1]
    cfg = toml.load(configfile)['SPECFEM']
else:
    configfile = os.path.join(GFMAGIC_DIR, 'config.toml')
    cfg = toml.load(configfile)['SPECFEM']

fwd_parfile_update = cfg['Par_file']['FORWARD']
rec_parfile_update = cfg['Par_file']['RECIPROCAL']


def set_model_vars(pardict: dict, cfg: dict, sf_dir: str):

    # Check if model is set to 'GLL'
    if pardict['MODEL'] != 'GLL':
        return

    # IF the model is GLL check whether a model should be copied to the
    # specfem directory
    if cfg['model_gll_location'] is None or cfg['model_gll_location'] == '':
        return

    # If path is defined, make sure to check whether GLL directory exists
    glldir = os.path.join(sf_dir, 'DATA', 'GLL')
    if not os.path.exists(glldir):
        os.makedirs(glldir)

    # Copy model to GLL directory
    import subprocess
    gllfile = os.path.join(glldir, 'model_gll.bp')
    subprocess.run(f"cp -r {cfg['model_gll_location']} {gllfile}", shell=True, check=True)

def set_gpu_vars(pardict: dict, cfg: dict):

    # GPU settings
    if cfg['GPU'] == 'CPU':
        pardict['GPU_MODE'] = False

    elif cfg['GPU'] == 'CUDA':
        pardict['GPU_MODE'] = True
        pardict['GPU_RUNTIME'] = 1
        pardict['GPU_PLATFORM'] = 'NVIDIA'
        pardict['GPU_DEVICE'] = '*'

    elif cfg['GPU'] == 'HIP':
        pardict['GPU_MODE'] = True
        pardict['GPU_RUNTIME'] = 3
        pardict['GPU_PLATFORM'] = '*' # HIP doesn't have a platform
        pardict['GPU_DEVICE'] = '*'

    else:
        raise ValueError("GPU must be either CPU, CUDA, or HIP. Or you gotta define a new version")

def set_adios_vars(pardict: dict, cfg: dict):

    pardict['ADIOS_ENABLED'] = cfg['ADIOS']
    pardict['ADIOS_FOR_FORWARD_ARRAYS'] = cfg['ADIOS']
    pardict['ADIOS_FOR_MPI_ARRAYS'] = cfg['ADIOS']
    pardict['ADIOS_FOR_ARRAYS_SOLVER'] = cfg['ADIOS']
    pardict['ADIOS_FOR_SOLVER_MESHFILES'] = cfg['ADIOS']
    pardict['ADIOS_FOR_AVS_DX'] = cfg['ADIOS']
    pardict['ADIOS_FOR_KERNELS'] = cfg['ADIOS']
    pardict['ADIOS_FOR_MODELS'] = cfg['ADIOS']
    pardict['ADIOS_FOR_UNDO_ATTENUATION'] = cfg['ADIOS']

def forward():
    """
    Set specfem3d_globe for forward compilation
    """

    # Get environment variables from environment variables
    if not cfg['FORWARD']:
        print('Not setting up forward specfem 3d_globe.')
        return

    sf_dir = os.environ['SF3DGF']

    # Par_file locations
    if 'DATA_default' in cfg and cfg['DATA_default'] != '':
        in_parfile = os.path.join(cfg['DATA_default'], "Par_file")
    else:
        in_parfile = os.path.join(DATA_default, 'Par_file')

    outparfile = os.path.join(sf_dir, 'DATA', 'Par_file')
    pardict = utils.read_par_file(in_parfile, verbose=False, savecomments=True)

    # Set parameters
    for key, value in fwd_parfile_update.items():
        if key == 'skip':
            continue
        pardict[key] = value

    # Set up model
    set_model_vars(pardict, cfg, sf_dir)

    # ADIOS
    set_adios_vars(pardict, cfg)

    # GPU settings
    set_gpu_vars(pardict, cfg)

    # Write Par_file
    utils.write_par_file(pardict, outparfile)

    # Par_file locations
    constantsfile = os.path.join(sf_dir, 'setup', 'constants.h.in')

    # Update constants file
    utils.update_constants(constantsfile, outfile=constantsfile, rotation='+',
                           external_stf=False)



def reciprocal():
    """
    Set specfem3d_globe for reciprocal compilation
    """

    if not cfg['RECIPROCAL']:
        print('Not setting up reciprocal specfem3d_globe.')
        return

    # Get environment variables from environment variables
    sf_dir = os.environ['SF3DGR']

    # Get Par_file
    if 'DATA_default' in cfg and cfg['DATA_default'] != '':
        in_parfile = os.path.join(cfg['DATA_default'], "Par_file")
    else:
        in_parfile = os.path.join(DATA_default, 'Par_file')

    outparfile = os.path.join(sf_dir, 'DATA', 'Par_file')
    pardict = utils.read_par_file(in_parfile, verbose=False, savecomments=True)

    # Set parameters
    for key, value in rec_parfile_update.items():
        if key == 'skip':
            continue
        pardict[key] = value

    # Set up model
    set_model_vars(pardict, cfg, sf_dir)

    # ADIOS
    set_adios_vars(pardict, cfg)

    # GPU settings
    set_gpu_vars(pardict, cfg)

    # Write Par_file
    utils.write_par_file(pardict, outparfile)

    # Par_file locations
    constantsfile = os.path.join(sf_dir, 'setup', 'constants.h.in')

    # Update constants file
    utils.update_constants(constantsfile, outfile=constantsfile, rotation='-',
                           external_stf=cfg['RECIPROCAL_EXTERNAL_STF'])


if __name__ == '__main__':
    forward()
    reciprocal()