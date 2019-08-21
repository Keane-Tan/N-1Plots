# N-1Plots
Generate N-1 plots using LPC condor

We are using CMSSW_9_0_0. The files shown here were modified from https://github.com/CTFallon/FAnalysis.
All ntuple files were stored at root://cmseos.fnal.gov//store/user/lpcsusyhad/SusyRA2Analysis2015/Run2ProductionV17/

# Instructions
## Using Condor to Produce ROOT Files with Histograms from Ntuples
Start your terminal, do kinit and ssh into cmslpc. cd into CMSSW_9_0_0, do cmsenv, and git clone the repository.
```
1. voms-proxy-init --valid 192:00 -voms cms
2. cd N-1Plots/condor
3. python FastSubmit.py
```
This will submit 222 jobs to lpc condor. It takes about a day for all the jobs to finish running. Do
```
condor_q
```
to check the status.

## Transferring output ROOT files to local directory
When all the jobs are done (no more running or held jobs), then cd into the local directory of this repository,
```
1. cd OutputRoot
2. python ChangeHistName.py
3. python hadd.py
4. python CopySig.py
```
## Producing N-1 Plots
```
1. cd ../plots
2. python N1Plots.py -b
```
The plots should be in the folders whose names are the years when the data were taken.

# Brief Explanation of What Each Script Does
FastSubmit.py - there are many ntuple files (~58,000, see condor/N1Analysis/input_conf/inputRoot_fullRun2.py) involved in this analysis. These files were broken into 222 groups (QCD16_Pt_80to120, TTJets17_DiLepy_genMET_150, etc.). This script submit a job to condor for each group. The output files (a ROOT file and an .out file for troubleshooting) from each job was automatically transferred to root://cmseos.fnal.gov//store/user/keanet/CondorOutput/MCRoot (see N-1PLots/condor/RunCondor.sh).

ChangeHistName.py - the way the code was written, the branch names of one output ROOT file are different from those of the other ROOT files. This script makes all the branch names the same and saves the changed files to the current directory sorted by year and background type (QCD, TTJets, etc.).

hadd.py - hadd all the files with the same background, say QCD16, but different pT or HT bins into a single background ROOT file.

CopySig.py - copy the relevant signal files from the Signal directory to the year directories, so that it is straightforward to use the plotting code to make the N-1 plots.

N1Plots.py - plot the N-1 plots, where each variable was plotted after the preselection cuts was applied to all other variables in the preselection. For example, if MET is plotted, all the Jet cuts, Delta Eta cut, and lepton veto are applied. See condor/N1Analysis/macros/datamc/dataMC_comp.py for detail.
