import pyLikelihood
import pyIrfLoader
import os
import math
import numpy as np
import pyfits
import matplotlib.pyplot as plt

import settings

PHI_LATs = [45.0*i for i in range(8)]
PATH_SAVE_EFF = os.path.join(
    os.getcwd(),
    "effective_area",
    "static_table",
    settings.IRF_NAME
)

CM2_TO_M2 = 10000.0
GEV_TO_MEV = 1000.0

# LOG_EFF_FRONT = []
# LOG_EFF_BACK = []
# LOG_EFF = []

'''

This script has been design for only python2.7

'''

def getEnergyMidBins():
    energy_edge_bins = [
        settings.E_START_GEV * math.pow(settings.E_STOP_GEV/settings.E_START_GEV, float(i)/float(settings.N_E_BINS))
        for i in range(settings.N_E_BINS+1)
    ]
    _energy_mid_bins = []
    for i in range(settings.N_E_BINS):
        divider = 1.0 - float(settings.GAMMA)
        e2d = math.pow(energy_edge_bins[i+1], divider)
        e1d = math.pow(energy_edge_bins[i], divider)
        ln = math.log(0.5*(e2d - e1d)+ e1d)
        _energy_mid_bins.append(math.exp(ln/(divider)))
    return _energy_mid_bins

def main():
    phi_lats = [i*45.0 for i in range(8)]
    theta_lats = [i for i in range(int(settings.THETA_LAT_CUTOFF)+1)]
    energy_mid_bins = getEnergyMidBins()

    pyIrfLoader.Loader_go()
    myFactory = pyIrfLoader.IrfsFactory_instance()
    irfs_f = myFactory.create("%s::FRONT"%settings.IRF_NAME)
    irfs_b = myFactory.create("%s::BACK"%settings.IRF_NAME)
    aeff_f = irfs_f.aeff()
    aeff_b = irfs_b.aeff()
    for energy_mid_bin in energy_mid_bins:
        f_eff = open(
            os.path.join(PATH_SAVE_EFF, "eff_E%d.csv"%(int(math.floor(energy_mid_bin))))
            , "w"
        )
        f_eff.write("theta_lat,eff_m2\n")
        for theta_lat in theta_lats:
            for phi_lat in phi_lats:
                eff = []
                eff_front = aeff_f.value(GEV_TO_MEV*energy_mid_bin, theta_lat, phi_lat)/CM2_TO_M2
                eff_back = aeff_b.value(GEV_TO_MEV*energy_mid_bin, theta_lat, phi_lat)/CM2_TO_M2
                eff.append(eff_front + eff_back)
            mean_eff = sum(eff)/len(eff)
            f_eff.write("%f,%f\n"%(theta_lat, mean_eff))
        f_eff.close()

if __name__ == "__main__":
    main()