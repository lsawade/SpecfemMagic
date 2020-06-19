#!/bin/bash

for i in $(ls OUTPUT_FILES/*.ascii)
do
	infile=$i
	file=${i/.sem.ascii/.adj}
	oufile=${file/OUTPUT_FILES/SEM}
	#echo -ne "cp $infile $oufile\n"
	cp -v $infile $oufile
done
