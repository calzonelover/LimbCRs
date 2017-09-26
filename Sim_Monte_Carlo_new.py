from Limb_package import *

# condition
n_simulation = 2000
simtype = 1# 1=Stat, 2=Tot
mode = 1 # 1=SPLwHe, 2=BPLwHe
fitalgorithm = 1 # 1=fmin,2=brute
f_dat_mea = 'alldat.olo'
if __name__ == '__main__':
    # setting
    initialguesspar, rangetrial, namealgorithm, model = setting(simtype, mode, fitalgorithm)
    # initialize model
    init_model(model)
    Eavgbin = np.genfromtxt(f_dat_mea)[:,1]
    # open dat file
    Hist_Stat, Hist_Tot = def_Hist_Sys_Stat(f_dat_mea)
    for i in range(n_simulation):
        flux_stat = Sim_Flux_Stat(f_dat_mea)
        flux275_stat = Flux_to_Flux275(Eavgbin, flux_stat)
        flux_tot = Sim_Flux_Tot(f_dat_mea)
        flux275_tot = Flux_to_Flux275(Eavgbin, flux_tot)
        for j in range(len(flux_stat)):
            Hist_Stat[j].Fill(flux275_stat[j])
            Hist_Tot[j].Fill(flux275_tot[j])
    # write
    write_sim_to_ROOTFile(Hist_Stat, Hist_Tot, 'Monte_Sim.root')
    exit()
    a = np.array([2])
    flux_tot = []
    flux = Sim_Flux_Tot(flux_tot, 'alldat.olo')
    print flux