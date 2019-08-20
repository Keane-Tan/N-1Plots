import os

sigList = ["base","z20","z40"] 		# list of signals to be plotted onto the N-1 plots. If you change this list, you 	 				# will need to change ../plots/N1Plots.py to make the N-1 plots.
years = ["16","17","18PRE","18POST"]

for year in years:
	for sig in sigList:
		ddir = "20" + year + "/" + sig             # destination folder
		if not os.path.exists(ddir):
			sfile = "Signal/" + sig + ".root"  # source file
			dfile = ddir + "/" + "dataMC_comp.root" # destination file
			os.system("mkdir " + ddir)			
			os.system("cp " + sfile + " " + dfile)
