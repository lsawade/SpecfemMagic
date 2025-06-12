#!/bin/bash
# This is a very ugly script that reads the config file separately for each
# and sets the environment variables

# This script is meant to be sourced from the root of the repository.
thisfile="$(realpath "${BASH_SOURCE[0]}")"

# Parent directory of this script's directory
GFMAGIC_DIR=$(dirname $(dirname $thisfile))

# Config file
CONFIG_FILE=$GFMAGIC_DIR/config.toml

# Big one-liner to get environment variables from config file's ENV section
txt=$(python -c "import toml; envs=toml.load(\"${CONFIG_FILE}\")[\"ENV\"]; l=[f\"{k}={v}\" for k, v in envs.items()]; print('\n'.join(l))")

echo $txt
exit
# Loop over lines
for line in $txt;
do
    # Set environment variable
    VAR=$(echo $line | cut -d'=' -f1)
    VAL=$(echo $line | cut -d'=' -f2)

    # Check if variable is empty
    if [ -z "${VAL}" ];
    then
        echo "WARNING: ${VAR} is empty. Not overwriting setting."

    # If not empty set it
    else
        echo "Setting ${VAR}=${VAL}"
        export $VAR=$VAL
    fi


done
