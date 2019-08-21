# N-1Plots
Generate N-1 plots using LPC condor

We are using CMSSW_9_0_0. The files shown here were modified from https://github.com/CTFallon/FAnalysis.

# Instructions
## Using Condor to Produce ROOT Files with Histograms from Ntuples
Start your terminal, do kinit and ssh into cmslpc. cd into CMSSW_9_0_0, do cmsenv, and git clone the repository.
```
1. voms-proxy-init --valid 192:00 -voms cms
2. cd condor
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
