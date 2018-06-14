from Limb_package import *

# condition
n_simulation = 1
simtype = 1 # 1=Stat, 2=Tot
mode = 2 # 1=SPLwHe, 2=BPLwHe
fitalgorithm = 1 # 1=fmin,2=brute
f_dat_mea = 'alldat.olo'

if __name__ == '__main__':
    # setting
    initialguesspar, rangetrial, namealgorithm, model,\
         modelname,simname = setting(simtype, mode, fitalgorithm)
    # initialize model
    init_model(model)
    # get Eavgbin
    count_bin, Eavgbin = np.genfromtxt(f_dat_mea)[:,0], np.genfromtxt(f_dat_mea)[:,1]
    # open log file
    f_log = open("issue_6_Loglikelihood_"+modelname+namealgorithm+".dat",'w')
    ### optimize
    flux_mea = np.genfromtxt(f_dat_mea)[:,2]
    # let boss deal simulation
    boss = deal_simulation(count_bin, Eavgbin, flux_mea)
    # fit section
    if fitalgorithm == 1:
        bestfit = fmin(boss.SumlogPois, initialguesspar)
    if fitalgorithm == 2:
        bestfit = brute(boss.SumlogPois, rangetrial)
    print(bestfit)
    # boss.SumlogPois([25247.9912,2.65232725,2.57566350,90.1658378,0.000271940836])
    LoglikelihoodVal = boss.SLPS
    print("!! SLPS = ",LoglikelihoodVal)
    ### memo
    f_log.write('%f %f %f %f \n'%(LoglikelihoodVal,bestfit[1],bestfit[2],bestfit[3]))
    f_log.close()
    print("!! Done fit !!")
