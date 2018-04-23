from math import *
from ROOT import *
from array import *
import numpy as np
####################
# out condition ()
expmap_version = 2 # 1 = Old, 2 = Cutted limb
###############

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
if expmap_version == 1:
	Fexpmap = TFile('ExpMap_P8R2_ULTRACLEANVETO_V6_w010-w399.root')
	cutted_rock_angle = 0.
if expmap_version == 2:
	cutted_rock_angle = 52.
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
	array_n = np.searchsorted(V, energy) - 1 ### *** need to check for sure again
	if array_n < len(V)-1 and abs(event.ROCK) > cutted_rock_angle \
	   and event.THETA < 70. and array_n != -1:
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
strMap = TH2F('strMap','strMap', 180, 0., 360., 800, 0., 80.)
dphi=(360./strMap.GetNbinsX())*pi/180.
dtheta=(80./strMap.GetNbinsY())*pi/180.
for j in range(strMap.GetNbinsY()):
	strbin = dphi*dtheta*sin((j+0.5)*dtheta) # d(phi)d(theta)sin(theta)
	for i in range(strMap.GetNbinsX()):
		strMap.SetBinContent(i+1, j+1, strbin)

# define flxmap
flxmap = []
for i in range(50):
	flxmap.append(cntmap[i].Clone())
flxvallimb = []
flxvalbg = []
# write dNsb, EavgdN to file
f_report = file('alldat.olo','w')
for i in range(len(V)-1):
	# dE
	dE = V[i+1]-V[i]
	# Flxmap : flxmap = (cntmap/expmap)/dE/dOmage
	expmap = Fexpmap.Get(name_expmap[i])
	expmap.Scale(1./10000.) # cm^2 -> m^2
	#
	flxmap[i].Divide(expmap)
	# get flux value limb
	flxmap[i].GetXaxis().SetRangeUser(0., 360.)
	flxmap[i].GetYaxis().SetRangeUser(180. - Zmax, 180. - Zmin)
	flxvallimb.append(flxmap[i].Integral()/solidangle/dE)
	# get flux value bg
	flxmap[i].GetXaxis().SetRangeUser(0., 360.)
	flxmap[i].GetYaxis().SetRangeUser(180. - Zbgmax, 180. - Zbgmin)
	flxvalbg.append(flxmap[i].Integral()/solidanglebg/dE)
	#
	flxmap[i].Scale(1./dE)
	flxmap[i].Divide(strMap)
	# 
	dNsb[i] = dN[i] - dNbg[i]*((Zmin-Zmax)/(Zbgmin-Zbgmax))
	EavgdN[i] = EavgdN[i]/dN[i]
	# Just condition for weak emission from bg
	if dNbg[i] != 0:
		EavgdNbg[i] = EavgdNbg[i]/dNbg[i]
	else:
		EavgdNbg[i] = 0.
	f_report.write('%f %f %e %f %f %e \n'%(dNsb[i], EavgdN[i], flxvallimb[i], \
									 dNbg[i], EavgdNbg[i], flxvalbg[i]))
	print("Limb unsubtract bg at bin %d = %d"%(i,dN[i]))
	print(dN[i])













#####################
# Just Visualize map
######################

# visualize setting
name_plotmap = "Flxmap"
plotmap = flxmap
is_expmap = False
#####################
lbOS=-0.13 #Z-axis label offset
lbS=0.05   #Z-axis label size
ttOS=0.5   #Z-axis tltle offset
ttS=0.04   #Z-axis tltle size
C=TCanvas('C','C',800,600)
C.Divide(2,2)
C.cd(1)
C.cd(1).SetLogz()
# gStyle.SetPalette(kRainBow)
if is_expmap==True:
	expmap=Fexpmap.Get(name_expmap[0]) ###
else:
	expmap=plotmap[0]
expmap.SetStats(0)
gPad.SetTheta(-90)
gPad.SetPhi(-90)
expmap.Draw('SURF2POLZ')
expmap.GetXaxis().SetTitle('#phi (degree)')
expmap.GetYaxis().SetTitle('#theta_{nadir} (degree)')
expmap.GetYaxis().SetRangeUser(0.,80.)
expmap.GetZaxis().SetLabelOffset(lbOS)
expmap.GetZaxis().SetLabelSize(lbS)
expmap.GetZaxis().SetTitleOffset(ttOS)
expmap.GetZaxis().SetTitleSize(ttS)
# Name Z-axis
if name_plotmap == "Flxmap":
	expmap.GetZaxis().SetTitle('Flux (GeV^{-1}s^{-1}sr^{-1}m^{-2})') #
elif name_plotmap == "Expmap":
	expmap.GetZaxis().SetTitle('Exposure (m^{2}s)')
