# the root files created in N1Analysis all have different branch names unfortunately; this script is to change all the branch names to the same names so that I can hadd the files correctly.
import ROOT as rt

met = rt.TH1F()
MTwmetR = rt.TH1F()
MTwoutmetR = rt.TH1F()
metR = rt.TH1F()
dPhi = rt.TH1F()
dEta = rt.TH1F()
nE = rt.TH1F()
nM = rt.TH1F()

histList = [met, MTwmetR, MTwoutmetR, metR, dPhi, dEta, nE, nM]
varList = ["MET", "MT_with_METMT_Cut", "MT_without_METMT_Cut", "metR", "DeltaPhiMin_AK8", "DeltaEta", "NElectrons", "NMuons"]

ffile = open('fileIDList.txt','r+')
fileIDList = ffile.readlines()
baseloc = "root://cmseos.fnal.gov//store/user/keanet/CondorOutput/MCRoot/"

for i in range(len(fileIDList)):
	fileID = fileIDList[i][:-1] # [:-1] cuts off the "\n" character
	filename = fileID + ".root"
	outfilename = filename

	if "QCD16" in fileID:
		bkgname = "QCD16"
		outfilename = "2016/QCD16/" + outfilename
	elif "QCD17" in fileID:
		bkgname = "QCD17"
		outfilename = "2017/QCD17/" + outfilename
	elif "QCD18PRE" in fileID:
		bkgname = "QCD18PRE"
		outfilename = "2018PRE/QCD18PRE/" + outfilename
	elif "QCD18POST" in fileID:
		bkgname = "QCD18POST"
		outfilename = "2018POST/QCD18POST/" + outfilename
	elif "TTJets16" in fileID:
		bkgname = "TTJets16"
		outfilename = "2016/TTJets16/" + outfilename
	elif "TTJets17" in fileID:
		bkgname = "TTJets17"
		outfilename = "2017/TTJets17/" + outfilename
	elif "TTJets18PRE" in fileID:
		bkgname = "TTJets18PRE"
		outfilename = "2018PRE/TTJets18PRE/" + outfilename
	elif "TTJets18POST" in fileID:
		bkgname = "TTJets18POST"
		outfilename = "2018POST/TTJets18POST/" + outfilename
	elif "WJets16" in fileID:
		bkgname = "WJets16"
		outfilename = "2016/WJets16/" + outfilename
	elif "WJets17" in fileID:
		bkgname = "WJets17"
		outfilename = "2017/WJets17/" + outfilename
	elif "WJets18PRE" in fileID:
		bkgname = "WJets18PRE"
		outfilename = "2018PRE/WJets18PRE/" + outfilename
	elif "WJets18POST" in fileID:
		bkgname = "WJets18POST"
		outfilename = "2018POST/WJets18POST/" + outfilename
	elif "ZJets16" in fileID:
		bkgname = "ZJets16"
		outfilename = "2016/ZJets16/" + outfilename
	elif "ZJets17" in fileID:
		bkgname = "ZJets17"
		outfilename = "2017/ZJets17/" + outfilename
	elif "ZJets18PRE" in fileID:
		bkgname = "ZJets18PRE"
		outfilename = "2018PRE/ZJets18PRE/" + outfilename
	elif "ZJets18POST" in fileID:
		bkgname = "ZJets18POST"
		outfilename = "2018POST/ZJets18POST/" + outfilename
	else:
		bkgname = fileID
		outfilename = "Signal/" + outfilename

	_outFile = rt.TFile.Open(outfilename, "RECREATE")
	_file = rt.TFile.Open(baseloc+filename,"READ")

	for ientry in range(len(varList)):
		_file.GetObject(varList[ientry] + "_" + fileID,histList[ientry])
		histList[ientry].SetName(varList[ientry]+"_"+bkgname)
		_outFile.cd()
		histList[ientry].Write()

	_file.Close()
	_outFile.Close()

ffile.close()
