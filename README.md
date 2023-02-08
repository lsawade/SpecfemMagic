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

### 5. Configure specfem distros

Given a the

### 6. Compile the Mesher

```bash
06_configure_specfem_and_compile_meshfem.sh
```

After this it is important to first run the mesher before compiling the solver.

### 6. Compile Solver

```bash
06_compile_specfem.sh
```

