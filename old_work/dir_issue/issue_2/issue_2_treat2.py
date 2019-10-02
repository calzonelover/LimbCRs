from ROOT import *
from array import *
from math import *
import numpy as np
import pyfits

import re # regular expression


#filename photon
filename = ['select_photon_w%d.fits'%(i+10) for i in range(390)] ##
#filename spacecraft
filenamesp = ['lat_spacecraft_weekly_w0%d_p202_v001.fits'%(i+10) for i in range(90)]
for i in range(300):
        filenamesp.append('lat_spacecraft_weekly_w%d_p202_v001.fits'%(i+100))

# our condition (Limb Peak at nadir 68.02)
Zmin = 110.0 # nadir 70.0
Zmax = 111.6 # nadir 68.4
Zbgmin = 0. # nadir 90 ## 80
Zbgmax = 106. # nadir 74 ## 72
cutted_rock_angle = 52.0
solidangle = (cos(Zmin*(pi/180.))-cos(Zmax*(pi/180.)))*(2.*pi)
solidanglebg = (cos(Zbgmin*(pi/180.))-cos(Zbgmax*(pi/180.)))*2.*pi

# Energy bin
oV = [(10**((float(i)/25)+1)) for i in range(51)]
V = array('d',oV)


# for map manipulation
cntmap = []
name_expmap = []
for i in range(50):
	namecntmap = 'cntmap%03d'%i
	cntmap.append(TH2F(namecntmap, namecntmap, 180,0.,360.,800,0.,80.))
	name_expmap.append('expmap%03d'%i)

list_week_frac_time_5per = []

def getWeekRegard(f_regard):
	week_sp_start = 10 # 010 is the starting week of our data
	week_consider = []
	for f in f_regard:
		week_consider.append(int(''.join(re.findall('[0-9]',f))) - week_sp_start)
	return week_consider




### Check week  ###
# if __name__ == "__main__":
# 	for processweek, f in enumerate(filename):
# 		print(f)
# 		sumlivetime_i = 0.
# 		sumlivetime_glimpse_i = 0. 
# 		fsp=pyfits.open(filenamesp[processweek])
# 		eventsp=fsp[1].data
# 		for i in range(len(eventsp)):
# 			sumlivetime_i+= eventsp[i]['LIVETIME']
# 			if abs(eventsp[i]['ROCK_ANGLE']) > 52.0:
# 				sumlivetime_glimpse_i+=eventsp[i]['ROCK_ANGLE']
# 		frac_time = sumlivetime_glimpse_i/sumlivetime_i
# 		if frac_time > 0.049 and frac_time < 0.051:
# 			list_week_frac_time_5per.append(f)
# 			print("found !")
# 	print("END PROGRAM")
# 	print("Found week that dart at limb 5 percent of livetime is :", list_week_frac_time_5per)

# # Rereult = ['select_photon_w54.fits', 'select_photon_w280.fits', 'select_photon_w362.fits']
# ### end check week ###


### Compute flux ###
# Choose week that LAT not looking at earth
f_regard = ['select_photon_w54.fits', 'select_photon_w280.fits', 'select_photon_w362.fits']

# Calculated week
regard_week = getWeekRegard(f_regard)

f_report = file('issue_2_treat2_alldat.olo','w')
### end config

Fexpmap = TFile('ExpMap_P8R2_ULTRACLEANVETO_V6_w010-w399_2.root')

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
    and event.THETA < 70. and array_n != -1 and (ev.PROCESSWEEK in regard_week):
		print "found photon pass !",ev.EVENTS, ev.PROCESSWEEK+10
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
# f_report = file('issue_2_treat1_alldat.olo','w')

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
	# Just condition for weak emission from bg
	try:
		EavgdN[i] = EavgdN[i]/dN[i]
	except ZeroDivisionError as e:
		EavgdN[i] = 0.
	try:
		EavgdNbg[i] = EavgdNbg[i]/dNbg[i]
	except ZeroDivisionError as e:
		EavgdNbg[i] = 0.
	f_report.write('%f %f %e %f %f %e \n'%(dNsb[i], EavgdN[i], flxvallimb[i], \
									 dNbg[i], EavgdNbg[i], flxvalbg[i]))
	print("Limb unsubtract bg at bin %d = %d"%(i,dN[i]))
	print(dN[i])
### end COmpute flux ###
























