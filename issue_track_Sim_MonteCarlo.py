from ROOT import *
from math import *
from array import *
import numpy as np
from scipy.optimize import fmin,brute
import os
import sys
global Filedat
# my condition
number_simulation=2
simtype = 1# 1=Stat, 2=Tot
mode=1 # 1=SPLwHe, 2=BPLwHe
fitalgorithm=1 # 1=fmin,2=brute
# Resolution of hill (when use brute force)
def def_Hist_Sys_Stat(Flux275_mea):
    Hist_Stat = []
    Hist_Tot = []
    for i in range(len(Eavgbin)):
        Hist_Stat.append(TH1F('Stat%d'%i,'Stat%d'%i,len(Flux275_mea)\
            ,Flux275_mea[i]*0.2,Flux275_mea[i]*2.0))
        Hist_Tot.append(TH1F('Tot%d'%i,'Tot%d'%i,len(Flux275_mea)\
            ,Flux275_mea[i]*0.2,Flux275_mea[i]*2.0))
    return Hist_Stat, Hist_Tot
def setting(simtype,mode,fitalgorithm):
	# initial guess parameters
	if mode==1:
		modelname='SPLwHe'
		model='SPLwHe.f'
		# came from brute force
		initialguesspar=[25247.9912,2.65232725,2.57566350,90.1658378,0.000271940836]
	if mode==2:
		modelname='BPLwHe'
		model='BPLwHe.f'
		# came from brute force
		initialguesspar=[72287.4,2.7916925,2.60771950,349.226419,0.000197465908]
	# rangetrial
	if mode==1:
		rangetrial=[slice(5000.,35000.,5000.),slice(2.5,3.0,0.01),slice(2.5,3.0,0.5),slice(200.,400.,200.),slice(0.0001,0.0003,0.0001)]
	if mode==2:
		rangetrial=[slice(5000.,35000.,5000.),slice(2.5,3.0,0.01),slice(2.5,3.0,0.01),slice(200.,400.,5.),slice(0.0001,0.0003,0.0001)]
    # just name of fit algorithm
	if fitalgorithm==1:
		namealgorithm='fmin'
	if fitalgorithm==2:
		namealgorithm='brute'
	return initialguesspar,rangetrial,namealgorithm,model
def Fluxcompute(A,gamma1,gamma2,Ebreak,normAll):
	RunFlux='./test1.out %f %f %f %f %f'%(A,gamma1,gamma2,Ebreak,normAll)
	os.system(RunFlux)
def SumlogPois(dummy):
	#print dummy
	A=dummy[0]
	gamma1=dummy[1]
	gamma2=dummy[2]
	Ebreak=dummy[3]
	normAll=dummy[4]
	Fluxcompute(A,gamma1,gamma2,Ebreak,normAll)
	file=open('0.dat')
	data=np.genfromtxt('0.dat')
	x,y=data[:,0],data[:,1]
	sumlogpois=0.
	for i in range(len(x)):
		measurement=Sim_Flux275.Eval(x[i],0,'S') # Cubic spline interpolate
		model=y[i]*(x[i]**2.75)
		if TMath.Poisson(measurement,model)==0:
			sumlogpois+=308.
		if TMath.Poisson(measurement,model)!=0:
			sumlogpois+=-log(TMath.Poisson(measurement,model))
	return sumlogpois
def Sim_Flux_Stat(flux275, Filedat): # Simlate Random count (Stat. err.)
	flux275=[]
	dNsb,Eavgbin,flxlimb=Filedat[:,0],Filedat[:,1],Filedat[:,2]
	for i in range(len(dNsb)):
		flux275.append((flxlimb[i]/dNsb[i]*(Eavgbin[i]**2.75))\
            *gRandom.PoissonD(dNsb[i]))
	return flux275
def Sim_Flux_Tot(flux275, Filedat): # include
	flux275=[]
	dNsb,Eavgbin,flxlimb=Filedat[:,0],Filedat[:,1],Filedat[:,2]
	# sim systematic distortion curve
	EdummySys=[]
	EdummySys.append(Eavgbin[0])
	EdummySys.append(Eavgbin[24])
	EdummySys.append(Eavgbin[49])
	ErrordummySys=[]
	ErrordummySys.append(1.00+gRandom.Gaus(0,0.05))
	ErrordummySys.append(1.00+gRandom.Gaus(0,0.05))
	ErrordummySys.append(1.00+gRandom.Gaus(0,0.15))
	gErrorSys=TGraph(3,array('d',EdummySys),array('d',ErrordummySys))
	for i in range(len(dNsb)):
		flux275.append((flxlimb[i]/dNsb[i]*(Eavgbin[i]**2.75))\
            *gRandom.PoissonD(dNsb[i])*gErrorSys.Eval(Eavgbin[i],0,'S'))
	return flux275
if __name__ == "__main__":
	# setting simulation
	initialguesspar,rangetrial,namealgorithm,model = setting(simytpe, mode, fitalgorithm)
	os.system('gfortran %s frag.f -o test1.out' %(model))
	# open dat file
	Filedat=np.genfromtxt('alldat.olo')
	Eavgbin, Flux_mea = Filedat[:,1], Filedat[:,2]
    Flux275_mea = np.multiply(Flux_mea,np.power(Eavgbin,2.75))
	# define histogram to collect simulation
    Hist_Stat, Hist_Tot = def_Hist_Sys_Stat(Flux275_mea)
    # start simulation
	for i in range(number_simulation):
		Flux275=[] # create global variable
        # Track Stat
        Flux275_Stat = Sim_Flux_Stat(Flux275, Filedat)
        for j in range(len(Flux275)):
            Hist_Stat[j].Fill(Flux275_Stat[j])
        # Track Tot
        Flux275_Tot = Sim_Flux_Tot(Flux275, Filedat)
        for j in range(len(Flux275)):
            Hist_Tot[j].Fill(Flux275_Tot[j])
        # save to root file
        File_Hist = TFile('Monte_Sim.root','RECREATE')
        for j in range(len(Hist_Stat)):
            Hist_Stat[j].Write()
            Hist_Tot[j].Write()
        File_Hist.Close()
