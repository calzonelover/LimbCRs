from ROOT import *
from array import *
from math import *
import numpy as np

# Energy bin
oV=[(10**((float(i)/25)+1)) for i in range(51)]
V=array('d',oV)
# data
dat=np.genfromtxt('testdat.olo')
dN,Eavgbin,flux=dat[:,0],dat[:,1],dat[:,2]
datBPL=np.genfromtxt('bestBPL.olo')
xBPL,yBPL=datBPL[:,0],datBPL[:,1]
datSPL=np.genfromtxt('bestSPL.olo')
xSPL,ySPL=datSPL[:,0],datSPL[:,1]
# histogram
Elimb=TH1F('Elimb,','Elimb',len(V)-1,V)
Eband=TH1F('Eband','Eband',len(V)-1,V)
#EBPL=TH1F('EBPL','EBPL',len(yBPL)-1,yBPL)
#ESPL=TH1F('ESPL','ESPL',len(ySPL)-1,ySPL)
for i in range(50):
    Elimb.SetBinContent(i+1,flux[i]*(Eavgbin[i]**2.75))
    Elimb.SetBinError(i+1,Elimb.GetBinContent(i+1)/sqrt(dN[i]))
    Eband.SetBinContent(i+1,flux[i]*(Eavgbin[i]**2.75))
    if Eavgbin[i]<100.:
        syserr=0.05
    if Eavgbin[i]>=100.:
        syserr=0.05+0.1*(log10(Eavgbin[i]*1000.)-5.)
    toterr=syserr*Eband.GetBinContent(i+1)+Elimb.GetBinError(i+1)
    Eband.SetBinError(i+1,toterr)
for i in range(len(xSPL)):
    yBPL[i]=yBPL[i]*(xBPL[i]**2.75)
    ySPL[i]=ySPL[i]*(xSPL[i]**2.75)
#
gBPL=TGraph(len(yBPL),array('d',xBPL),array('d',yBPL))
gSPL=TGraph(len(ySPL),array('d',xSPL),array('d',ySPL))
#
C=TCanvas('C','C',800,600)
C.SetLogx()
C.SetLogy()
Elimb.SetStats(0)
Eband.SetFillColor(2)
Elimb.GetYaxis().SetTitle('E^{2.75}Flux (GeV^{1.75}m^{-2}s^{-1}sr^{-1})')
Eband.GetXaxis().SetTitle('E (GeV)')
Elimb.Draw('E1')
Eband.SetFillColorAlpha(kRed,0.3)
Elimb.SetTitle('Measurement')
# build legend
gSPL.SetLineWidth(2)
gSPL.SetLineStyle(2)
gSPL.SetFillColor(0)
gSPL.SetLineColor(4)
gSPL.SetTitle('Model incident proton SPL')
gSPL.Draw('same')
gBPL.SetLineWidth(3)
gBPL.SetLineStyle(5)
gBPL.SetFillColor(0)
gBPL.SetLineColor(8)
gBPL.SetTitle('Model incident proton BPL')
gBPL.Draw('same')
C.BuildLegend()
# band
Eband.Draw('E3same')
#
Elimb.SetTitle('Model vs Measurement')
# drw point
Elimb.SetMarkerStyle(20)
Elimb.SetMarkerColor(2)
Elimb.SetLineColor(2)
Elimb.Draw('E1same')
gSPL.Draw('same')
gBPL.Draw('same')
raw_input()
