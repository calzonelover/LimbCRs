
from ROOT import *
from math import *
from array import *
import numpy as np
from scipy.optimize import fmin,brute
import os
import sys

def def_Hist_Sys_Stat(f_dat_mea):# define histogram with mean is Flux*E^2.75
    Filedat = np.genfromtxt(f_dat_mea)
    Eavgbin, Flux_mea = Filedat[:,1], Filedat[:,2]
    Flux275_mea = np.multiply(Flux_mea, np.power(Eavgbin,2.75))
    Hist_Stat = []
    Hist_Tot = []
    for i in range(len(Flux_mea)):
        Hist_Stat.append(TH1F('Stat%d'%i,'Stat%d'%i,len(Flux275_mea)\
            ,Flux275_mea[i]*0.2,Flux275_mea[i]*2.0))
        Hist_Tot.append(TH1F('Tot%d'%i,'Tot%d'%i,len(Flux275_mea)\
            ,Flux275_mea[i]*0.2,Flux275_mea[i]*2.0))
    return Hist_Stat, Hist_Tot

def setting(simtype,mode,fitalgorithm): # setting
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
		rangetrial=[slice(5000.,35000.,5000.),slice(2.5,3.0,0.01)\
			,slice(2.5,3.0,0.5),slice(200.,400.,200.),slice(0.0001,0.0003,0.0001)]
	if mode==2:
		rangetrial=[slice(5000.,35000.,5000.),slice(2.5,3.0,0.01)\
			,slice(2.5,3.0,0.01),slice(200.,400.,5.),slice(0.0001,0.0003,0.0001)]
    # just name of fit algorithm
	if fitalgorithm==1:
		namealgorithm='fmin'
	if fitalgorithm==2:
		namealgorithm='brute'
	return initialguesspar,rangetrial,namealgorithm,model

def init_model(model):
	os.system('gfortran %s frag.f -o test1.out' %(model))

def Fluxcompute(A,gamma1,gamma2,Ebreak,normAll):
	RunFlux='./test1.out %f %f %f %f %f'%(A,gamma1,gamma2,Ebreak,normAll)
	os.system(RunFlux)

def SumlogPois(dummy, Filedat):
	# get parameter
	A = dummy[0]
	gamma1 = dummy[1]
	gamma2 = Ebreak[2]
	Ebreak = dummy[3]
	normAll = dummy[4]
	# simulation (in gfortran)
	Fluxcompute(A,gamma1,gamma2,Ebreak,normAll)
	# get data from measurement
	E_mea, F_mea = Filedat[:,1], Filedat[:,2]
	gF_mea = TGraph(len(E_mea), array('d',E_mea), array('d',F_mea))
	# get data from simulation
	dat_sim = np.genfromtxt(Filedat)
	x, y = data_sim[:,0], data_sim[:,1]
	sumlogpois = 0.
	for i in range(len(x)):
		measurement = gF_mea.Eval(x[i])
		model = y[i]
		if TMath.Poisson(measurement,model) == 0:
			sumlogpois += 308.
		if TMath.Poisson(measurement,model) != 0:
			sumlogpois += -log(TMath.Poisson(measurement,model))
	return sumlogpois

def Sim_Flux_Stat(f_dat_mea):
    Filedat = np.genfromtxt(f_dat_mea)
    dNsb, Eavgbin, flxlimb = Filedat[:,0], Filedat[:,1], Filedat[:,2]
    flux_stat = []
    for i in range(len(flxlimb)):
        flux_stat.append(flxlimb[i]/dNsb[i]*gRandom.PoissonD(dNsb[i]))
    return flux_stat

def Sim_Flux_Tot(f_dat_mea):
	Filedat = np.genfromtxt(f_dat_mea)
	dNsb, Eavgbin, flxlimb = Filedat[:,0], Filedat[:,1], Filedat[:,2]
	flux_tot = []
	EdummySys = []
	EdummySys.append(Eavgbin[0])
	EdummySys.append(Eavgbin[24])
	EdummySys.append(Eavgbin[49])
	ErrordummySys = []
	ErrordummySys.append(1.0+gRandom.Gaus(0,0.05))
	ErrordummySys.append(1.0+gRandom.Gaus(0,0.05))
	ErrordummySys.append(1.0+gRandom.Gaus(0,0.15))
	gErrorSys = TGraph(3, array('d',EdummySys), array('d', ErrordummySys))
	for i in range(len(flxlimb)):
		flux_tot.append(flxlimb[i]/dNsb[i]*gRandom.PoissonD(dNsb[i])\
			*gErrorSys.Eval(Eavgbin[i],0,'S'))
	return flux_tot

def write_sim_to_ROOTFile(Hist_Stat, Hist_Tot, name_f_root):
    F_ROOT = TFile(name_f_root, 'RECREATE')
    for j in range(len(Hist_Stat)):
        Hist_Stat[j].Write()
        Hist_Tot[j].Write()
    F_ROOT.Close() 
def Flux_to_Flux275(Eavgbin, Flux):
    return np.multiply(Flux,np.power(Eavgbin,2.75))
def ScanMountain(f_dat_mea, mode):
    initialguesspar, rangetrial, namealgorithm, model = setting(simtype, mode, fitalgorithm)
    # init model
    init_model(model)
    return 



















