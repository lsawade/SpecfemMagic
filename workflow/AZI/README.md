# Azimuthal anisotropy stuff.


1. Moved the model to GLL_AZI instead of GLL
2. Par_files are updated depending on the RUNTIME using scripts/setup.py
3. CurrentlyDATA_Default in the main GFMagic directory is used, but this
   will change in the future.
4. $SF3DGF is the base forward directory, $SF3DR is the base Forward simulation
5. To make an actual testdatabase and forward directory please use scripts/create_reciprocal_station.py

