from ROOT import *
from math import *
from array import *
import numpy as np
import pyfits
from scipy.optimize import fmin,brute
import os
import sys
global gamma1,gamma2,Ebreak,alldat
def Fluxcompute(A,gamma1,gamma2,Ebreak,normAll):
    RunFlux='./test1.out %f %f %f %f %f'%(A,gamma1,gamma2,Ebreak,normAll)
    os.system(RunFlux)
def SumlogPois(dummy):
    #print dummy
    Norm=dummy[0]
    gamma1=dummy[1]
    gamma2=dummy[2]
    Ebreak=dummy[3]
    normAll=dummy[4]
    Fluxcompute(Norm,gamma1,gamma2,Ebreak,normAll)
    file=open('0.dat')
    data=np.genfromtxt('0.dat')
    x,y=data[:,0],data[:,1]
    sumlogpois=0.
    for i in range(len(x)):
        model=y[i]*(x[i]**2.75)
        measurement=g.Eval(x[i])
        if TMath.Poisson(measurement,model)==0:
            sumlogpois+=308.
        if TMath.Poisson(measurement,model)!=0:
            sumlogpois+=-log(TMath.Poisson(measurement,model))
    return sumlogpois
# initialize model
os.system('gfortran BPLwHe.f frag.f -o test1.out')
# gen data Limb
datlimb=np.genfromtxt('testdat.olo')
#datlimb=np.genfromtxt('alldat.olo')
Eavgbin=datlimb[:,10]
Flux=datlimb[:,11]
Flux275=[]
for i in range(50):
    Flux275.append(Flux[i]*(Eavgbin[i]**2.75))
g=TGraph(len(Eavgbin),array('d',Eavgbin),array('d',Flux275))
# find bestfit
trial=[10000.,2.849,2.716,336,0.00021]
rangetrial=[slice(5000.,35000.,5000.),slice(2.5,3.1,0.1),slice(2.5,3.1,0.1),slice(200.,400.,20.),slice(0.0001,0.0003,0.0001)]
#rangetrial=[slice(5000.,35000.,5000.),slice(2.5,3.0,0.1),slice(2.5,3.0,0.5),slice(200.,400.,20.),slice(0.0001,0.0003,0.0001)]
bestfit=fmin(SumlogPois,trial)
fuck=brute(SumlogPois,rangetrial)
print 'fmin',bestfit,'SLPS=',SumlogPois(bestfit)
print 'brute',fuck,'SLPS=',SumlogPois(fuck)
