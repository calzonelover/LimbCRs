from ROOT import *
from array import *
from math import *
import pyfits

#filename photon
filename = ['select_photon_w%d.fits'%(i+10) for i in range(390)]
#fileneme spacecraft
filenamesp= ['lat_spacecraft_weekly_w0%d_p202_v001.fits'%(i+10) for i in range(90)]
for i in range(300):
    filenamesp.append('lat_spacecraft_weekly_w%d_p202_v001.fits'%(i+100))

def rE(latitude): #Ref from https://en.wikipedia.org/wiki/Earth_radius
        latitude=radians(latitude)
        ae=6378.1370
        be=6356.7523
        up=(((ae**2.)*cos(latitude))**2.)+(((be**2.)*sin(latitude))**2.)
        down=((ae*cos(latitude))**2.)+((be*sin(latitude))**2.)
        return sqrt(up/down)
def altitudesp(processweek,missiontime):
        #for fspace in filenamesp: #dont forget set filename->filenamespace
        fsp=pyfits.open(filenamesp[processweek])
        eventsp=fsp[1].data
        for i in range(len(eventsp)):
		if missiontime>=eventsp[i]['START'] and i>=len(eventsp)-1:
			return eventsp[i]['RAD_GEO']/1000.0
		if missiontime>=eventsp[i]['START'] and missiontime<eventsp[i+1]['START']:
			return ((eventsp[i]['RAD_GEO']+eventsp[i+1]['RAD_GEO'])/2.0)/1000.0


def zenithshift(zenithang,missiontime):
        return zenithang-(0.0211*(550.0-altitudesp(missiontime)))
#Create graph
galtitude=TH1F('galtitude','Altitude theta<70 zenith > 100',100,520.,575.)



processweek=0
sum_livetime = 0
for f in filenamesp:
    file=pyfits.open(f)
    eventsp=file[1].data
    print(f, '%e'%sum_livetime)
    for i in range(len(eventsp)):
        sum_livetime += eventsp[i]['LIVETIME']
#		if events[i]['THETA'] < 70.0 and events[i]['ZENITH_ANGLE'] > 100.0:
#			galtitude.Fill(altitudesp(processweek,events[i]['TIME']))
#    		print events[i]['ROCK_ANGLE']
#    processweek+=1
#Cgaltitude=TCanvas('Cg','Cg',800,600)
#galtitude.Draw()
        # if events[i]['ROCK_ANGLE'] > 52.0:	# past 42 
           # sum_livetime += events[i]['LIVETIME']
#            print f,i,sum
#sum over all = 70761348.6153
# over all at ROCK_ANGLE > 42 => livetime = 70545074.725537941
# over all at ROCK_ANGLE > 42 => livetime = 5294102.3631355334
print "finish, livetime = ",sum_livetime
raw_input()
