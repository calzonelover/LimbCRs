from math import *
from ROOT import *
from array import *
import numpy as np
# out condition ()
# our condition (Limb Peak at nadir 68.02)
Zmin=110.0 # nadir 70.0
Zmax=111.6 # nadir 68.4
Zbgmin=0. # nadir 90 ## 80
Zbgmax=106. # nadir 74 ## 72
solidangle=(cos(Zmin*(pi/180.))-cos(Zmax*(pi/180.)))*(2.*pi)
solidanglebg=(cos(Zbgmin*(pi/180.))-cos(Zbgmax*(pi/180.)))*2.*pi
# Energy bin
oV = [(10**((float(i)/25)+1)) for i in range(51)]
V = array('d',oV)
# Build count map
cntmap = []
# open expmap
Fexpmap = TFile('ExpMap_P8R2_ULTRACLEANVETO_V6_w010-w399_2.root')
name_expmap = []
for i in range(50):
	namecntmap = 'cntmap%03d'%i
	cntmap.append(TH2F(namecntmap, namecntmap, 180,0.,360.,800,0.,80.))
	name_expmap.append('expmap%03d'%i)

# Extract data from tree
ev = TChain('Data of photon and spacecraft')
ev.Add('limb_photon_data.root')

# Declare variable
dN = []
dNbg = []
EavgdN = []
EavgdNbg = []
dNsb = []
for i in range(50):
	dN.append(0)
	dNbg.append(0)
	EavgdN.append(0)
	EavgdNbg.append(0)
	dNsb.append(0)

# process data
### Uncorrected process
for event in ev:
	energy = event.ENERGY
	array_n = np.searchsorted(V, energy) - 1
	if array_n > 0 and array_n < 51 and abs(event.ROCK) > 52. \
	and event.THETA < 70.:
		cntmap[array_n].Fill(event.PHI_EARTH, 180.-event.ZENITH)
		# limb photon
		if event.ZENITH > Zmin and event.ZENITH < Zmax:
			dN[array_n]+=1.
			EavgdN[array_n]+=energy
		# bg photon
		if event.ZENITH > Zbgmin and event.ZENITH < Zbgmax:
			dNbg[array_n]+=1.
			EavgdNbg[array_n]+=energy
### Corrected process ????????????????? in SOON ?????????????????

# create strMap
strMap = TH2F('strmap','strmap', 180, 0., 360., 800, 0., 80.)
dphi=(360./strmap.GetNbinsX())*pi/180.
dtheta=(80./strmap.GetNbinsY())*pi/180.
for j in range(strmap.GetNbinsY()):
	strbin = dphi*dtheta*sin((j+0.5)*dtheta) # d(phi)d(theta)sin(theta)
	for i in range(strmap.GetNbinsX()):
		strmap.SetBinContent(i+1, j+1, strbin)

# define flxmap
flxmap = []
for i in range(50):
	flxmap.append(cntmap[i].Clone())
flxvallimb = []
flxvalbg = []
# write dNsb, EavgdN to file
f_report = file('allall.olo','w')
for i in range(len(V)-1):
	# dE
	dE = V[i+1]-V[i]
	# Flxmap : flxmap = (cntmap/expmap)/dE/dOmage
	expmap = Fexpmap.Get(name_expmap[i])
	expmap.Scale(1./10000.) # cm^2 -> m^2
	#
	flxmap[i].Divide(expmap)
	flxmap[i].Scale(1./dE)
	# get flux value limb
	flxmap[i].GetXaxis().SetRangeUser(0., 360.)
	flxmap[i].GetYaxis().SetRangeUser(180. - Zmax, 180. - Zmin)
	flxvallimb.append(flxmap[i].Integral()/solidangle)
	# get flux value bg
	flxmap[i].GetXaxis().SetRangeUser(0., 360.)
	flxmap[i].GetYaxis().SetRangeUser(180. - Zbgmax, 180. - Zbgmin)
	flxvalbg.append(flxmap[i].Integral()/solidanglebg)
	# 
	dNsb[i] = dN[i] - dNbg[i]*((Zmin-Zmax)/(Zbgmin-Zbgmax))
	EavgdN[i] = EavgdN[i]/dN[i]
	# Just condition for weak emission from bg
	if dNbg[i] != 0:
		EavgdNbg[i] = EavgdNbg[i]/dNbg[i]
	else:
		EavgdNbg[i] = 0.
	f1.write('%f %f %e %f %f %e \n'%(dNsb[i], EavgdN[i], flxvallimb[i], \
									 dNbg[i], EavgdNbg[i], flxvalbg[i]))
	print("Limb unsubtract bg at bin %d = %d"%(i,dN[i]))









