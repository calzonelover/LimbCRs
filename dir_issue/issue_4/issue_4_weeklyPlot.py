from ROOT import *
from array import *
from math import *
import numpy as np
import pyfits

# our condition (Limb Peak at nadir 68.02)
nadirCutMin = 68.4
nadirCutMax = 70.0
rockCut = 52.0 
thetaCut = 70.0

# event photon file
ev = TChain('Data of photon and spacecraft')
ev.Add('limb_photon_data.root')

# read data from count and time fraction file
f_time = np.genfromtxt('issue_3_time.olo')
f_count = np.genfromtxt('issue_3_count.olo')

def getFraction(f_time, f_count):
	# get data
	dat_time = np.genfromtxt(f_time)
	dat_count = np.genfromtxt(f_count)
	try:
		fracC, fracT = np.divide(dat_count[:, 2], dat_count[:, 1])\
					  ,np.divide(dat_time[:, 2], dat_time[:, 1])
	except ZeroDivisionError:
		print('Found zero divider !!')
		exit()
	return fracC, fracT


# Declare TH1F of distribution
DistTH1FArray = []


# compute for Fill function
def weeklyFill(DistTH1FArray, arbitaryFrac):
	for i in range(len(arbitaryFrac)):
		DistTH1FArray.append(TH1F("week %i"%(i+10),"week %i"%(i+10),100,20,90))

def LabelHist(DistTH1FArray, fracT, fracC):
	# for Fill label of fraction (count & time)
	for event in ev:
		eventNadia = 180.0 - event.ZENITH
		DistTH1FArray[event.PROCESSWEEK].Fill(eventNadia)
	## find some fn that setting 
	for i in range(len(DistTH1FArray)):
		 #DistTH1FArray[i].setSomeLabel( "Time fraction" fracT[i] 
		#								 "Count fraction" fracC[i])


if __name__ == "__main__":
	## get data each week
	fracT, fracC = getFraction(f_time, f_count)
	## Compute to Fill ( loop over week )
	weeklyFill(DistTH1FArray, fracT)
	## Label each TH1F with fraction and change title
	LabelHist(DistTH1FArray, fracT, fracC)







