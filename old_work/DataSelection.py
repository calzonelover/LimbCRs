from ROOT import *
from math import *
from array import *
import numpy as np
import pyfits

####### condition ########
typedat=21 # ultraclean_veto
#subfunction
class LookFT2:
	def __init__(self, events, eventsp, i, processweek, missiontime):
		# just declare variable
		self.Col_n = 0 # column in FT2 weekly file
		self.events = events
		self.eventsp = eventsp
		self.i = i
		self.processweek = processweek
		self.missiontime = missiontime
		self.array_n = self.OrderArray()
	def OrderArray(self): # Serves order of an array
		return np.searchsorted(self.eventsp[:,]['START'],self.missiontime) - 1
	def AltitudeSP(self): # For altitude SP
		return self.eventsp[self.array_n]['RAD_GEO']/1000. # m => km
	def ZenithShift(self):
		return self.events[self.i]['ZENITH_ANGLE']\
			   +(0.0211*(550.0-self.AltitudeSP()))
	def GetData(self):## will return ROCK_ANGLE, ALTITUDE_SP, ZENITH_SHIFT
		# check incorrect photon
		if self.missiontime <= self.eventsp[0]['START']: # Event before first
			return self.eventsp[self.i]['ROCK_ANGLE'], \
				   self.eventsp[self.i]['RAD_GEO']/1000., self.ZenithShift()
		if self.missiontime >= self.eventsp[len(self.eventsp)-1]['STOP']: # event after first
			print('!!!! More than end !!!!')
			return self.eventsp[self.i]['ROCK_ANGLE'], \
				   self.eventsp[self.i]['RAD_GEO']/1000., self.ZenithShift()
		# Collect proper photon
		return self.eventsp[self.array_n]['ROCK_ANGLE'], self.eventsp[self.array_n]['RAD_GEO']/1000., \
			   self.ZenithShift()



#filename photon
filename = ['select_photon_w%d.fits'%(i+10) for i in range(390)] ##
#filename spacecraft
filenamesp= ['lat_spacecraft_weekly_w0%d_p202_v001.fits'%(i+10) for i in range(90)]
for i in range(300):
        filenamesp.append('lat_spacecraft_weekly_w%d_p202_v001.fits'%(i+100))
#file to write
f1=TFile('limb_photon_data.root','RECREATE')
t1=TTree('Data of photon and spacecraft','Data events')
#array that we want
EVENTS = np.zeros(1, dtype=int)
TIME=np.zeros(1,dtype=float)
PROCESSWEEK=np.zeros(1,dtype=float)
ENERGY = np.zeros(1, dtype=float)
ZENITH = np.zeros(1, dtype=float)
ZENITHSHIFT = np.zeros(1, dtype=float)
THETA = np.zeros(1, dtype=float)
PHI = np.zeros(1, dtype=float)
ALTITUDE = np.zeros(1,dtype=float)
PHI_EARTH = np.zeros(1,dtype=float)
ROCK = np.zeros(1,dtype=float)


# create the branch of our tre
t1.Branch('EVENTS',EVENTS,'EVENTS/I')
t1.Branch('TIME',TIME,'TIME/D')
t1.Branch('PROCESSWEEK',PROCESSWEEK,'PROCESSWEEK/D')
t1.Branch('ENERGY',ENERGY,'ENERGY/D')
t1.Branch('ZENITH',ZENITH,'ZENITH/D')
t1.Branch('ZENITHSHIFT',ZENITHSHIFT,'ZENITHSHIFT/D')
t1.Branch('THETA',THETA,'THETA/D')
t1.Branch('PHI',PHI,'PHI/D')
t1.Branch('ALTITUDE',ALTITUDE,'ALTITUDE/D')
t1.Branch('PHI_EARTH',PHI_EARTH,'PHI_EARTH/D')
t1.Branch('ROCK',ROCK,'ROCK/D')




numberevent = 0
for processweek, f in enumerate(filename):
	file=pyfits.open(f)
	events=file[1].data
	fsp=pyfits.open(filenamesp[processweek])
	eventsp=fsp[1].data
	print(f," Done !")
	for i in range(len(events)): # i is an array number in file photon
		if events[i]['EVENT_CLASS'][typedat]==True:
			# Let looker seek SP data at that time
			looker = LookFT2(events, eventsp, i, processweek, events[i]['TIME'])
			# print(f,i,numberevent, looker.array_n, len(looker.eventsp))
			RockAngle, AltitudeSP, ZenithShift = looker.GetData()
			# just count
			numberevent+=1
			# Fill in th tree
			EVENTS[0]=numberevent
			TIME[0]=events[i]['TIME']
			PROCESSWEEK[0]=processweek
			ENERGY[0]=events[i]['ENERGY']/1000. # MeV -> Gev
			ZENITH[0]=events[i]['ZENITH_ANGLE']
			ZENITHSHIFT[0]= ZenithShift # zenithshift(events[i]['ZENITH_ANGLE'],processweek,events[i]['TIME'])
			THETA[0]=events[i]['THETA']
			PHI[0]=events[i]['PHI']
			ALTITUDE[0]= AltitudeSP # altitudesp(processweek,events[i]['TIME'])
			PHI_EARTH[0]=events[i]['EARTH_AZIMUTH_ANGLE']
			ROCK[0]= RockAngle # rockang(processweek,events[i]['TIME'])
			t1.Fill()
			#if numberevent%1 == 0:
			#	print(f,i,numberevent, looker.array_n, len(looker.eventsp))


# finish tree branch
f1.Write()
f1.Close()
