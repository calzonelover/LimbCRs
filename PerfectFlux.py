from math import *
from ROOT import *
from array import *
import numpy as np
# our condition (Limb Peak at nadir 68.02)
Zmin=110.0 # nadir 70.0
Zmax=111.6 # nadir 68.4
Zbgmin=0. # nadir 90 ## 80
Zbgmax=106. # nadir 74 ## 72
solidangle=(cos(Zmin*(pi/180.))-cos(Zmax*(pi/180.)))*(2.*pi)
solidanglebg=(cos(Zbgmin*(pi/180.))-cos(Zbgmax*(pi/180.)))*2.*pi
# Energy bin
oV=[(10**((float(i)/25)+1)) for i in range(51)]
V=array('d',oV)
# Build count map
cntmap=[]
# open expmap
Fexpmap=TFile('ExpMap_P8R2_ULTRACLEANVETO_V6_w010-w399_2.root') # has two type (2) is newest
name_expmap=[]# declare map name in expmap
for i in range(50):
    namecntmap='cntmap%03d'%(i)
    cntmap.append(TH2F(namecntmap,namecntmap,180,0.,360.,800,0.,80.))
    name_expmap.append('expmap%03d'%(i))

# import data from tree
ev=TChain('Data of photon and spacecraft')
ev.Add('finaltree.root')
# Declare variable
dN=[] # raw count
dNbg=[] # background count
EdN=[]
EavgdN=[] # Energy average in each limb bin
EavgdNbg=[] # Energy average in each bg bin
dNsb=[] # dN subtract background
for i in range(50): #have 0-50 but interest just 1-50
    dN.append(0)
    dNbg.append(0)
    EdN.append(0)
    EavgdN.append(0)
    EavgdNbg.append(0)
    dNsb.append(0)


# process data
#mapt = TH1F('mapt','mapt',900,0.,90.)####
#mapt_shift = TH1F('mapt_shift','mapt_shift',900,0.,90.)
for event in ev:
    # original selection
    energy=ev.ENERGY
    if np.searchsorted(V,energy)>0 and np.searchsorted(V,energy)<51: # select photon range (10,1000)
        cntmap[np.searchsorted(V,energy)-1].Fill(event.PHI_EARTH,180.-event.ZENITH)
        # limb photon
        if event.ZENITH>Zmin and event.ZENITH<Zmax and event.THETA<70.:
            dN[np.searchsorted(V,energy)-1]+=1.
            EavgdN[np.searchsorted(V,energy)-1]+=energy # sum before, average in next for-loop
        # bg photon
        if event.ZENITH>Zbgmin and event.ZENITH<Zbgmax and event.THETA < 70.:# bg count
            dNbg[np.searchsorted(V,energy)-1]+=1.
            EavgdNbg[np.searchsorted(V,energy)-1]+=energy
'''    # correct bias
    energy=0.963*ev.ENERGY # bias energy
    if np.searchsorted(V,energy)>0 and np.searchsorted(V,energy)<51: # select photon range (10,1000)
        cntmap[np.searchsorted(V,energy)-1].Fill(event.PHI_EARTH,180.-event.ZENITHSHIFT)
        # limb photon
        if event.ZENITHSHIFT>Zmin and event.ZENITHSHIFT<Zmax and event.THETA < 70.:# limb count
            dN[np.searchsorted(V,energy)-1]+=1.
            EavgdN[np.searchsorted(V,energy)-1]+=energy # sum before, average in next for-loop
        # bg photon
        if event.ZENITHSHIFT>Zbgmin and event.ZENITHSHIFT<Zbgmax and event.THETA < 70.:# bg count
            dNbg[np.searchsorted(V,energy)-1]+=1.
            EavgdNbg[np.searchsorted(V,energy)-1]+=energy
'''

# create strMap
strmap=TH2F('strmap','strmap',180,0.,360.,800,0.,80.)
dphi=(360./strmap.GetNbinsX())*pi/180.
dtheta=(80./strmap.GetNbinsY())*pi/180.
for j in range(strmap.GetNbinsY()):
    strbin=dphi*dtheta*sin((j+0.5)*dtheta) # d(phi)d(theta)sin(theta)
    for i in range(strmap.GetNbinsX()):
        strmap.SetBinContent(i+1,j+1,strbin)
# define flxmap
flxmap=[]
for i in range(50):
    flxmapadd=cntmap[i].Clone()
    flxmap.append(flxmapadd)
