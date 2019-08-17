import os
import time

years = ["16","17","18PRE","18POST"]
bkg = ["QCD", "TTJets", "WJets", "ZJets"]

for iyear in range(len(years)):
	direc1 = "20" + years[iyear]

	for ibkg in range(len(bkg)):
		direc2 = direc1 + "/" + bkg[ibkg] + years[iyear] + "/"
		filelist = os.listdir(direc2)		

		print direc2

		# to avoid hadd-ing the existing dataMC_comp.root file
		if os.path.exists(direc2 + "dataMC_comp.root"):
			os.system("rm " + direc2 + "dataMC_comp.root")
			print("Deleting existing dataMC_comp.root file...")

	for ibkg in range(len(bkg)):
		direc2 = direc1 + "/" + bkg[ibkg] + years[iyear] + "/"
		filelist = os.listdir(direc2)		

		print direc2

		command = "hadd "+ direc2 +"dataMC_comp.root "	
		for ifile in range(len(filelist)):
			command = command + direc2 + filelist[ifile] + " "  

		os.system(command)

