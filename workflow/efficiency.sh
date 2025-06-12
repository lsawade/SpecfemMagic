#!/bin/bash

JOBID=$1

# Get the number of used cpus
current=$(sacct -j $JOBID -o "ReqCPUS,State" | grep RUNNING | tail -n +4 | awk '{print $1}' | awk '{s+=$1} END {print s}')

# Get the number of total cpus requested
total=$(sacct -j $JOBID -o "ReqCPUS,State" | grep RUNNING | head -3 | tail -1 | awk '{print $1}')

if [ -z $current ];
then
    
    echo No jobsteps are running

else

    # Compute efficiency
    efficiency=$((100 * $current / $total))

    # Print efficiency
    echo "Efficiency: $efficiency%"

fi
