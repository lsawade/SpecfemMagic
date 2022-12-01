# SpecfemMagic

This repo contains a bunch of scripts that download, configure, and compile
specfem as well as specfem related packages.

## Main compilation parameters

Check out `00_compilations_parameters.sh`.


## How to

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

### 5. Compile the Mesher

```bash
05_configure_specfem_and_compile_meshfem.sh
```

After this it is important to first run the mesher before compiling the solver.

### 6. Compile Solver

```bash
06_compile_specfem.sh
```

