from ROOT import *
from math import *
from array import *
import numpy as np
import pyfits
####### condition ########
typedat=21 #ultraclean_veto
#subfunction
#def rockang(processweek,missiontime):
#	fsp=pyfits.open(filenamesp[processweek])
#	eventsp=fsp[1].data
#	if missiontime<=eventsp[0]['START']:
#		return eventsp[i]['ROCK_ANGLE']
#	if missiontime>=eventsp[len(eventsp)-2]['START']:
#		return eventsp[i]['ROCK_ANGLE']
#	return (eventsp[np.searchsorted(eventsp[:,]['START'],missiontime)]['ROCK_ANGLE']+eventsp[np.searchsorted(eventsp[:,]['START'],missiontime)+1]['ROCK_ANGLE'])/2.
def altitudesp(processweek,missiontime):
        fsp=pyfits.open(filenamesp[processweek])
        eventsp=fsp[1].data
	if missiontime<=eventsp[0]['START']:
		return eventsp[i]['ROCK_ANGLE']
	if missiontime>=eventsp[len(eventsp)-2]['START']:
		return eventsp[i]['RAD_GEO']/1000.
	return (eventsp[np.searchsorted(eventsp[:,]['START'],missiontime)]['RAD_GEO']+eventsp[np.searchsorted(eventsp[:,]['START'],missiontime)+1]['RAD_GEO'])/2000.
def zenithshift(zenithang,processweek,missiontime):
        return zenithang+(0.0211*(550.0-altitudesp(processweek,missiontime)))
#filename photon
filename = ['select_photon_w%d.fits'%(i+10) for i in range(390)] ##
#filename spacecraft
filenamesp= ['lat_spacecraft_weekly_w0%d_p202_v001.fits'%(i+10) for i in range(90)]
for i in range(300):
        filenamesp.append('lat_spacecraft_weekly_w%d_p202_v001.fits'%(i+100))
#file to write
f1=TFile('finaltree.root','RECREATE')
t1=TTree('Data of photon and spacecraft','Data events')
#array that we want
EVENTS = np.zeros(1, dtype=int)
TIME=np.zeros(1,dtype=float)
ENERGY = np.zeros(1, dtype=float)
ZENITH = np.zeros(1, dtype=float)
ZENITHSHIFT = np.zeros(1, dtype=float)
THETA = np.zeros(1, dtype=float)
PHI = np.zeros(1, dtype=float)
ALTITUDE = np.zeros(1,dtype=float)
PHI_EARTH = np.zeros(1,dtype=float)
#ROCK = np.zeros(1,dtype=float)
# create the branch of our tre
t1.Branch('EVENTS',EVENTS,'EVENTS/I')
t1.Branch('TIME',TIME,'TIME/D')
t1.Branch('ENERGY',ENERGY,'ENERGY/D')
t1.Branch('ZENITH',ZENITH,'ZENITH/D')
t1.Branch('ZENITHSHIFT',ZENITHSHIFT,'ZENITHSHIFT/D')
t1.Branch('THETA',THETA,'THETA/D')
t1.Branch('PHI',PHI,'PHI/D')
t1.Branch('ALTITUDE',ALTITUDE,'ALTITUDE/D')
t1.Branch('PHI_EARTH',PHI_EARTH,'PHI_EARTH/D')
#t1.Branch('ROCK',ROCK,'ROCK/D')

#freport=open('reportdat.olo','w')
#freport.truncate()
numberevent=0
processweek=0
for f in filename:
	file=pyfits.open(f)
	events=file[1].data
	for i in range(len(events)):
		if events[i]['EVENT_CLASS'][typedat]==True:
			numberevent+=1
			EVENTS[0]=numberevent
			TIME[0]=events[i]['TIME']
			ENERGY[0]=events[i]['ENERGY']/1000. #Gev
			ZENITH[0]=events[i]['ZENITH_ANGLE']
			ZENITHSHIFT[0]=zenithshift(events[i]['ZENITH_ANGLE'],processweek,events[i]['TIME'])
			THETA[0]=events[i]['THETA']
			PHI[0]=events[i]['PHI']
			ALTITUDE[0]=altitudesp(processweek,events[i]['TIME'])
			PHI_EARTH[0]=events[i]['EARTH_AZIMUTH_ANGLE']
			#ROCK[0]=rockang(processweek,events[i]['TIME'])
			t1.Fill()
			print f,i,numberevent
	processweek+=1
#freport.close()

# finish tree branch
f1.Write()
f1.Close()
