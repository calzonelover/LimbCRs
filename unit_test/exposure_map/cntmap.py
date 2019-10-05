import numpy as np
import math
import pyfits
import os
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from utility import transform
import settings

WEEK = 164

## ROCK -100.27
ROCK_ANGLE = -100.27
T_START = 332916755.6
T_END = 332916785.6
## ROCK 50.00395
# ROCK_ANGLE = 50.00395
# T_START = 332902412.6
# T_END = 332902442.6
## ROCK 171
# ROCK_ANGLE = 175.71
# T_START = 333352615.6
# T_END = 333352645.6

path = os.path.join(
    os.getcwd(),
    os.path.join(
        "data",
        "static"
    )
)

def main():
    phi_ps = []
    theta_ps = []

    f = pyfits.open(os.path.join(path, "lat_photon_weekly_w{0:3d}_p302_v001.fits").format(WEEK))
    rows = f[1].data

    rows = list(filter(lambda x: x['THETA'] < settings.THETA_LAT_CUTOFF, rows))
    interested_photon_theta_nads = list(map(lambda  x: 180.0 - x['ZENITH_ANGLE'], rows))
    interested_photon_phi_nads = list(map(lambda  x: x['EARTH_AZIMUTH_ANGLE'], rows))
    # interested_photon_theta_nads = []
    # interested_photon_phi_nads = []
    # for row in rows:
    #     if row['TIME'] > T_START and row['TIME'] < T_END:
    #         if row['THETA'] < settings.THETA_LAT_CUTOFF:
    #             interested_photon_theta_nads.append(180.0 - row['ZENITH_ANGLE'])
    #             interested_photon_phi_nads.append(row['EARTH_AZIMUTH_ANGLE'])
    # visualize
    np_cntmap, _, _ = np.histogram2d(
        interested_photon_phi_nads,
        interested_photon_theta_nads,
        bins=(settings.N_BINS_PHI_NADIR, settings.N_BINS_THETA_NADIR),
        range=([settings.PHI_NADIR_MIN, settings.PHI_NADIR_MAX], [settings.THETA_NADIR_MIN, settings.THETA_NADIR_MAX]),        
    )
    # phi_nad_hist = np.histogram(
    #     interested_photon_phi_nads,
    #     bins=settings.N_BINS_PHI_NADIR,
    #     range=(settings.PHI_NADIR_MIN, settings.PHI_NADIR_MAX),
    # )
    x, y = np.mgrid[
        slice(settings.PHI_NADIR_MIN, settings.PHI_NADIR_MAX + settings.D_PHI, settings.D_PHI),
        slice(settings.THETA_NADIR_MIN, settings.THETA_NADIR_MAX + settings.D_THETA, settings.D_THETA),
    ] 
    # 1D hist
    plt.hist(
        interested_photon_phi_nads,
        bins=int(settings.N_BINS_PHI_NADIR),
        range=(settings.PHI_NADIR_MIN, settings.PHI_NADIR_MAX)
    )
    plt.title("Distribution of PHI_NAD (one row of week:{}, rock:{:.02f})".format(WEEK, ROCK_ANGLE))
    plt.xlabel("$\phi_{nadir}$ (deg)")
    plt.ylabel("Count")
    plt.show()
    # cartesian  
    plt.clf()  
    plt.pcolormesh(x, y, np_cntmap, cmap="cividis")
    plt.title("Count map (one row of week:{}, rock:{:.02f})".format(WEEK, ROCK_ANGLE))
    plt.xlabel("$\phi_{nadir}$ (deg)")
    plt.ylabel("$\\theta_{nadir}$ (deg)")
    a = plt.colorbar()
    a.set_label('Count')
    plt.show()
    # polar
    plt.clf()
    ax = plt.subplot(projection='polar')
    ax.set_theta_zero_location("N")  # theta=0 at the top
    ax.set_theta_direction(-1)  # theta increasing clockwise
    plt.pcolormesh(transform.d2r(x), y, np_cntmap, cmap="cividis")
    # plt.thetagrids([theta * 15 for theta in range(int(settings.PHI_NADIR_MAX)//15)])
    plt.rgrids([theta * 30 for theta in range(int(settings.THETA_NADIR_MAX)//30)])
    plt.grid(alpha=0.5, linestyle='--')
    a = plt.colorbar()
    a.set_label('Count')
    plt.title("Count map (one row of week:{}, rock:{:.02f})".format(WEEK, ROCK_ANGLE))
    plt.show()