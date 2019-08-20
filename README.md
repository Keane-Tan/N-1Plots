# N-1Plots
Generate N-1 plots using LPC condor

We are using CMSSW_9_0_0. The files shown here were modified from https://github.com/CTFallon/FAnalysis.

# Instructions
## Using Condor to Produce ROOT Files with Histograms from Ntuples
1. voms-proxy-init --valid 192:00 -voms cms
2. cd condor
3. python FastSubmit.py

This will submit 222 jobs to lpc condor. It takes about a day for all the jobs to finish running. Do
condor_q
to check the status.
