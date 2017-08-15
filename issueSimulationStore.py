from ROOT import *
from math import *
from array import *
import numpy as np
global Filedat
# my condition
number_simulation=2
def SimulateStat(flux275): # Simlate Random count (Stat. err.)
	flux275=[]
	dNsb,Eavgbin,flxlimb=Filedat[:,0],Filedat[:,1],Filedat[:,2]
	for i in range(len(dNsb)):
		flux275.append((flxlimb[i]/dNsb[i])*gRandom.PoissonD(dNsb[i])*(Eavgbin[i]**2.75))
        print 'test',i,len(dNsb)
	return flux275
def SimulateSys(flux275):
    flux275=[]
    dNsb,Eavgbin,flxlimb=Filedat[:,0],Filedat[:,1],Filedat[:,2]
    simtot10GeV_flux=gRandom.Gaus(flxlimb[0],flxlimb[0]*0.05) # Error 5% at 10GeV
    simtot100GeV_flux=gRandom.Gaus(flxlimb[24],flxlimb[24]*0.05) # Error 5% at 100GeV
    simtot1000GeV_flux=gRandom.Gaus(flxlimb[49],flxlimb[49]*0.15) #Error 15% at 10GeV
    flux275.append(simtot10GeV_flux*(Eavgbin[0]**2.75))
    flux275.append(simtot100GeV_flux*(Eavgbin[24]**2.75))
    flux275.append(simtot1000GeV_flux*(Eavgbin[49]**2.75))
    return flux275
def SimulateTot(flux275): # include
	flux275=[]
	dNsb,Eavgbin,flxlimb=Filedat[:,0],Filedat[:,1],Filedat[:,2]
	# simulate random coutn (Statistical error)
	simstat10GeV_flux=(flxlimb[0]/dNsb[0])*gRandom.PoissonD(dNsb[0])
	simstat100GeV_flux=(flxlimb[24]/dNsb[24])*gRandom.PoissonD(dNsb[24])
	simstat1000GeV_flux=(flxlimb[49]/dNsb[49])*gRandom.PoissonD(dNsb[49])
	# simulate Systematic error (Aeff err.)
	simtot10GeV_flux=gRandom.Gaus(simstat10GeV_flux,simstat10GeV_flux*0.05) # Error 5% at 10GeV
	simtot100GeV_flux=gRandom.Gaus(simstat100GeV_flux,simstat100GeV_flux*0.05) # Error 5% at 100GeV
	simtot1000GeV_flux=gRandom.Gaus(simstat1000GeV_flux,simstat1000GeV_flux*0.15) #Error 15% at 10GeV
	flux275.append(simtot10GeV_flux*(Eavgbin[0]**2.75))
	flux275.append(simtot100GeV_flux*(Eavgbin[24]**2.75))
	flux275.append(simtot1000GeV_flux*(Eavgbin[49]**2.75))
	return flux275
# open dat file
Filedat=np.genfromtxt('alldat.olo')
Eavgbin=Filedat[:,1]
# initialize tree
ft=TFile('MontySim.root','RECREATE')
t1=TTree('Simulation tree','data simulation')
# array want to insert in tree
SimStat=np.zeros(1,dtype=float)
SimSys=np.zeros(1,dtype=float)
SimTot=np.zeros(1,dtype=float)
# declare branch in tree
t1.Branch('SimStat',SimStat,'SimStat/D')
t1.Branch('SimSys',SimSys,'SimSys/D')
t1.Branch('SimTot',SimTot,'SimTot/D')
for i in range(number_simulation):
    # Simulation
    SStat=[]
    SStat=SimulateStat(SStat)
    SSys=[]
    SSys=array('d',SimulateSys(SSys))
    SStat=[]
    SStat=array('d',SimulateTot(SStat))
    print 'bue',SStat
    # insert in tree
    SimStat[0]=SStat
    SimSys[0]=SSys
    SimTot[0]=SStat
    t1.Fill()
# close dat file
ft.Close()
