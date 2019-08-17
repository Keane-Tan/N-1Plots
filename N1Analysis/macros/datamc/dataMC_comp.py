from analysisBase import baseClass
import ROOT as rt
import tdrstyle
from array import array

rt.gROOT.SetBatch(True)
rt.gStyle.SetOptTitle(1)
tdrstyle.setTDRStyle()

def loop(self):
	# set up trees or chains
	#f = rt.TFile.Open(self.inputFileList[0])
	#tree = f.Get(self.treeNameList[0])
	
	tree = self.getChain(self.treeNameList[0])

	# added friend tree
	nEvents = tree.GetEntries()
	print("n events = " + str(nEvents))


	# initalize histograms to be made, or create Friend tree to be filled
	self.outRootFile.cd()

	metx = 1500
	MTx = 6000
	metRx = 0.45
	phix = 3.3
	etax = 3.5

	# list of branches to plot
	plotDict = {#key = var name, value = [varType, nBins, binLow, binHigh, title]
				# varType can be "s" - single value (ie 'MET')
				#				 "sF" - single value, but a function of (not sure if this exists, but just in case)
				#				 "vA" - vector, all values (ie 'JetsAK8_girth')
				#				 "vI" - vector, only index value (ie 'JetsAK8_girth[0]')
				#				 "vAF" - vector, all values but function (ie 'JetsAK8.Pt()' - Pt of all ak8 Jets)
				#				 "vIF" - vector, indexed function (ie 'JetsAK8[0].Pt()', only Pt of leading AK8 Jet)
				#				 "vR", "vRF
	
	'MET':["s",100,0,metx*1.01,self.fileID+";MET; Events"],
	'MT_with_METMT_Cut':["s",100,0,MTx*1.01,self.fileID+"; M_{T} ; Events"],
	'MT_without_METMT_Cut':["s",100,0,MTx*1.01,self.fileID+"; M_{T} ; Events"],
	'metR':["spec",100,0,metRx*1.01,self.fileID+";MET/M_{T};Events"],
	'DeltaPhiMin_AK8':["s",100,0,phix*1.01,self.fileID+";#Delta#phi_{min};Events"],
	'DeltaEta':["spec",100,0,etax*1.01,self.fileID+";#Delta#eta(j_{1},j_{2});Events"],
	'NElectrons':["spec",5,0,5,self.fileID+";NElectrons;Events"],
	'NMuons':["spec",5,0,5,self.fileID+";NMuons (miniIso<0.4);Events"]
	}

	branchList = tree.GetListOfBranches()
	branchListNames = []
	for thing in branchList:
		branchListNames.append(thing.GetName())
	tree.SetBranchStatus("*",0)
	tree.SetBranchStatus("RunNum" ,1)
	tree.SetBranchStatus("madHT",1)
	tree.SetBranchStatus("GenElectrons",1)
	tree.SetBranchStatus("GenMuons",1)
	tree.SetBranchStatus("GenTaus",1)
	tree.SetBranchStatus("GenMET",1)
	tree.SetBranchStatus("MT_AK8",1)
	tree.SetBranchStatus("Jets",1)
	tree.SetBranchStatus("fixedGridRhoFastjetAll",1)
	tree.SetBranchStatus("NVtx",1)
	tree.SetBranchStatus("MET",1)
	tree.SetBranchStatus("DeltaPhiMin_AK8",1)
	tree.SetBranchStatus("JetsAK8",1)
	tree.SetBranchStatus("JetsAK8_ID",1)
	tree.SetBranchStatus("TrueNumInteractions",1)	
	tree.SetBranchStatus("Muons_MiniIso",1)
	tree.SetBranchStatus("NElectrons",1)
	tree.SetBranchStatus("globalSuperTightHalo2016Filter",1)
	tree.SetBranchStatus("HBHENoiseFilter",1)
	tree.SetBranchStatus("HBHEIsoNoiseFilter",1)
	tree.SetBranchStatus("BadPFMuonFilter",1)
	tree.SetBranchStatus("BadChargedCandidateFilter",1)
	tree.SetBranchStatus("EcalDeadCellTriggerPrimitiveFilter",1)
	tree.SetBranchStatus("eeBadScFilter",1)

	for plotVar in plotDict.keys():
		if plotVar.split("[")[0] in branchListNames:
			tree.SetBranchStatus(plotVar.split("[")[0],1)
		else:
			print(plotVar.split("[")[0] +" not in tree")

	if (("Jets" in self.fileID) or ("QCD" in self.fileID)): # only need to do this for MC bkg
		tree.SetBranchStatus("Weight",1)		# activate puWeight, puSysUp, puSysDown branches
		tree.SetBranchStatus("puWeight",1)

		if "16" in self.fileID:
			lumi = 35921.036
			print("2016 Lumi")
		elif "17" in self.fileID:
			lumi = 41521.331
			print("2017 Lumi")
		elif "18PRE" in self.fileID:
			lumi = 21071.460
			print("2018 pre Lumi")
		elif "18POST" in self.fileID:
			lumi = 38621.232
			print("2018 post Lumi")
		elif "18" in self.fileID:
			lumi = 59692.692
			print("2018 full lumi")
		else:
			print("Dont know what total lumi to use. default to 40 fb-1")
			lumi = 40000.
	else:
		lumi = 1
	histDict = {}

	for plotVar, histSpecs in plotDict.items():
		histDict[plotVar] = self.makeTH1F(plotVar+"_"+self.fileID,histSpecs[4],histSpecs[1],histSpecs[2],histSpecs[3]) 
	for iEvent in range(nEvents):
		if iEvent%1000 == 0:
			print("Event: " + str(iEvent) + "/" + str(nEvents))
		tree.GetEvent(iEvent)


		if "TT" in self.fileID:
			if self.stitchTT(tree.GetFile().GetName().split("/")[-1], tree.madHT, len(tree.GenElectrons),len(tree.GenMuons), len(tree.GenTaus), tree.GenMET, self.fileID):
				continue		
		
		if (("Jets" in self.fileID) or ("QCD" in self.fileID)): # or ("ST1" in self.fileID)): # Bkg MC get tree weight, data and signal MC get weight == 1
			weight = (tree.Weight)*(tree.puWeight)
		else: 
			weight = 1.

		# HEMVeto definition: AK4 jets with pt>30, -3.05<eta<-1.35, and -1.62<phi<-0.82$.
		jets = tree.Jets
		nJet = len(jets)

		if "18" in self.fileID:
			if (("PRE" in self.fileID) and ("Data" in self.fileID) and (tree.RunNum >= 319077)):
				continue
			elif "POST" in self.fileID:
				HEMOptVetoFilter = 1
				for ijet4 in range(nJet):
					jet_i = jets[ijet4]
					if jet_i.Pt()>30 and -3.05<jet_i.Eta()<-1.35 and -1.62<jet_i.Phi()<-0.82:
						HEMOptVetoFilter = 0
				if ( ( ("Data" in self.fileID) and (tree.RunNum < 319077) ) or (HEMOptVetoFilter == 0) ):
					continue

		### important variables		
		FJets = tree.JetsAK8
		FJetID = tree.JetsAK8_ID
		nFJets = len(FJets)
		MET = tree.MET
		MT = tree.MT_AK8		
		dPhiMin = tree.DeltaPhiMin_AK8
		gSTH = tree.globalSuperTightHalo2016Filter
		HBHEN = tree.HBHENoiseFilter
		HBHEIN = tree.HBHEIsoNoiseFilter
		BPFM = tree.BadPFMuonFilter
		BCC = tree.BadChargedCandidateFilter
		EDCTP = tree.EcalDeadCellTriggerPrimitiveFilter
		eeBS = tree.eeBadScFilter
		nV = tree.NVtx

		# Applying MET Filters
		if not(gSTH == 1 and HBHEN == 1 and HBHEIN == 1 and BPFM == 1 and BCC == 1 and EDCTP == 1 and eeBS == 1 and nV > 0):
			continue
		
		# Applying N-1 Preselection cuts (MT cut is excluded)

		## FJets cut
		if nFJets < 2:
			continue
		elif FJets[0].Pt() <= 200 or abs(FJets[0].Eta()) >= 2.4 or (not FJetID[0]):
			continue
		elif FJets[1].Pt() <= 200 or abs(FJets[1].Eta()) >= 2.4 or (not FJetID[1]):
			continue

		### Important variables
		deltaEta = abs(FJets[0].Eta()- FJets[1].Eta())
		metR = MET/MT
		nElec = tree.NElectrons
		mmIso = tree.Muons_MiniIso
		nMuon = 0

		### Counting the number of loose muon
		if (mmIso.size() > 0):
			for imm in range(mmIso.size()):
				if mmIso[imm] < 0.4:
					nMuon += 1

		## All cuts besides Delta eta
		if metR > 0.15 and nElec == 0 and nMuon == 0:
			if deltaEta > etax:
				histDict['DeltaEta'].Fill(etax,weight*lumi)
			else:
				histDict['DeltaEta'].Fill(deltaEta,weight*lumi)
		
		## All cuts besides MET/MT
		if deltaEta < 1.5 and nElec == 0 and nMuon == 0:
			if metR > metRx:
				histDict['metR'].Fill(metRx,weight*lumi)
			else:
				histDict['metR'].Fill(metR,weight*lumi)

		## All cuts besides MET/MT (MET)
		if deltaEta < 1.5 and nElec == 0 and nMuon == 0:
			if MET > metx:
				histDict['MET'].Fill(metx,weight*lumi)
			else:
				histDict['MET'].Fill(MET,weight*lumi)

		## All cuts (MT)
		if metR > 0.15 and deltaEta < 1.5 and nElec == 0 and nMuon == 0:
			if MT > MTx:
				histDict['MT_with_METMT_Cut'].Fill(MTx,weight*lumi)
			else:
				histDict['MT_with_METMT_Cut'].Fill(MT,weight*lumi)

		## All cuts besides MET/MT cut (MT)
		if deltaEta < 1.5 and nElec == 0 and nMuon == 0:
			if MT > MTx:
				histDict['MT_without_METMT_Cut'].Fill(MTx,weight*lumi)
			else:
				histDict['MT_without_METMT_Cut'].Fill(MT,weight*lumi)

		## All cuts (Delta phi min)
		if metR > 0.15 and deltaEta < 1.5 and nElec == 0 and nMuon == 0:
			if dPhiMin > phix:
				histDict['DeltaPhiMin_AK8'].Fill(phix,weight*lumi)
			else:
				histDict['DeltaPhiMin_AK8'].Fill(dPhiMin,weight*lumi)

		## All cuts besides nElec
		if deltaEta < 1.5 and metR > 0.15 and nMuon == 0:
			if nElec > 5:
				histDict['NElectrons'].Fill(5,weight*lumi)
			else:
				histDict['NElectrons'].Fill(nElec,weight*lumi)


		## All cuts besides nMuon
		if deltaEta < 1.5 and metR > 0.15 and nElec == 0:
			if nMuon > 5:
				histDict['NMuons'].Fill(5,weight*lumi)
			else:
				histDict['NMuons'].Fill(nMuon,weight*lumi)

def addLoop():
	baseClass.loop = loop