flxvallimb=[]
flxvalbg=[]
# write dNsb,EavgdN to file
f1=file('alldat.olo','w')
for i in range(len(V)-1):
    # dE
    dE=V[i+1]-V[i]
    # Flxmap : flxmap=(cntmap/expmap)/dE/dOmega
    expmap=Fexpmap.Get(name_expmap[i])
    expmap.Scale(1./10000.) # cm^2->m^2
    #
    flxmap[i].Divide(cntmap[i],expmap)
    #flxmap[i].Divide(flxmap[i],strmap) ###
    flxmap[i].Scale(1./dE)
    ####
    #flxmap[i].Divide(flxmap[i],strmap) ####
    ####
    # get flux value limb
    flxmap[i].GetXaxis().SetRangeUser(0.,360.)
    flxmap[i].GetYaxis().SetRangeUser(180.-Zmax,180.-Zmin)
    flxvallimb.append(flxmap[i].Integral()/solidangle)
    # get flux value bg
    flxmap[i].GetXaxis().SetRangeUser(0.,360.)
    flxmap[i].GetYaxis().SetRangeUser(180.-Zbgmax,180.-Zbgmin)
    flxvalbg.append(flxmap[i].Integral()/solidanglebg)
    #
    dNsb[i]=dN[i]-dNbg[i]*((Zmin-Zmax)/(Zbgmin-Zbgmax)) # weight str bg ti str limb
    EavgdN[i]=EavgdN[i]/dN[i]
    EavgdNbg[i]=EavgdNbg[i]/dNbg[i]
    f1.write('%f %f %e %f %f %e\n'%(dNsb[i],EavgdN[i],flxvallimb[i],dNbg[i],EavgdNbg[i],flxvalbg[i]))
    print dN[i]
    # write count map in root file

#####################
# Just Visualize map
######################
lbOS=-0.13 #Z-axis label offset
lbS=0.05   #Z-axis label size
ttOS=0.5   #Z-axis tltle offset
ttS=0.04   #Z-axis tltle size
C=TCanvas('C','C',800,600)
C.Divide(2,2)
C.cd(1)
C.cd(1).SetLogz()
gStyle.SetPalette(kRainBow)
expmap=flxmap[0]
#expmap=Fexpmap.Get(name_expmap[0]) ###
expmap.SetStats(0)
gPad.SetTheta(-90)
gPad.SetPhi(-90)
expmap.Draw('SURF2POLZ')
expmap.GetXaxis().SetTitle('#phi (degree)')
expmap.GetYaxis().SetTitle('#theta_{nadir} (degree)')
expmap.GetYaxis().SetRangeUser(62.,80.)
expmap.GetZaxis().SetLabelOffset(lbOS)
expmap.GetZaxis().SetLabelSize(lbS)
expmap.GetZaxis().SetTitleOffset(ttOS)
expmap.GetZaxis().SetTitleSize(ttS)
expmap.GetZaxis().SetTitle('Flux (GeV^{-1}s^{-1}sr^{-1}m^{-2})') #
expmap.SetTitle('Flux map 10.000-10.965 GeV')
#C.cd(1).SetLogz()
C.cd(2)
expmap2=flxmap[12]
#expmap2=Fexpmap.Get(name_expmap[12]) ###
expmap2.SetStats(0)
expmap2.Draw('SURF2POLZ')
gPad.SetTheta(-90)
gPad.SetPhi(-90)
expmap2.GetXaxis().SetTitle('#phi (degree)')
expmap2.GetYaxis().SetTitle('#theta_{nadir} (degree)')
expmap2.GetYaxis().SetRangeUser(62.,80.)
expmap2.GetZaxis().SetLabelOffset(lbOS)
expmap2.GetZaxis().SetLabelSize(lbS)
expmap2.GetZaxis().SetTitleOffset(ttOS)
expmap2.GetZaxis().SetTitleSize(ttS)
expmap2.GetZaxis().SetTitle('Flux (GeV^{-1}s^{-1}sr^{-1}m^{-2})') #
expmap2.SetTitle('Flux map 30.200-33.113 GeV')
C.cd(2).SetLogz()
C.cd(3)
expmap3=flxmap[24]
#expmap3=Fexpmap.Get(name_expmap[24]) ###
expmap3.SetStats(0)
expmap3.Draw('SURF2POLZ')
gPad.SetTheta(-90)
gPad.SetPhi(-90)
expmap3.GetXaxis().SetTitle('#phi (degree)')
expmap3.GetYaxis().SetTitle('#theta_{nadir} (degree)')
expmap3.GetYaxis().SetRangeUser(62.,80.)
expmap3.GetZaxis().SetLabelOffset(lbOS)
expmap3.GetZaxis().SetLabelSize(lbS)
expmap3.GetZaxis().SetTitleOffset(ttOS)
expmap3.GetZaxis().SetTitleSize(ttS)
expmap3.GetZaxis().SetTitle('Flux (GeV^{-1}s^{-1}sr^{-1}m^{-2})') #
expmap3.SetTitle('Flux map 91.201-100.000 GeV')
C.cd(3).SetLogz()
C.cd(4)
expmap4=flxmap[49]
#expmap4=Fexpmap.Get(name_expmap[49]) ###
expmap4.SetStats(0)
expmap4.Draw('SURF2POLZ')
gPad.SetTheta(-90)
gPad.SetPhi(-90)
expmap4.GetXaxis().SetTitle('#phi (degree)')
expmap4.GetYaxis().SetTitle('#theta_{nadir} (degree)')
expmap4.GetYaxis().SetRangeUser(62.,80.)
expmap4.GetZaxis().SetLabelOffset(lbOS)
expmap4.GetZaxis().SetLabelSize(lbS)
expmap4.GetZaxis().SetTitleOffset(ttOS)
expmap4.GetZaxis().SetTitleSize(ttS)
expmap4.GetZaxis().SetTitle('Flux (GeV^{-1}s^{-1}sr^{-1}m^{-2})') #
expmap4.SetTitle('Flux map 912.011-1000.000 GeV')
C.cd(4).SetLogz()
raw_input()
#####
# Close all file
Fexpmap.Close()
f1.close()
