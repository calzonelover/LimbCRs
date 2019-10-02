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
f_time = 'issue_3_time.olo'
f_count = 'issue_3_count.olo'

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
def weeklyFill(arbitaryFrac):
	out_array = []
	for i in range(len(arbitaryFrac)):
		out_array.append(TH1F("week %i"%(i+10),"week %i"%(i+10),4000,20,90))
	return out_array
def LabelHist(DistTH1FArray, fracT, fracC):
	# for Fill label of fraction (count & time)
	for event in ev:
		eventNadia = 180.0 - event.ZENITH
		DistTH1FArray[int(event.PROCESSWEEK)].Fill(eventNadia)
	# Draw and save
	F_ROOT = TFile("WeeklySummary.root", 'RECREATE')
	## find some fn that setting
	for i in range(len(DistTH1FArray)):
		# set axis
		DistTH1FArray[i].GetXaxis().SetTitle("#theta_{Nadir}")
		DistTH1FArray[i].GetYaxis().SetTitle("Count")
		# set title
		DistTH1FArray[i].SetTitle("Week %d | fracT : %f , fracC : %f"\
								%(i+10,fracT[i],fracC[i]))
		DistTH1FArray[i].Write()
	# Close root file
	F_ROOT.Close()
if __name__ == "__main__":
	print("!! being process !!")
	## get data each week
	fracT, fracC = getFraction(f_time, f_count)
	## Compute to Fill ( loop over week )
	DistTH1FArray = weeklyFill(fracT)
	## Label each TH1F with fraction and change title
	LabelHist(DistTH1FArray, fracT, fracC)
	# done
	print("!! Done issue_4 process !!")
