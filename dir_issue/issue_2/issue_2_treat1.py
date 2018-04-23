from ROOT import *
from array import *
from math import *
import numpy as np
import pyfits

import re # regular expression


#filename photon
filename = ['select_photon_w%d.fits'%(i+10) for i in range(390)] ##
#filename spacecraft
filenamesp= ['lat_spacecraft_weekly_w0%d_p202_v001.fits'%(i+10) for i in range(90)]
for i in range(300):
        filenamesp.append('lat_spacecraft_weekly_w%d_p202_v001.fits'%(i+100))

# our condition (Limb Peak at nadir 68.02)
Zmin=110.0 # nadir 70.0
Zmax=111.6 # nadir 68.4
Zbgmin=0. # nadir 90 ## 80
Zbgmax=106. # nadir 74 ## 72
cutted_rock_angle = 52.0
solidangle=(cos(Zmin*(pi/180.))-cos(Zmax*(pi/180.)))*(2.*pi)
solidanglebg=(cos(Zbgmin*(pi/180.))-cos(Zbgmax*(pi/180.)))*2.*pi

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
		week_consider.append(int(''.join(re.findall('[0-9]',f))) - 10)
	return week_consider




# if __name__ == "__main__":
# 	### Check week ###
# 	for processweek, f in enumerate(filename):
# 		print(f)
# 		sumlivetime = 0
# 		fsp=pyfits.open(filenamesp[processweek])
# 		eventsp=fsp[1].data
# 		for i in range(len(eventsp)):
# 			if abs(eventsp[i]['ROCK_ANGLE'])>52.0:
# 				break
# 		else:
# 			list_week_not_look.append(f)
# 			print("Found !")
# 	print("End program")
# 	print("Found that week which not looking for |phi_rock|<52 is"\
# 		,list_week_not_look)
# # Result = ['select_photon_w10.fits', 'select_photon_w11.fits', 'select_photon_w13.fits', 'select_photon_w14.fits', 'select_photon_w15.fits', 'select_photon_w16.fits', 'select_photon_w18.fits', 'select_photon_w19.fits', 'select_photon_w21.fits', 'select_photon_w22.fits', 'select_photon_w23.fits', 'select_photon_w24.fits', 'select_photon_w26.fits', 'select_photon_w28.fits', 'select_photon_w31.fits', 'select_photon_w32.fits', 'select_photon_w36.fits', 'select_photon_w37.fits', 'select_photon_w38.fits', 'select_photon_w40.fits', 'select_photon_w41.fits', 'select_photon_w45.fits', 'select_photon_w46.fits', 'select_photon_w47.fits', 'select_photon_w48.fits', 'select_photon_w51.fits', 'select_photon_w53.fits', 'select_photon_w55.fits', 'select_photon_w56.fits', 'select_photon_w57.fits', 'select_photon_w60.fits', 'select_photon_w61.fits', 'select_photon_w62.fits', 'select_photon_w67.fits', 'select_photon_w93.fits', 'select_photon_w95.fits', 'select_photon_w100.fits', 'select_photon_w102.fits', 'select_photon_w107.fits', 'select_photon_w109.fits', 'select_photon_w114.fits', 'select_photon_w116.fits', 'select_photon_w123.fits', 'select_photon_w128.fits', 'select_photon_w133.fits', 'select_photon_w139.fits', 'select_photon_w140.fits', 'select_photon_w142.fits', 'select_photon_w154.fits', 'select_photon_w175.fits', 'select_photon_w178.fits', 'select_photon_w188.fits', 'select_photon_w200.fits', 'select_photon_w205.fits', 'select_photon_w278.fits', 'select_photon_w308.fits', 'select_photon_w318.fits', 'select_photon_w341.fits', 'select_photon_w345.fits', 'select_photon_w353.fits', 'select_photon_w361.fits', 'select_photon_w366.fits', 'select_photon_w374.fits', 'select_photon_w385.fits', 'select_photon_w391.fits']
# 	### end Check week ###





### Compute flux ###
# Choose week that LAT not looking at earth
f_regard = ['select_photon_w10.fits', 'select_photon_w11.fits', 'select_photon_w13.fits', 'select_photon_w14.fits', 'select_photon_w15.fits', 'select_photon_w16.fits', 'select_photon_w18.fits', 'select_photon_w19.fits', 'select_photon_w21.fits', 'select_photon_w22.fits', 'select_photon_w23.fits', 'select_photon_w24.fits', 'select_photon_w26.fits', 'select_photon_w28.fits', 'select_photon_w31.fits', 'select_photon_w32.fits', 'select_photon_w36.fits', 'select_photon_w37.fits', 'select_photon_w38.fits', 'select_photon_w40.fits', 'select_photon_w41.fits', 'select_photon_w45.fits', 'select_photon_w46.fits', 'select_photon_w47.fits', 'select_photon_w48.fits', 'select_photon_w51.fits', 'select_photon_w53.fits', 'select_photon_w55.fits', 'select_photon_w56.fits', 'select_photon_w57.fits', 'select_photon_w60.fits', 'select_photon_w61.fits', 'select_photon_w62.fits', 'select_photon_w67.fits', 'select_photon_w93.fits', 'select_photon_w95.fits', 'select_photon_w100.fits', 'select_photon_w102.fits', 'select_photon_w107.fits', 'select_photon_w109.fits', 'select_photon_w114.fits', 'select_photon_w116.fits', 'select_photon_w123.fits', 'select_photon_w128.fits', 'select_photon_w133.fits', 'select_photon_w139.fits', 'select_photon_w140.fits', 'select_photon_w142.fits', 'select_photon_w154.fits', 'select_photon_w175.fits', 'select_photon_w178.fits', 'select_photon_w188.fits', 'select_photon_w200.fits', 'select_photon_w205.fits', 'select_photon_w278.fits', 'select_photon_w308.fits', 'select_photon_w318.fits', 'select_photon_w341.fits', 'select_photon_w345.fits', 'select_photon_w353.fits', 'select_photon_w361.fits', 'select_photon_w366.fits', 'select_photon_w374.fits', 'select_photon_w385.fits', 'select_photon_w391.fits']

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
		print "found photon pass !",ev.EVENTS, ev.PROCESSWEEK
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








