import pyIrfLoader
from ROOT import *
from math import *
from array import *
import numpy as np
import pyfits

pyIrfLoader.Loader_go()
myFactory = pyIrfLoader.IrfsFactory_instance()
irfs_f = myFactory.create("P8R2_SOURCE_V6::FRONT")
irfs_b = myFactory.create("P8R2_SOURCE_V6::BACK")
aeff_f = irfs_f.aeff()
aeff_b = irfs_b.aeff()

#CE1=TCanvas("CE1","CE1",800,600)

filename = ['select_photon_w%d.fits'%(i+10) for i in range(390/100)]
CE1=TCanvas("CE1","Canvas Discrete Energy",800,600)
oV=[(10**((float(i)/25)+1)) for i in range(51)]
V=array('d',oV)
print V
E1=TH1F("E1","Discrete Energy",len(V)-1,V)
    
for f in filename:
	file=pyfits.open(f)
	events=file[1].data
	for i in range(len(events)):
		if events[i]['ZENITH_ANGLE'] > 100 and events[i]['ENERGY']> 8000 and events[i]['EVENT_CLASS'][24] == True and (180-events[i]['THETA'])> 68.4 and events[i]['THETA'] < 70:			
			E1.Fill(events[i]['ENERGY']/1000.)
			if i<20:
				print f,i

E1.Draw('E1')
CE1.SetLogy()
CE1.SetLogx()
E1.GetXaxis().SetTitle("E (GeV)")
E1.GetYaxis().SetTitle("dN")
func1=TF1("func1","10**([0]*x**[1])",1,2)
E1.Fit("func1","0")
func1.Draw("same")
print "finish E1"

gamma=2.66
livetime=70761348.6153
onV=[(10**((float(i)/50.)*6)) for i in range(51)]
nV=array('d',onV)

Cexp=TCanvas("Cexp","Exposure map (theta=61.5)",800,600)
Eexp=TH1F('Eexp','Exposure map (theta=61.5)',len(nV)-1,nV)
#Eexp=E1.Clone('Eexp')
for i in range(E1.GetNbinsX()):
	E2d=(Eexp.GetBinLowEdge(i+1)+Eexp.GetBinWidth(i+1))**(1-gamma)
	E1d=(Eexp.GetBinLowEdge(i+1))**(1-gamma)
	In=log((0.5*(E2d-E1d))+E1d)
	Emidbin=exp(In/(1-gamma))
	exposure=(aeff_f.value(Emidbin,61.5,0)+aeff_b.value(Emidbin,61.5,0))/10000.
	Eexp.SetBinContent(i+1,exposure)
	#Eexp.SetBinError(i+1,i+1,0,0)
	print i,Emidbin,exposure
#Eexp=TGraph(len(V),V,y)
Cexp.SetLogx()
Eexp.Draw('P')
Eexp.SetMarkerStyle(22)
print "finish exposure"

Ednde=E1.Clone('Ednde')
for i in range(E)


E2=E1.Clone('E2')
for i in range(E2.GetNbinsX()):
	E2d=(E2.GetBinLowEdge(i+1)+E2.GetBinWidth(i+1))**(1-gamma)
	E1d=(E2.GetBinLowEdge(i+1))**(1-gamma)
	In=log((0.5*(E2d-E1d))+E1d)
	Emidbin=exp(In/(1-gamma))
	exposure=(aeff_f.value(Emidbin*1000,61.5,0)+aeff_b.value(Emidbin*1000,61.5,0))/10000.
	exposure=1
	E2.SetBinContent(i+1,(E1.GetBinContent(i+1)/exposure)/livetime)
	E2.SetBinError(i+1,(E1.GetBinError(i+1)/exposure)/livetime)
	print i,Emidbin
CE2=TCanvas("CE2","CE2",800,600)
#g.GetXaxis().SetRangeUser(10.0,1000.0)
E2.Draw("E1")
CE2.SetLogy()
CE2.SetLogx()
E2.GetXaxis().SetTitle("E (GeV)")
E2.GetYaxis().SetTitle("Flux (m^{-2}*s^{-1})")
E2.SetTitle("Flux")
func2=TF1("func2","[0]*(x**[1])",10,1000)
E2.Fit("func2","0")
func2.Draw("same")
print "finish Flux"

E3=E2.Clone('E3')
for i in range(E3.GetNbinsX()):
	E2d=(E3.GetBinLowEdge(i+1)+E3.GetBinWidth(i+1))**(1-gamma)
	E1d=(E3.GetBinLowEdge(i+1))**(1-gamma)
	In=log((0.5*(E2d-E1d))+E1d)
	Emidbin=exp(In/(1-gamma))
	E3.SetBinContent(i+1,(E2.GetBinContent(i+1))*(Emidbin**2.75))
	E3.SetBinError(i+1,(E2.GetBinError(i+1))*(Emidbin**2.75))
	print i
CE3=TCanvas("CE3","CE3",800,600)
E3.Draw('E1')
CE3.SetLogy()
CE3.SetLogx()
E3.GetXaxis().SetTitle("E (GeV)")
E3.GetYaxis().SetTitle("E^{2.75}*Flux (m^{-2}*s^{-1})")
E3.SetTitle("E^{2.75}*Flux")
print "finish"

print nV
raw_input()
