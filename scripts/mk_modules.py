"""

Depending on the dependencies, this script will expect a few
environment variables to be set. These are for example:

```
# Compilers
CC=cc
CXX=cc
MPICC=cc
MPICXX=cc
FC=ftn
MPIFC=ftn
GPU="CUDA"

# If you want ASDF/HDF5
HDF5_ROOT=/path/to/hdf5
ASDF_INSTALL=/path/to/asdf

# If you want to use ADIOS
ADIOS_INSTALL=/path/to/adios
```

Will create module file `$MODULE_PATH/sf3dgf/<version>-<tag>` for forward
specfem that sets the following environment variables (and prereqs):

```

# SPECFEM Forward location
SF3DGF=/path/to/packagedir/sf3dgf/sf_version/<tag>

```

Will create module file `$MODULE_PATH/sf3dgf/<version>-<tag>` for reciprocal
specfem that sets the following environment variables (and prereqs):
```
# SPECFEM Reciprocal location (only set if config has reciprocal true)
SF3DGR=/path/to/packagedir/sf3dgr/sf_version/<tag>

"""

import os
import toml

# Get common valus from config
filedirectory = os.path.dirname(os.path.realpath(__file__))
configfile = os.path.join(filedirectory, '..', 'config.toml')
fcfg = toml.load(configfile)
modulepath = fcfg['MAIN']['MODULE_PATH']
packagepath = fcfg['MAIN']['PACKAGE_DIR']

cfg = fcfg['SPECFEM']
version = cfg['VERSION']
tag = cfg['TAG']


def forward():

    if not cfg['FORWARD']:
        print('Not making forward module file')
        return

    module_dir = os.path.join(modulepath, 'sf3dgf')
    modulefilename = os.path.join(module_dir, cfg['VERSION'] + '-' + tag)
    sf3dgf_path = os.path.join(packagepath, 'sf3dgf', version, tag)

    filestring = ""
    filestring += "#%Module\n\n"

    filestring += "proc ModulesHelp { } {\n"
    filestring += "    puts stderr 'Module is used to set SPECFEM3D_GLOBE FORWARD related ENVs.'\n"
    filestring += "}\n"
    filestring += "\n"
    filestring += 'module-whatis "Sets ENVs for SF3D GLOBE"\n'
    filestring += "\n\n"

    filestring += "# Setting environment variables\n"
    filestring += f'setenv SF3DGF "{sf3dgf_path}"\n'

    # Make sure module_dir exists
    if not os.path.exists(module_dir):
        os.makedirs(module_dir)

    # Write module file
    with open(modulefilename, 'w') as f:
        f.write(filestring)


def reciprocal():

    if not cfg['RECIPROCAL']:
        print('Not making reciprocal module file')
        return

    module_dir = os.path.join(modulepath, 'sf3dgr')
    modulefilename = os.path.join(module_dir, cfg['VERSION']+'-'+tag)
    sf3dgr_path = os.path.join(packagepath, 'sf3dgr', version, tag)

    filestring = ""
    filestring += "#%Module\n\n"

    filestring += "proc ModulesHelp { } {\n"
    filestring += "    puts stderr 'Module is used to set compiler env vars.'\n"
    filestring += "}\n"
    filestring += "\n"
    filestring += 'module-whatis "This module is used to set all compilers etc."\n'
    filestring += "\n\n"

    filestring += "# Setting environment variables\n"
    filestring += f'setenv SF3DGR "{sf3dgr_path}"\n'

    # Make sure module_dir exists
    if not os.path.exists(module_dir):
        os.makedirs(module_dir)

    # Write module file
    with open(modulefilename, 'w') as f:
        f.write(filestring)


if __name__ == '__main__':
    forward()
    reciprocal()