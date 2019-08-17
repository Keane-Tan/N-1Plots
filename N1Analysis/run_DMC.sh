#!/bin/bash

# ./run_DMC.sh dataMC_comp QCD16_Pt_80to120

NAME=$1
MACRO="datamc/$NAME.py"
OUT="$2.root"

echo "Submitting jobs for $2"


for fileID in $2

do
	if [ ! -d "outputs/$fileID" ]; then
		mkdir outputs/$fileID
	fi
	python main.py $MACRO $fileID inputTree.txt outputs/$fileID $OUT 2 >& outputs/$fileID/$2.out &
	echo "Submitted  $fileID"
done
echo Working...

wait

echo Finished.
