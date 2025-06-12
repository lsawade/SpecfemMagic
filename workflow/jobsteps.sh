#!/bin/bash

JOBID=$1
format="JobID%20,ReqCPUS,TotalCPU,Elapsed,NodeList%30,State"

sacct -j $JOBID -o $format | grep RUNNING | head
echo "     :            :              :                 :             "
sacct -j $JOBID -o $format | grep RUNNING | tail
