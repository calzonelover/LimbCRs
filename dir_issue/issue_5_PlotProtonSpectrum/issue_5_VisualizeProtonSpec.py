# -*- coding: utf-8 -*-
from ROOT import *
from math import *
from array import *
import numpy as np

import abc # abstract base class

### Setting
title = ''#'Proton spectrum in rigidity'
N_bin_SPL = 66
N_bin_BPL = 66 # bin of histogram AMS-02 for normalize model
Plot_Range = [8, 40000]
# AMS
AMS_MarkerColor = 8
AMS_MarkerStyle = 20
# PAMELA
PAMELA_MarkerColor = 38
PAMELA_MarkerStyle = 22
# model
Model_LineColor = 2
Model_LineStyle = 1
Model_LineWidth = 3

ModelMinMax_LineStyle = 7
ModelMinMax_LineWidth = 2


### method for get E^{2.75}Flux
def getHistE275Flux(binEdgeAMS, binFluxAMS, binStatErrorAMS\
				, binEdgePAMELA, binFluxPAMELA, binStatErrorPAMELA):
	# declare histogram
	HistE275FluxAMS = TH1F("AMS-02 (2015)", "AMS-02 (2015)", len(binEdgeAMS)-1, binEdgeAMS)
	HistE275FluxPAMELA = TH1F("PAMELA", "PAMELA (2011)", len(binEdgePAMELA)-1, binEdgePAMELA)
	# declare histogram error band
	for i in range(len(binEdgeAMS)-1):
		E275_AMS_i = ((binEdgeAMS[i]+binEdgeAMS[i+1])/2.0)**2.75
		HistE275FluxAMS.SetBinContent(i+1, binFluxAMS[i]*E275_AMS_i)
		# set bin error
		HistE275FluxAMS.SetBinError(i+1, binStatErrorAMS[i]*E275_AMS_i)
	for i in range(len(binEdgePAMELA)-1):
		E275_PAMELA_i = ((binEdgePAMELA[i]+binEdgePAMELA[i+1])/2.0)**2.75
		HistE275FluxPAMELA.SetBinContent(i+1, binFluxPAMELA[i]*E275_PAMELA_i)
		# set error
		HistE275FluxPAMELA.SetBinError(i+1, binStatErrorPAMELA[i]*E275_PAMELA_i)
	# use definition to get average Ebin from power law rules
	return HistE275FluxAMS, HistE275FluxPAMELA

### get our model result
class Model:
	@abc.abstractmethod
	def getY(self, input_x):
		return
	@abc.abstractmethod
	def getNormFactor(model_y, exp_y):
		pass

class SPL(Model):
	def __init__(self, gamma):
		self.norm = None
		self.gamma = gamma
	def getY(self, input_x):
		return self.norm*input_x**(-1.0*self.gamma)
	def getNormFactor(self, exp_x, exp_y):
		self.norm = exp_y*exp_x**self.gamma

class BPL(Model):
	def __init__(self, gamma1, gamma2, Rbreak):
		self.norm1 = None
		self.gamma1 = gamma1
		self.norm2 = None
		self.gamma2 = gamma2
		self.Rbreak = Rbreak
	def getY(self, input_x):
		if input_x <= self.Rbreak:
			return self.norm1*input_x**(-1.0*self.gamma1)
		else:
			return self.norm2*input_x**(-1.0*self.gamma2)
	def getNormFactor(self, exp_x, exp_y):
		if exp_x <= self.Rbreak:
			self.norm1 = exp_y*exp_x**self.gamma1
			self.norm2 = self.norm1*self.Rbreak**(self.gamma2-self.gamma1)
		else:
			self.norm2 = exp_y*exp_x**self.gamma2
			self.norm1 = self.norm2*self.Rbreak**(self.gamma1-self.gamma2)


def getModelResults(modelType):
	binEdgeModel = [(10**((float(i)/25)+1)) for i in range(60)]
	binFluxModel = [ modelType.getY((binEdgeModel[i]+binEdgeModel[i+1])/2.0)\
	 				for i in range(len(binEdgeModel)-1) ]
	binFlux275Model = [ modelType.getY((binEdgeModel[i]+binEdgeModel[i+1])/2.0)\
						*((binEdgeModel[i]+binEdgeModel[i+1])/2.0)**2.75 \
						for i in range(len(binEdgeModel)-1) ]
	binModel = [ (binEdgeModel[i]+binEdgeModel[i+1])/2.0 \
				 for i in range(len(binEdgeModel)-1)]
	return binModel, binFluxModel, binFlux275Model

