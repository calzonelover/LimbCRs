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
nadirCutMin = 68.4
nadirCutMax = 70.0
rockCut = 52.0 
thetaCut = 70.0

# Declare variable
NCutNadir = 0.
NUsual = 0.

# report file
f_report = file('issue_3_count.olo','w')

# event photon file
ev = TChain('Data of photon and spacecraft')
ev.Add('limb_photon_data.root')

# count 
currentweek = None

for event in ev:
	eventNadir = 180.0 - event.ZENITH
	if event.THETA < thetaCut \
	and eventNadir < nadirCutMax and eventNadir > nadirCutMin:
		NUsual += 1.
		if abs(event.ROCK) > rockCut:
			NCutNadir +=1.
	# for reset count and report each week 
	if currentweek != event.PROCESSWEEK:
		f_report.write('%f %f %f \n'%(event.PROCESSWEEK, NUsual, NCutNadir))
		NCutNadir = 0.
		NUsual = 0.		
	currentweek = event.PROCESSWEEK

