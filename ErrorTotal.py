from ROOT import *
from math import *
from array import *
import numpy as np
from scipy.optimize import fmin,brute
import os
import sys
global Filedat,Ebinbefore,Ebin
# my condition
number_simulation=2
mode=1 # 1=SPLwHe, 2=BPLwHe
fitalgorithm=1 # 1=fmin,2=brute
# Resolution of hill (when use brute force)
if mode==1:
	rangetrial=[slice(5000.,35000.,5000.),slice(2.5,3.0,0.01),slice(2.5,3.0,0.5),slice(200.,400.,200.),slice(0.0001,0.0003,0.0001)]
if mode==2:
	rangetrial=[slice(5000.,35000.,5000.),slice(2.5,3.0,0.01),slice(2.5,3.0,0.01),slice(200.,400.,5.),slice(0.0001,0.0003,0.0001)]
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
	file.close()
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
def SimulateFlux(flux275): # include
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
		flux275.append((flxlimb[i]/dNsb[i])
			*gRandom.PoissonD(dNsb[i])*(Eavgbin[i]**2.75)
			*gErrorSys.Eval(Eavgbin[i],0,'S'))
	return flux275
if __name__ == "__main__":
	# Initialize model
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
	os.system('gfortran %s frag.f -o test1.out' %(model))
	# open dat file
	Filedat=np.genfromtxt('alldat.olo')
	Eavgbin=Filedat[:,1] # GOT Emidbin
    # open to write output parameters
	if fitalgorithm==1:
		namealgorithm='fmin'
	if fitalgorithm==2:
		namealgorithm='brute'
	foutput=open(modelname+namealgorithm+'Total.dat','w')
	for i in range(number_simulation):
		Flux275=[] # create global variable
		Flux275=SimulateFlux(Flux275) # simulate new flux (Random Error stat.)
		Sim_Flux275=TGraph(50,array('d',Eavgbin),array('d',Flux275))
		if mode==1: #SPLwHe
			if fitalgorithm==1:
				bestfit=fmin(SumlogPois,initialguesspar)
			if fitalgorithm==2:
				bestfit=brute(SumlogPois,rangetrial)
		if mode==2: #BPLwHe
			if fitalgorithm==1:
				bestfit=fmin(SumlogPois,initialguesspar)
			if fitalgorithm==2:
				bestfit=brute(SumlogPois,rangetrial)
		foutput.write('%f %f %f \n' %(bestfit[1],bestfit[2],bestfit[3]))
# close dat file
foutput.close()
