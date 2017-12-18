import pyLikelihood
import pyIrfLoader
from ROOT import *
from math import *
from array import *
import numpy as np

# approximate value
### mode theta = 62.10
theta_fix = 62.10
livetime = 5294102.3631 # 70761348.6153
Zmin=110.0 # nadir 70.0
Zmax=111.6 # nadir 68.4
solidangle=(cos(Zmin*(pi/180.))-cos(Zmax*(pi/180.)))*(2.*pi)

# setting Aeff factory
pyIrfLoader.Loader_go()
myFactory = pyIrfLoader.IrfsFactory_instance()
irfs_f = myFactory.create("P8R2_ULTRACLEANVETO_V6::FRONT")
irfs_b = myFactory.create("P8R2_ULTRACLEANVETO_V6::BACK")
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
		if event.EVENTS % 10000 == 0: # this condition just print
			print(event.EVENTS, event.ENERGY)
		if event.ZENITH>Zmin and event.ZENITH<Zmax and event.THETA<70.: # select photon
			cntmap.Fill(event.ENERGY)
			dN[np.searchsorted(V,event.ENERGY)-1]+=1.
			EavgdN[np.searchsorted(V,event.ENERGY)-1]+=event.ENERGY
# check Aeff
for i in range(50):
	i = i+1 # start from 0 => 1
	cntbin_i = dN[i-1]
	Ebin_i = EavgdN[i-1]/cntbin_i # GeV
	Ebin_i_MeV = Ebin_i*1000. # GeV -> MeV
	Aeff_i = ((aeff_f.value(Ebin_i_MeV,theta_fix,0.)\
			  +aeff_b.value(Ebin_i_MeV,theta_fix,0.)))/10000. # cm^2 -> m^2
	Eff0.SetBinContent(i, Aeff_i)
	dE_bin_i = V[i]-V[i-1]
	print Ebin_i
	cntmap.SetBinContent(i, cntbin_i/dE_bin_i/Aeff_i/solidangle/livetime*(Ebin_i**2.75))
	cntmap.SetBinError(i, cntmap.GetBinContent(i)/sqrt(cntbin_i))

print V

C = TCanvas('C','C',800,600)
C.SetLogx()
C.SetLogy()
C.SetGrid()
cntmap.GetXaxis().SetTitle('E_{#gamma} (GeV)')
cntmap.GetYaxis().SetTitle('E^{2.75}Flux (GeV^{1.75}s^{-1}m^{-2}sr^{-1})')
cntmap.SetStats(0)
cntmap.SetTitle('#gamma-ray flux')
cntmap.Draw('E1')
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