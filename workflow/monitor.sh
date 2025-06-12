#!/bin/bash

JOBID=$1

squeue -u lsawade -o "%.14i %.24j %.9P %.2t%.10M %.6D %.21S %.15R"
echo 
echo ----------------------------------
echo

./efficiency.sh $JOBID

echo
echo ----------------------------------
echo

./jobsteps.sh $JOBID
