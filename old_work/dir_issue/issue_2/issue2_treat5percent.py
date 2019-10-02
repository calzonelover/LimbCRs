from ROOT import *
from array import *
from math import *
import numpy as np
import pyfits

import re # regular expression

#filename photon
filename = ['select_photon_w%d.fits'%(i+10) for i in range(390)] ##
#filename time 5% of space craft spacecraft
fsp_regard =  ['select_photon_w54.fits'] ## try just one week and second layer
#fsp_regard =  ['select_photon_w54.fits', 'select_photon_w280.fits', 'select_photon_w362.fits']


# our condition (Limb Peak at nadir 68.02)
Zmin = 110.0 # nadir 70.0
Zmax = 114 # nadir 66
cutted_rock_angle = 52.0

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

f_report = file('issue_2_treat25percent_alldat.olo','w')

Fexpmap = TFile('ExpMap_P8R2_ULTRACLEANVETO_V6_w010-w399_2.root')

# event photon file
ev = TChain('Data of photon and spacecraft')
ev.Add('limb_photon_data.root')

# Declare variables
dN_limb = 0
dN_week = 0

def getWeekRegard(f_regard):
	week_sp_start = 10 # 010 is the starting week of our data
	week_consider = []
	for f in f_regard:
		week_consider.append(int(''.join(re.findall('[0-9]',f))) - week_sp_start)
	return week_consider

### Compute flux ###
regard_week = getWeekRegard(fsp_regard)

# process data 
for event in ev:
	energy = event.ENERGY
	array_n = np.searchsorted(V, energy) - 1 
	if array_n < len(V) - 1 and (ev.PROCESSWEEK in regard_week) \
	and event.THETA < 70.0 and array_n != -1:
		# for ordinary photon
		dN_week += 1.
		# for limb's photon
		if abs(event.ROCK) > cutted_rock_angle and event.ZENITH > Zmin and event.ZENITH < Zmax:
			dN_limb += 1.
			print('hi limb!!')

## save data to text
f_report.write('Report ordinary photon %f \n Got limb photon %f \n'%(dN_week, dN_limb))

















