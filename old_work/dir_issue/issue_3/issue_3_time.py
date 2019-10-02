from ROOT import *
from array import *
from math import *
import numpy as np
import pyfits

#filename spacecraft
filenamesp= ['lat_spacecraft_weekly_w0%d_p202_v001.fits'%(i+10) for i in range(90)]
for i in range(300):
        filenamesp.append('lat_spacecraft_weekly_w%d_p202_v001.fits'%(i+100))

# Declare variable
t_52 = 0.
t_42 = 0.

# report file
f_report = file('issue_3_time.olo','w')

# process for count time 
for f in filenamesp:
	file = pyfits.open(f)
	eventsp = file[1].data
	for i in range(len(eventsp)):
		# for | theta_ROCK | > 42
		if abs(eventsp[i]['ROCK_ANGLE']) > 42.:
			t_42 += eventsp[i]['LIVETIME']
			# for | theta_ROCK | > 52.
			if abs(eventsp[i]['ROCK_ANGLE']) > 52.:
				t_52 += eventsp[i]['LIVETIME']
	f_report.write('%s %f %f \n'%(f, t_42, t_52))