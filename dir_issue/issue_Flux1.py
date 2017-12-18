
import pyLikelihood
import pyIrfLoader
from ROOT import *
from math import *
from array import *
import pyfits
import numpy as np
#mycondition
Zmin=110.0
Zmax=111.6
evclass=24 #source
livetime=70761348.6153 #approximation
solidangle=(cos(Zmin*(pi/180.))-cos(Zmax*(pi/180.)))*2.*pi
# setting LAT performance
pyIrfLoader.Loader_go()
myFactory=pyIrfLoader.IrfsFactory_instance()
irfs_f=myFactory.create("P8R2_SOURCE_V6::FRONT") # use source
irfs_b=myFactory.create("P8R2_SOURCE_V6::BACK") # use source
aeff_f=irfs_f.aeff()
aeff_b=irfs_b.aeff()
#file photon
filename = ['select_photon_w%d.fits'%(i+10) for i in range(390)]
# Energy bin
oV=[(10**((float(i)/25)+1)) for i in range(51)]
V=array('d',oV)
# open file dN.root (we already have dN.root)
filedN=TFile('dN.root')
filedN.ls()
h=filedN.Get('E1')
# Read energy average in each bin
dataEavgbin=np.genfromtxt('Eavgbin.olo')
Eavgbin=dataEavgbin[:,1]
# flux extraction
for i in range(50):
	i=i+1
	rand=gRandom.PoissonD(h.GetBinContent(i))
	LATperformance=(aeff_f.value(Eavgbin[i-1]*1000.,61.5,0.)+aeff_b.value(Eavgbin[i-1]*1000.,61.5,0.))/10000.
	print (((h.GetBinContent(i)/h.GetBinWidth(i))/livetime)/solidangle)/LATperformance
	h.SetBinContent(i,rand) # Generate random new dN 'Monte carlo'
	h.SetBinContent(i,(((h.GetBinContent(i)/h.GetBinWidth(i))/livetime)/solidangle)/LATperformance) #dN-> (dN)/dE/livetime/solidang/performance 'flux'
	print h.GetBinContent(i)
# draw
#C=TCanvas('C','C',800,600)
#h.Draw('E1')

print "finish "
# save to root
fflux=TFile('flux.root','RECREATE')
h.Write()
fflux.Write()
fflux.Close()


filedN.Close()