### Plot

if __name__ == "__main__":
	########################################
	### Get data from other experiment  ####
	########################################
	f_AMS = np.genfromtxt('AMS_data.dat')
	f_PAMELA = np.genfromtxt('PAMELA_data.dat')
	binEdgeAMS, binFluxAMS, binStatErrorAMS, binSysErrorAMS = f_AMS[:,0].tolist()\
				, f_AMS[:,1][0:-1].tolist(), f_AMS[:,2][0:-1].tolist(), f_AMS[:,3][0:-1].tolist()
	binEdgePAMELA, binFluxPAMELA, binStatErrorPAMELA, binSysErrorPAMELA = \
		f_PAMELA[:,0].tolist(), f_PAMELA[:,1][0:-1].tolist()\
		, f_PAMELA[:,2][0:-1].tolist(), f_PAMELA[:,3][0:-1].tolist()
	binEdgeAMS, binEdgePAMELA = array('d', binEdgeAMS), array('d', binEdgePAMELA)
	### get Flux275
	HistE275FluxAMS, HistE275FluxPAMELA = getHistE275Flux(binEdgeAMS, binFluxAMS, binStatErrorAMS\
						, binEdgePAMELA, binFluxPAMELA, binStatErrorPAMELA)
	######################
	### Model stuff  #####
	######################
	## init model
	# SPL
	modelSPL = SPL(2.68)
	modelSPLmin = SPL(2.65)
	modelSPLmax = SPL(2.71)
	# BPL
	modelBPL = BPL(2.84, 2.64, 328)
	modelBPLmin = BPL(2.90, 2.81, 177)
	modelBPLmax = BPL(2.78, 2.47, 479)
	## get normalize factor
	# SPL
	modelSPL.getNormFactor((binEdgeAMS[N_bin_SPL]+binEdgeAMS[N_bin_SPL+1])/2.0
						 , binFluxAMS[N_bin_SPL])
	modelSPLmin.getNormFactor((binEdgeAMS[N_bin_SPL]+binEdgeAMS[N_bin_SPL+1])/2.0
						 , binFluxAMS[N_bin_SPL])
	modelSPLmax.getNormFactor((binEdgeAMS[N_bin_SPL]+binEdgeAMS[N_bin_SPL+1])/2.0
						 , binFluxAMS[N_bin_SPL])
	# BPL
	modelBPL.getNormFactor((binEdgeAMS[N_bin_BPL]+binEdgeAMS[N_bin_BPL+1])/2.0
						 , binFluxAMS[N_bin_BPL])
	modelBPLmin.getNormFactor((binEdgeAMS[N_bin_BPL]+binEdgeAMS[N_bin_BPL+1])/2.0
						 , binFluxAMS[N_bin_BPL])
	modelBPLmax.getNormFactor((binEdgeAMS[N_bin_BPL]+binEdgeAMS[N_bin_BPL+1])/2.0
						 , binFluxAMS[N_bin_BPL])
	## get data from model to take as TGraph
	# SPL
	binModelSPL, binFluxModelSPL, binFlux275ModelSPL = getModelResults(modelSPL)
	binModelSPLmin, binFluxModelSPLmin, binFlux275ModelSPLmin = getModelResults(modelSPLmin)
	binModelSPLmax, binFluxModelSPLmax, binFlux275ModelSPLmax = getModelResults(modelSPLmax)
	# BPL
	binModelBPL, binFluxModelBPL, binFlux275ModelBPL = getModelResults(modelBPL)
	binModelBPLmin, binFluxModelBPLmin, binFlux275ModelBPLmin = getModelResults(modelBPLmin)
	binModelBPLmax, binFluxModelBPLmax, binFlux275ModelBPLmax = getModelResults(modelBPLmax)
	#$$ make TGraph
	# SPL
	gSPL = TGraph(len(binModelSPL), array('d', binModelSPL), array('d', binFlux275ModelSPL))
	gSPLmin = TGraph(len(binModelSPLmin), array('d', binModelSPLmin), array('d', binFlux275ModelSPLmin))
	gSPLmax = TGraph(len(binModelSPLmax), array('d', binModelSPLmax), array('d', binFlux275ModelSPLmax))
	# BPL
	gBPL = TGraph(len(binModelBPL), array('d', binModelBPL), array('d', binFlux275ModelBPL))
	gBPLmin = TGraph(len(binModelBPLmin), array('d', binModelBPLmin), array('d', binFlux275ModelBPLmin))
	gBPLmax = TGraph(len(binModelBPLmax), array('d', binModelBPLmax), array('d', binFlux275ModelBPLmax))
	######################
	###    Plot      #####
	######################
	C = TCanvas('C','C',800,700)
	C.Divide(1,2,0,0)
	C.GetPad(1).SetRightMargin(.01)
	#############
	###   1   ###
	#############
	C.cd(1)
	C.cd(1).SetLogx()
	C.cd(1).SetLogy()
	HistE275FluxAMS.SetStats(0)
	HistE275FluxAMS.Draw('E1')
	HistE275FluxPAMELA.Draw('E1same')
	# AMS Setting
	HistE275FluxAMS.SetLineColor(AMS_MarkerColor)
	HistE275FluxAMS.SetMarkerStyle(AMS_MarkerStyle)
	HistE275FluxAMS.SetMarkerColor(AMS_MarkerColor)
	# PAMELA setting
	HistE275FluxPAMELA.SetLineColor(PAMELA_MarkerColor)
	HistE275FluxPAMELA.SetMarkerStyle(PAMELA_MarkerStyle)
	HistE275FluxPAMELA.SetMarkerColor(PAMELA_MarkerColor)
	# Model SPL
	gSPL.Draw('same')
	gSPLmin.Draw('same')
	gSPLmax.Draw('same')
	## setting style
	gSPL.SetLineColor(Model_LineColor)
	gSPL.SetLineStyle(Model_LineStyle)
	gSPL.SetLineWidth(Model_LineWidth)
	gSPLmin.SetLineColor(Model_LineColor)
	gSPLmin.SetLineStyle(ModelMinMax_LineStyle)
	gSPLmin.SetLineWidth(ModelMinMax_LineWidth)
	gSPLmax.SetLineColor(Model_LineColor)
	gSPLmax.SetLineStyle(ModelMinMax_LineStyle)
	gSPLmax.SetLineWidth(ModelMinMax_LineWidth)
	# Set title after legend
	HistE275FluxAMS.SetTitle(title)
	HistE275FluxAMS.GetYaxis().SetTitle('Proton E^{2.75}#times Flux (GV^{1.75}m^{-2}s^{-1}sr^{-1})')
	HistE275FluxAMS.GetXaxis().SetTitle('Rigidity (GV)')
	HistE275FluxAMS.GetXaxis().SetRangeUser(Plot_Range[0], Plot_Range[1])
	############
	###   2  ###
	############
	C.cd(2)
	C.GetPad(2).SetRightMargin(.01)
	C.cd(2).SetLogx()
	C.cd(2).SetLogy()
	## AMS
	HistE275FluxAMS.Draw('E1')
	## PAMELA
	HistE275FluxPAMELA.Draw('E1same')
	## Model BPL
	gBPL.Draw('same')
	gBPL.SetTitle('This work')
	# set style
	gBPL.SetFillColor(0)
	gBPL.SetLineColor(Model_LineColor)
	gBPL.SetLineStyle(Model_LineStyle)
	gBPL.SetLineWidth(Model_LineWidth)
	C.cd(2).BuildLegend()
	# min max case
	gBPLmin.Draw('same')
	gBPLmax.Draw('same')
	gBPLmin.SetLineColor(Model_LineColor)
	gBPLmin.SetLineStyle(ModelMinMax_LineStyle)
	gBPLmin.SetLineWidth(ModelMinMax_LineWidth)
	gBPLmax.SetLineColor(Model_LineColor)
	gBPLmax.SetLineStyle(ModelMinMax_LineStyle)
	gBPLmax.SetLineWidth(ModelMinMax_LineWidth)
	###############################
	#  Setting global Label Axis  #
	###############################
	# C.cd()
	# XLabel = TText(.05, 0.8, "Rigidity")
	# XLabel.SetTextSize(0.1)
	# XLabel.Draw()
	raw_input()
	C.SaveAs('ProtonSpectrumModelMeasurement.pdf')
	print("done")
