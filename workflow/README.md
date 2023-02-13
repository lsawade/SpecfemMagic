# `nnodes` workflow for the creation of a Green Function database

This directory is used to create a Green Function database without hassle. For the generation you will need
`lwsspy.GF` package to setup reciprocal simulations and post-processing of the files that `specfem3d_globe` creates.
Then you will need a recent version of specfem that implements the `SAVE_GREEN_FUNCTIONS` option in the `Par_file`. Finally, you will nnodes to run the workflow in
`workflow.py`. `nnodes` takes care of submitting the simulations and post-processing in a reasonable manner.

Database structure is as follows

  ```
  path/to/database
  |--- Networks/
       |--- II/
            |--- BFO.h5
            |--- config.toml
            |--- N/specfem # Simulation directories
            |--- E/specfem
            |--- Z/specfem

       |--- IU/
            |--- HRV.h5
            |--- ...
  ```

The `config.toml` is really where it's at. It contains the setup for both the
nnodes workflow `nnodes` and the Green Function database setup. They can be
disentangled, but this way is easier (unless you prove me otherwise.). `job` and
`root` keys are used for the `nnodes` workflow, while the key `root.cfg`
contains the database setup. For the database configuration please check the
documentation of `lwsspy.GF` and, in particular, the `Simulation` class which
takes in all the important keys.

## Run Workflow

See `nnodes` documentation for running the workflow.

```bash
nnrun
```