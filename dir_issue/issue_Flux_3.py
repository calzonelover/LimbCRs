import pyLikelihood
import pyIrfLoader
from ROOT import *
from math import *
from array import *
import numpy as np

# approximate value
### mode theta = 62.10
theta_fix = 62.10
livetime = 70761348.6153
Zmin=110.0 # nadir 70.0
Zmax=111.6 # nadir 68.4

# setting Aeff factory
pyIrfLoader.Loader_go()
myFactory = pyIrfLoader.IrfsFactory_instance()
irfs_f = myFactory.create("P8R2_SOURCE_V6::FRONT")
irfs_b = myFactory.create("P8R2_SOURCE_V6::BACK")
aeff_f = irfs_f.aeff()
aeff_b = irfs_b.aeff()

# import data from tree
ev=TChain('Data of photon and spacecraft')
ev.Add('finaltree.root')

# Define bin edge
oV=[(10**((float(i)/25)+1)) for i in range(51)]
V=array('d',oV)
# graph
cntmap = TH1F('cntmap', 'cntmap', len(V)-1, V)
Eff0 = TH1F('Eff0', '#phi = 0', len(V)-1, V) # phi 0
'''
Eff1 = TH1F('Eff1', '#phi = 45', len(V)-1, V) # phi 45
Eff2 = TH1F('Eff2', '#phi = 180', len(V)-1, V) # phi 180
Eff3 = TH1F('Eff3', '#phi = 275', len(V)-1, V) # phi 275
'''
# Declare variable
dN = []
EavgdN = []
for i in range(50):
	dN.append(0)
	EavgdN.append(0)
# for fill event
for event in ev:
	if np.searchsorted(V,event.ENERGY)>0 and np.searchsorted(V,event.ENERGY)<51: # select photon range (10,1000)
		if event.EVENTS % 10000 == 0:
			print(event.EVENTS, event.ENERGY)
		if event.ZENITH>Zmin and event.ZENITH<Zmax and event.THETA<70.:
			cntmap.Fill(event.ENERGY)
			dN[np.searchsorted(V,event.ENERGY)-1]+=1.
			EavgdN[np.searchsorted(V,event.ENERGY)-1]+=event.ENERGY
# check Aeff
for i in range(50):
	i = i+1 # start from 0 => 1
	cntbin_i = dN[i-1]
	Ebin_i = EavgdN[i-1]/cntbin_i
	Aeff_i = ((aeff_f.value(Ebin_i,theta_fix,0.)+aeff_b.value(Ebin_i,theta_fix,0.0)))/10000. # cm^2 -> m^2
	Eff0.SetBinContent(i, Aeff_i)
	print Ebin_i
	cntmap.SetBinContent(i, cntbin_i/Aeff_i/livetime*(Ebin_i**2.75))
print V
'''
	#### 
	Aeff_i1 = ((aeff_f.value(Ebin_i,theta_fix,45.)+aeff_b.value(Ebin_i,theta_fix,45.0)))/10000.
	Eff1.SetBinContent(i, Aeff_i1)
	Aeff_i2 = ((aeff_f.value(Ebin_i,theta_fix,180.)+aeff_b.value(Ebin_i,theta_fix,180.0)))/10000.
	Eff2.SetBinContent(i, Aeff_i2)
	Aeff_i3 = ((aeff_f.value(Ebin_i,theta_fix,275.)+aeff_b.value(Ebin_i,theta_fix,275.0)))/10000.
	Eff3.SetBinContent(i, Aeff_i3)
	####
'''

C = TCanvas('C','C',800,600)
C.SetLogx()
C.SetLogy()
C.SetGrid()
cntmap.GetXaxis().SetTitle('E_#gamma (GeV)')
cntmap.GetYaxis().SetTitle('E^{2.75}Flux (GeV^{1.75}s^{-1}m^{-2}sr^{-1})')
cntmap.Draw()
'''
#gPad.SetGrid()
Eff0.GetXaxis().SetTitle('E (GeV)')
Eff0.GetYaxis().SetTitle('Effective area (m^{2})')
Eff0.SetStats(0)
Eff0.Draw()
Eff1.SetLineColor(2)
Eff1.Draw('same')
Eff2.SetLineColor(3)
Eff2.Draw('same')
Eff3.SetLineColor(8)
Eff3.Draw('same')
C.BuildLegend()
Eff0.SetTitle('Effective area')
'''

raw_input()