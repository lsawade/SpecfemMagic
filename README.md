# SpecfemMagic

This repo contains a bunch of scripts that download, configure, and compile
specfem as well as specfem for the generation of a Green function database.

It differs slightly from `main` in the sense that `main` is really aimed towards
the compilation, and forward modelling of specfem and not for the reciprocal
modeling.

It's currently a mix and match between Python and Bash scripts because I'm
slowly but steadily transitioning to Python for this package, but it was all
written in Bash originally

## Main configuration files

As of recently, the setup has changed to a more environment module type of setup.
The main reason for this is that I'm constantly reusing the packages that I
install such as ADIOS, HDF5, ASDF.

So after setting
```bash
export MODULEPATH=/path/to/specfemmagic/modules:$MODULEPATH
```

You should be able to just load the modules after installing them, so that

```bash
module load sfm       # loads base environment variables
module load sfm-hdf5  # loads HDF5 environment variables and sets path
module load sfm-asdf  # loads ASDF environment variables and sets path
module load sfm-adios # loads ADIOS environment variables and sets path
```

Now it is important to realize that these statements only set paths as you can
see in for example
```bash
module show sfm-hdf5
```

If you have multiple specfem magics and want to compile specfem in a variety of ways
you can create a super module that loads the module path to the specfem directories.
Here specfem magic is explicitly located at `${HOME}/GFMagic`

A sample would look like this:

```tcl
#%Module

proc ModulesHelp { } {
   puts stderr "Adds to Module path and loads sfmagic for reciprocal glad m25 with 128x128"
}

module-whatis "Module gets paths for installed specfem. Afterwards you can load sfm, sfm-hdf5, sfm-adios, sfm-asdf"

set MODULEPATH $::env(MODULEPATH)
set HOME $::env(HOME)

pushenv MODULEPATH "$MODULEPATH:$HOME/GFMagic/modules"
```

If you place it under the name
```bash
${HOME}/Modules/modulefiles/sfmagic/reciprocal/glad-m25/128```
```
and export the path to the modules
```bash
export MODULEPATH=${HOME}/Modules/modulefiles:$MODULEPATH
```
then you can load separate specfemmagics from the commandline to setup new
simulation directories and use the subpackages like so:

```bash
module load sfmagic/reciprocal/glad-m25/128
module load sfm sfm-hdf5 sfm-adios sfm-asdf
```

Again this only sets variables and paths, the installation scripts still have to be run to actually use these packages.

I know not a lot of people are familiar with module files, but maybe it suffices
to say that they are very neat ways of modifying, e.g., the PATH  variable, and
when unloading the module unsetting it.

### `00_compilations_parameters.sh`

Check out `00_compilations_parameters.sh`. It contains setups for most major
machines that Princeton affiliated people are using. Tiger, Traverse, Della, and
Summit. For each of the systems, a set of modules and compilers are loaded
separately. This file is used as a basis for the rest of the scripts `01_..` -
`10_...`.

For drastic changes to the compilation of `specfem3d_globe` you will have to
change not only files `00_..`, but also
`06_configure_specfem_and_compile_meshfem.sh` and `08_compile_specfem.sh`.

### `config.toml`

The `config.toml` really is the setup file for the reciprocal database
computation. It is used to change both the `Par_file`,
`constants.h.in` in `specfem3d_globe`, and add a `stf`, `GF_LOCATIONS` file for
the downsampled source time function, and the element tagging respectively.


## How To

All scripts except from `01_ge..` use the `00_compilations_parameters.sh`. To
install specfem given the parameters in that file. Run the numbered scripts
sequentially.

### 1. Get the necessary repos

```bash
01_get_repositories.sh
```

### 2. Compile ADIOS (optional)
```bash
02_compile_adios.sh
```

### 3. Compile HDF5 for ASDF (optional)
```bash
03_compile_hdf5.sh
```

### 4. Compile ASDF (optional)
```bash
04_compile_asdf.sh
```

### 5. Set up the specfem3d_globe simulation directories for configuration

Uses the `WORKFLOW_DIR` flag to get the database `config.toml` and creates
reciprocal specfem distribution (and forward distribution if wanted).

### 6. Compile the Mesher

```bash
06_configure_specfem_and_compile_meshfem.sh
```

After this it is important to first run the mesher before compiling the solver.


### 7. Run mesher

Runs mesher for both reciprocal (and optionally forward directories).

```bash
07_compile_specfem.sh
```

### 8. Compile Solver

```bash
08_compile_specfem.sh
```

### 9. Update the station information

Before meshing, we don't really know the timestep, so this script gets the
timestep from specfem and defines subsampling rate and source time function from
specfem.

```bash
08_compile_specfem.sh
```

### 10. Runs the solver

Runs the solver for both forward and reciprocal databases.
```bash
10_runsolver.py
```

