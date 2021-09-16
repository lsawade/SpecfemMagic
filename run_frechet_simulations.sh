#!/bin/bash
# This script was originally written to run a test
# for checking the difference between the true frechet derivatives
# with respect to the source location and the ones
# that were missing a second order term.
#
# The SOURCE_DERIVATIVE_TYPE1 flag has since been removed
# from specfem. And the code will not work.
# It is kept because it contains a quite simple script that
# can test a variety of source location, and possibly
# moment tensor variations with just minor modifications.
#
# 2021.09.16 10:45 -- Lucas Sawade


# Scriptdir
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"


# Specfem
submissiondir="${SCRIPT_DIR}/submission/slurm"
specfem="${SCRIPT_DIR}/specfem3d_globe"
specfemdata="${specfem}/DATA"
outdir="${specfem}/OUTPUT_FILES"

oldparfile="${SCRIPT_DIR}/Par_file"
newparfile="${specfemdata}/Par_file"

oldcmt="${SCRIPT_DIR}/CMTSOLUTION"
newcmt="${specfemdata}/CMTSOLUTION"


# Output dirs
OUT="${SCRIPT_DIR}/outdir"

# Event parameters ( Foot of Himalaya, Andes-Pacific )
lats=( 26.8363 -24.6024 )
lons=( 87.4610 -70.4798 )

typeder=( .true. .false. )

for i in ${!lats[@]}
do
    
    # Make one directory for each event
    maindir="${OUT}/event_${i}"

    if [ ! -d $maindir ]
    then
	mkdir -p $maindir
    fi

    # Seimogram dir
    seismograms="${maindir}/seismograms"

    if [ ! -d $seismograms ]
    then
	mkdir $seismograms
    fi
    
    # Editing CMTSOLUTION
    echo "Latitude  ${lats[${i}]}"
    echo "Longitude ${lons[${i}]}"

    latitude="${lats[${i}]}"
    longitude="${lons[${i}]}"

    repl=$(printf "latitude: %18.4f" "$latitude")
    sed "s/.*latitude.*/$repl/" $oldcmt > $newcmt

    repl=$(printf "longitude: %17.4f" "$longitude")
    sed -i "s/.*longitude.*/$repl/" $newcmt

    # Check 
    diff $oldcmt $newcmt

    # Copy cmtsolution to the directory
    cp $newcmt $maindir/
    
    # Change up the seismogram game
    for j in ${typeder[@]}
    do
	if [ "${j}" == ".true." ]
	then
	    seisdir="${seismograms}/2nd"
	    echo 2nd Order Derivative
	else
	    seisdir="${seismograms}/DD"
	    echo Double Differentiation
	fi

	# Change Parfile
	repl="USE_SOURCE_DERIVATIVE_TYPE1 = ${j}"
	echo $repl
	sed "s/.*USE_SOURCE_DERIVATIVE_TYPE1.*/$repl/" $oldparfile > $newparfile

	diff $oldparfile $newparfile
	

	if [ ! -d $seisdir ]
	then
	    mkdir $seisdir
	fi

	# switch to submissiondir
	cd $submissiondir
	sbatch --wait run.sh
	cd -

	# Move computed seismograms
	mv ${outdir}/*.sac ${seisdir}/
	
    done
    

done


