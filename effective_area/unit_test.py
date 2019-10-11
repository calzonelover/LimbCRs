import pyLikelihood
import pyIrfLoader
import os
import math
import numpy as np
import pyfits

import matplotlib.pyplot as plt

IRF_NAME = "P8R2_SOURCE_V6"
N_BINS_THETA_NADIR = int(1600/16)
THETA_NADIR_MIN, THETA_NADIR_MAX = 0.0, 160.0
D_THETA = (THETA_NADIR_MAX - THETA_NADIR_MIN)/N_BINS_THETA_NADIR


FIX_E = 1e3 # (1 GeV) 100 Mev -> 100 GeV
FIX_PHI_LAT = 0.0
PATH_SAVE_EFF = os.path.join(
    os.getcwd(),
    "eff_log"
)

LOG_EFF_FRONT = []
LOG_EFF_BACK = []
LOG_EFF = []

'''

This script has been design for only python2.7

'''

def main():
    theta_lats = [i for i in range(90)]

    pyIrfLoader.Loader_go()
    myFactory = pyIrfLoader.IrfsFactory_instance()
    irfs_f = myFactory.create("%s::FRONT"%IRF_NAME)
    irfs_b = myFactory.create("%s::BACK"%IRF_NAME)
    aeff_f = irfs_f.aeff()
    aeff_b = irfs_b.aeff()

    f_eff = open("eff_E%d_PHI%d.csv"%(FIX_E, FIX_PHI_LAT), "w")
    f_eff.write("theta_lat,eff_m2\n")
    for theta_lat in theta_lats:
        eff_front = aeff_f.value(FIX_E, theta_lat, FIX_PHI_LAT)/10000.0
        eff_back = aeff_b.value(FIX_E, theta_lat, FIX_PHI_LAT)/10000.0
        eff = eff_front + eff_back
        LOG_EFF_FRONT.append(eff_front)
        LOG_EFF_BACK.append(eff_back)
        LOG_EFF.append(eff)
        f_eff.write("%f,%f\n"%(theta_lat, eff))
    f_eff.close()
    plt.plot(LOG_EFF_FRONT, 'ro-',label="FRONT")
    plt.plot(LOG_EFF_BACK, 'bo-' ,label="BACK")
    plt.plot(LOG_EFF, 'ko-' ,label="TOTAL")
    plt.legend()
    plt.title('%s eff area E %d GeV PHI_LAT %d'%(IRF_NAME, FIX_E/1000, FIX_PHI_LAT))
    plt.xlabel('$\\theta_{LAT}$')
    plt.ylabel('Effective area ($m^2$)')
    plt.savefig('eff_theta_nadir_dist.png')
    # plt.show()

if __name__ == "__main__":
    main()