elif name_plotmap == "Cntmap":
	expmap.GetZaxis().SetTitle('Count')
# expmap.GetZaxis().SetTitle('Count')
expmap.SetTitle('%s 10.000-10.965 GeV'%name_plotmap)
#C.cd(1).SetLogz()
C.cd(2)
if is_expmap==True:
	expmap2=Fexpmap.Get(name_expmap[12]) ###
else:
	expmap2=plotmap[12]
expmap2.SetStats(0)
expmap2.Draw('SURF2POLZ')
gPad.SetTheta(-90)
gPad.SetPhi(-90)
expmap2.GetXaxis().SetTitle('#phi (degree)')
expmap2.GetYaxis().SetTitle('#theta_{nadir} (degree)')
expmap2.GetYaxis().SetRangeUser(0.,80.)
expmap2.GetZaxis().SetLabelOffset(lbOS)
expmap2.GetZaxis().SetLabelSize(lbS)
expmap2.GetZaxis().SetTitleOffset(ttOS)
expmap2.GetZaxis().SetTitleSize(ttS)
# Name Z-axis
if name_plotmap == "Flxmap":
	expmap2.GetZaxis().SetTitle('Flux (GeV^{-1}s^{-1}sr^{-1}m^{-2})') #
elif name_plotmap == "Expmap":
	expmap2.GetZaxis().SetTitle('Exposure (m^{2}s)')
elif name_plotmap == "Cntmap":
	expmap2.GetZaxis().SetTitle('Count')
# expmap2.GetZaxis().SetTitle('Count')
expmap2.SetTitle('%s 30.200-33.113 GeV'%name_plotmap)
C.cd(2).SetLogz()
C.cd(3)
if is_expmap==True:
	expmap3=Fexpmap.Get(name_expmap[24]) ###
else:
	expmap3=plotmap[24]
# expmap3=plotmap[24]
# expmap3=Fexpmap.Get(name_expmap[24]) ###
expmap3.SetStats(0)
expmap3.Draw('SURF2POLZ')
gPad.SetTheta(-90)
gPad.SetPhi(-90)
expmap3.GetXaxis().SetTitle('#phi (degree)')
expmap3.GetYaxis().SetTitle('#theta_{nadir} (degree)')
expmap3.GetYaxis().SetRangeUser(0.,80.)
expmap3.GetZaxis().SetLabelOffset(lbOS)
expmap3.GetZaxis().SetLabelSize(lbS)
expmap3.GetZaxis().SetTitleOffset(ttOS)
expmap3.GetZaxis().SetTitleSize(ttS)
# Name Z-axis
if name_plotmap == "Flxmap":
	expmap3.GetZaxis().SetTitle('Flux (GeV^{-1}s^{-1}sr^{-1}m^{-2})') #
elif name_plotmap == "Expmap":
	expmap3.GetZaxis().SetTitle('Exposure (m^{2}s)')
elif name_plotmap == "Cntmap":
	expmap3.GetZaxis().SetTitle('Count')
# expmap3.GetZaxis().SetTitle('Count')
expmap3.SetTitle('%s 91.201-100.000 GeV'%name_plotmap)
C.cd(3).SetLogz()
C.cd(4)
if is_expmap==True:
	expmap4=Fexpmap.Get(name_expmap[49]) ###
else:
	expmap4=plotmap[49]
# expmap4=plotmap[49]
# expmap4=Fexpmap.Get(name_expmap[49]) ###
expmap4.SetStats(0)
expmap4.Draw('SURF2POLZ')
gPad.SetTheta(-90)
gPad.SetPhi(-90)
expmap4.GetXaxis().SetTitle('#phi (degree)')
expmap4.GetYaxis().SetTitle('#theta_{nadir} (degree)')
expmap4.GetYaxis().SetRangeUser(0.,80.)
expmap4.GetZaxis().SetLabelOffset(lbOS)
expmap4.GetZaxis().SetLabelSize(lbS)
expmap4.GetZaxis().SetTitleOffset(ttOS)
expmap4.GetZaxis().SetTitleSize(ttS)
# Name Z-axis
if name_plotmap == "Flxmap":
	expmap4.GetZaxis().SetTitle('Flux (GeV^{-1}s^{-1}sr^{-1}m^{-2})') #
elif name_plotmap == "Expmap":
	expmap4.GetZaxis().SetTitle('Exposure (m^{2}s)')
elif name_plotmap == "Cntmap":
	expmap4.GetZaxis().SetTitle('Count')
# 
expmap4.SetTitle('%s 912.011-1000.000 GeV'%name_plotmap)
C.cd(4).SetLogz()
raw_input()
#####
# Close all file
Fexpmap.Close()
f_report.close()

raw_input()




