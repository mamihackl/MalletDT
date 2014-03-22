#!/bin/bash
ul='_'
ext=$3$ul$4
accfile=$acc$ext
modelfile=$5$ext
sysfile=$6$ext
timelog='time.'

START=$SECONDS
./DTlearner.py $1 $3 $4 $modelfile
./DTclassifier.py $1 $2 $modelfile $sysfile 
END=$SECONDS
DIFF=$(($END-$START))
echo ''$accfile: Processing time $DIFF seconds'' > $timelog$accfile

