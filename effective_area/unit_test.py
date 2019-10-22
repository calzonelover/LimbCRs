import pyLikelihood
import pyIrfLoader
import os
import math
import numpy as np
import pyfits
import matplotlib.pyplot as plt

import settings

FIX_PHI_LAT = 0.0
FIX_THETA_LAT = 0.0

CM2_TO_M2 = 10000.0
GEV_TO_MEV = 1000.0

PATH_SAVE_EFF = os.path.join(
    os.getcwd(),
    "effective_area",
    "static_table",
    settings.IRF_NAME
)

LOG_EFF_FRONT = []
LOG_EFF_BACK = []
LOG_EFF = []

'''

This script has been design for only python2.7

'''

def getEnergyMidBins(e_start_gev=settings.E_START_GEV, e_stop_gev=settings.E_STOP_GEV, n_bins=settings.N_E_BINS):
    energy_edge_bins = [
        e_start_gev * math.pow(e_stop_gev/e_start_gev, float(i)/float(n_bins))
        for i in range(n_bins+1)
    ]
    _energy_mid_bins = []
    for i in range(n_bins):
        divider = 1.0 - float(settings.GAMMA)
        e2d = math.pow(energy_edge_bins[i+1], divider)
        e1d = math.pow(energy_edge_bins[i], divider)
        ln = math.log(0.5*(e2d - e1d)+ e1d)
        _energy_mid_bins.append(math.exp(ln/(divider)))
    return _energy_mid_bins

def main():
    phi_lats = [i*45.0 for i in range(8)]
    theta_lats = [i for i in range(int(settings.THETA_LAT_CUTOFF)+1)]
    energy_mid_bins = np.logspace(-2, 4, 100, base=10.0)# getEnergyMidBins(1e-2, 1e4, 100)
    print(energy_mid_bins)

    pyIrfLoader.Loader_go()
    myFactory = pyIrfLoader.IrfsFactory_instance()
    irfs_f = myFactory.create("%s::FRONT"%settings.IRF_NAME)
    irfs_b = myFactory.create("%s::BACK"%settings.IRF_NAME)
    aeff_f = irfs_f.aeff()
    aeff_b = irfs_b.aeff()
    for energy_mid_bin in energy_mid_bins:
        eff_front = aeff_f.value(GEV_TO_MEV*energy_mid_bin, FIX_THETA_LAT, FIX_PHI_LAT)/CM2_TO_M2
        eff_back = aeff_b.value(GEV_TO_MEV*energy_mid_bin, FIX_THETA_LAT, FIX_PHI_LAT)/CM2_TO_M2
        eff = eff_front + eff_back
        LOG_EFF_FRONT.append(eff_front)
        LOG_EFF_BACK.append(eff_back)
        LOG_EFF.append(eff)
    # visualize
    plt.plot(energy_mid_bins, LOG_EFF_FRONT, 'ro-',label="FRONT")
    plt.plot(energy_mid_bins, LOG_EFF_BACK, 'bo-' ,label="BACK")
    plt.plot(energy_mid_bins, LOG_EFF, 'ko-' ,label="TOTAL")
    plt.legend()
    plt.title('%s eff area (THETA_LAT %d deg, PHI_LAT %d deg)'%(settings.IRF_NAME, FIX_THETA_LAT, FIX_PHI_LAT))
    plt.xlabel('E (GeV)')
    plt.xscale('log')
    plt.ylabel('Effective area ($m^2$)')
    plt.savefig('eff_energy_dist.png')
    # plt.show()

if __name__ == "__main__":
    main()