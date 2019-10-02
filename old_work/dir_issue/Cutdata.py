from ROOT import *
from math import *
import pyfits

#week = [i for i in range(101,102)]

datadir = '/work/bow/data/'

#file = ['lat_photon_weekly_w0%d_p302_v001.fits'%(i+10) for i in range(90)]
file = ['lat_photon_weekly_w%d_p302_v001.fits'%(i) for i in range(100,400)]

#file = pyfits.open(datadir+'lat_photon_weekly_w200_p302_v001.fits')
#photon = file[1].data


for f in range(len(file)):
	
	fileph = pyfits.open(datadir+file[f])
	photon = fileph[1].data
	
	
	energy = photon.field('ENERGY') > 8000  
	energy_cut = photon[energy]
	
	print len(energy_cut)
	
	zenith = energy_cut.field('ZENITH_ANGLE') > 100
	zenith_cut = energy_cut[zenith]
	
	print len(zenith_cut)
	
		
	hdu = pyfits.BinTableHDU(zenith_cut)
	#hdu.writeto('select_photon_w%d.fits'%(f+10))
	hdu.writeto('select_photon_w%d.fits'%(f+100))

