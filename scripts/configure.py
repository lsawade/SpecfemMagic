"""

This enters the specfem directory and runs the configure script with the
appropriate options.



"""

import os
import toml
import asyncio
import subprocess


GFMAGIC_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
DATA_default = os.path.join(GFMAGIC_DIR, 'DATA_default')

# Get common valus from config
configfile = os.path.join(GFMAGIC_DIR, 'config.toml')
cfg = toml.load(configfile)['SPECFEM']


def configure():

    # Getting environment flags
    gpu = cfg['GPU']
    gpu_flags = cfg['GPU_FLAGS']
    gpu_version = cfg['GPU_VERSION']
    asdf = cfg['ASDF']
    adios = cfg['ADIOS']

    # Compilers
    cc = os.environ['CC']
    cxx = os.environ['CXX']
    mpicc = os.environ['MPICC']
    mpicxx = os.environ['MPICXX']
    fc = os.environ['FC']
    mpifc = os.environ['MPIFC']

    # FLAGS
    cflags = os.environ.get('CFLAGS') or ''
    cxxflags = os.environ.get('CXXFLAGS') or ''
    fcflags = os.environ.get('FCFLAGS') or ''

    # ADIOS
    if adios:
        adios_version = os.environ['ADIOS_VERSION']
        adios_install = os.environ['ADIOS_INSTALL']
        if int(adios_version[0]) == 1:
            adios_with = '--with-adios'
            adios_config = os.path.join(adios_install, 'bin', 'adios-config')
        elif int(adios_version[0]) == 2:
            adios_with = '--with-adios2'
            adios_config = os.path.join(adios_install, 'bin', 'adios2-config')
        else:
            raise ValueError("ADIOS version must be either 1 or 2.")



        # Combine the ADIOS configuration
        adios_conf = f'{adios_with} ADIOS_CONFIG="{adios_config}"'
    else:
        adios_conf = ''

    # ASDF
    if asdf:
        asdf_install = os.environ['ASDF_INSTALL']
        hdf5_root = os.environ['HDF5_ROOT']
        asdf_with = '--with-asdf'
        asdf_lib = f"-L{asdf_install}/usr/local/lib64 -lasdf"

        # Update flags
        cflags += f" -L{hdf5_root}/lib -I{hdf5_root}/include -lhdf5_hl -lhdf5"
        fcflags += f" -L{hdf5_root}/lib -I{hdf5_root}/include -lhdf5_hl_fortran -lhdf5_fortran"
        cxxflags += f" -L{hdf5_root}/lib -I{hdf5_root}/include -lhdf5_hl -lhdf5"

        # Combine the ASDF configuration
        asdf_conf = f'{asdf_with} ASDF_LIBS="{asdf_lib}"'
    else:
        asdf_conf = ''

    # Set compute Architecture
    if gpu == 'CPU':
        gpu_conf = ''

    # CUDA
    elif gpu == 'CUDA':

        # Get path to cuda
        import shutil
        path_to_nvcc = shutil.which('nvcc')

        if path_to_nvcc is None:
            raise ValueError("CUDA is enabled but nvcc is not in your PATH. Need nvcc to compile with CUDA and find cuda/lib64.")

        cuda_path = os.path.dirname(os.path.dirname(path_to_nvcc))

        with_gpu = f'--with-cuda={gpu_version}'
        gpu_lib =f'CUDA_LIB="{cuda_path}/lib64"'
        gpu_flags=f'CUDA_FLAGS="{gpu_flags}"'

        # Combine the gpu configuration
        gpu_conf = f'{with_gpu} {gpu_flags} {gpu_lib}'

    # HIP
    elif gpu == 'HIP':

        # Get path to hipcc
        import shutil
        path_to_hipcc = shutil.which('hipcc')

        if path_to_hipcc is None:
            raise ValueError("HIP is enabled but hipcc is not in your PATH. Need hipcc to compile with HIP and find hip/lib.")

        hip_path = os.path.dirname(os.path.dirname(path_to_hipcc))
        hip_path = os.path.join(hip_path, 'hip')

        with_gpu = f'--with-hip={gpu_version}'
        hip_inc = os.path.join(hip_path, 'include')
        hip_lib = os.path.join(hip_path, 'lib')
        gpu_flags = f'HIP_FLAGS="{gpu_flags} -L{hip_lib} -I{hip_inc}"'

        # Combine the gpu configuration
        gpu_conf = f'{with_gpu} {gpu_flags} HIP_INC="{hip_inc}" HIP_LIB="{hip_lib}"'

    else:
        raise ValueError("GPU must be either CPU, CUDA, or HIP.")

    # Configure
    confcmd = ""
    confcmd += f"./configure -C CC={cc} CXX={cxx} FC={fc} MPIFC={mpifc} "
    confcmd += f'CFLAGS="{cflags}" FCLAGS="{fcflags}" CXX="{cxxflags}" '
    confcmd += f'{gpu_conf} '
    confcmd += f'{asdf_conf} '
    confcmd += f'{adios_conf} '

    # Run configuration for forward
    forward(confcmd)

    # Run configuration for reciprocal
    reciprocal(confcmd)


def forward(confcmd):

    if not cfg['FORWARD']:
        print('Not configuring forward because set to False in config.toml')
        return

    # Print the command for testing
    sf_dir = os.environ['SF3DGF']

    # Configure
    print(72*'=')
    print(25*'=', '  FORWARD ', 25*'=')
    print(72*'=')
    configure_sf_dir(sf_dir, confcmd)


def reciprocal(confcmd):

    if not cfg['RECIPROCAL']:
        print('Not configuring reciprocal because set to False in config.toml')
        return

    # Print the command for testing
    sf_dir = os.environ['SF3DGR']

    # Configure
    print(72*'=')
    print(25*'=', '  RECIPROCAL  ', 25*'=')
    print(72*'=')
    configure_sf_dir(sf_dir, confcmd)


def configure_sf_dir(sf_dir, confcmd):

    # Make the directory clean. Try because the Makefile is made by configure,
    # so it might not exist yet.
    try:
        subprocess.run(f'cd {sf_dir} && make clean', shell=True, check=True)
        subprocess.run(f'cd {sf_dir} && make realclean', shell=True, check=True)
    except:
        pass

    # Configure
    subprocess.run(f'cd {sf_dir} && {confcmd}', shell=True, check=True)

    # Make
    subprocess.run(f'cd {sf_dir} && make -j 10 meshfem3D', shell=True, check=True)



if __name__ == '__main__':

    configure()