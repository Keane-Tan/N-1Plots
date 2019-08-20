# -*- coding: utf-8 -*-
import ROOT as rt
import sys
import os

def norm(hist):
	if hist.Integral(0,hist.GetNbinsX()) > 0:
		hist.Scale(1.0/hist.Integral(0,hist.GetNbinsX())) # normalizing the histograms

sbL = ['QCD', 'TTJets', 'WJets', 'ZJets','z20', 'base', 'z40']
yearlist = ["16","17","18PRE","18POST"]

t20 = rt.TH1F()
tB = rt.TH1F()
t40 = rt.TH1F()
tQ = rt.TH1F()
tT = rt.TH1F()
tZ = rt.TH1F()
tW = rt.TH1F()
tS = rt.TH1F()
tempHist = {"QCD":tQ,"TTJets":tT,"WJets":tW,"ZJets":tZ,"z20":t20,"base":tB,"z40":t40}

varList = {
	'MET':["MET [GeV]"],
	'MT_with_METMT_Cut':["M_{T}"],
	'MT_without_METMT_Cut':["M_{T}"],
	'metR':["MET/M_{T}"],
	'DeltaPhiMin_AK8':["#Delta#phi_{min}"],
	'DeltaEta':["#Delta#eta(j_{1},j_{2})"],
	'NElectrons':["number of electrons"],
	'NMuons':["number of muons"]
}

ColorDict = {"QCD":602,"TTJets":798,"WJets":801,"ZJets":881,"z20":rt.kBlue,"base":rt.kCyan + 2,"z40":rt.kMagenta}

for year in yearlist:
	if not os.path.exists(year):
		os.system("mkdir " + year)

	for var in varList.keys():
		print(var)

		for ibkg in range(len(sbL)):
			sb = sbL[ibkg]
			sbName = sb + year
			if sb == "z20" or sb == "base" or sb == "z40": 
				sbName = sb
			_file = rt.TFile.Open("../OutputRoot/20" + year + "/" + sbName+"/dataMC_comp.root","READ")
			print var+"_"+sbName
			_file.GetObject(var+"_"+sbName,tempHist[sb])
			tempHist[sb] = tempHist[sb].Clone(tempHist[sb].GetName()+"_")
			tempHist[sb].SetDirectory(0)
			tempHist[sb].SetLineColor(ColorDict[sb])
			tempHist[sb].SetLineStyle(1)
			if sb == "z20" or sb == "base" or sb == "z40": 
				tempHist[sb].SetLineStyle(7)
			norm(tempHist[sb])
			_file.Close()

		c = rt.TCanvas("c", "canvas", 800, 800) # we will use this for plotting		
	
		stack = rt.THStack()

		hList = [tempHist["QCD"],tempHist["TTJets"],tempHist["WJets"],tempHist["ZJets"],tempHist["z20"],tempHist["base"],tempHist["z40"]]
		for histo in hList:
			stack.Add(histo)
		stack.Draw("nostackHIST")
		ymax = stack.GetMaximum()	
		cutX = 0
		if var == 'metR':
			cutX = 0.15
		elif var == 'DeltaEta':
			cutX = 1.5
		elif var == 'MT_with_METMT_Cut' or var == 'MT_without_METMT_Cut':
			cutX = 1500	
		line = rt.TLine(cutX,0,cutX,ymax)
		line.SetLineColor(rt.kBlack)
		line.SetLineStyle(2)
		line.Draw("same")
		stack.GetXaxis().SetTitle(varList[var][0])
		stack.GetYaxis().SetTitle("Events (Normalized)")
		stack.GetXaxis().SetTitleOffset(1.2)
		stack.GetYaxis().SetTitleOffset(1.4) 
		stack.SetMaximum(ymax*10000) 

		rt.gPad.Update()
		rt.gPad.SetLogy(1)

		leg = rt.TLegend(0.12,0.69,0.75,0.89)
		leg.SetNColumns(2)
		leg.AddEntry(hList[0],'QCD', "l")
		leg.AddEntry(hList[4],'SVJ_2000_20_0.3_peak', "l")
		leg.AddEntry(hList[1],'TTJets', "l")
		leg.AddEntry(hList[5],'SVJ_3000_20_0.3_peak', "l")
		leg.AddEntry(hList[2],'WJets', "l")
		leg.AddEntry(hList[6],'SVJ_4000_20_0.3_peak', "l")
		leg.AddEntry(hList[3],'ZJets', "l")
		leg.SetTextSize(0.03)
		leg.SetBorderSize(0)
		leg.Draw('same')
		
		plotname= var+year+".pdf"
		c.SaveAs(year + "/" + plotname)
