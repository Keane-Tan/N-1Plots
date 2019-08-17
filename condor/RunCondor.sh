#!/bin/bash

mkdir kAnalysis
cd kAnalysis

source /cvmfs/cms.cern.ch/cmsset_default.sh  ## if a tcsh script, use .csh instead of .sh
export SCRAM_ARCH=slc6_amd64_gcc530
eval `scramv1 project CMSSW CMSSW_9_0_0`
cd CMSSW_9_0_0/src/
eval `scramv1 runtime -sh` # cmsenv is an alias not on the workers
echo "CMSSW: "$CMSSW_BASE

OUT="$1.root"
OUTDIR=root://cmseos.fnal.gov//store/user/keanet/CondorOutput

# transfering macro files
xrdcp -s $OUTDIR/N1Analysis.tgz .
tar -xf N1Analysis.tgz # untarring the tar ball
echo "After cd-ing into CMSSW_9_0_0/src and ls-ing"
ls

cd N1Analysis
./run_DMC.sh dataMC_comp $1

cd outputs

for fileID in $1
do
	echo "xrdcp -f $fileID/$OUT ${OUTDIR}/$OUT"
	xrdcp -f $fileID/$1.out $OUTDIR/MCRoot/$1.out
	xrdcp -f $fileID/$OUT $OUTDIR/MCRoot/$OUT 2>&1
done


# Remove everything
cd ${_CONDOR_SCRATCH_DIR}
rm -rf kAnalysis

