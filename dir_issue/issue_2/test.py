import numpy as np
import re

f_regard = ['select_photon_w54.fits', 'select_photon_w280.fits', 'select_photon_w362.fits']

def weekRegard(f_regard):
	week_sp_start = 10 # 010 is the starting week of our data
	week_consider = []
	for f in f_regard:
		week_consider.append(int(''.join(re.findall('[0-9]',f))) - 10)
	return week_consider

if __name__ == "__main__":
	print(weekRegard(f_regard))