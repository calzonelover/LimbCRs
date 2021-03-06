import pandas as pd
import numpy as np
import math
import os
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from utility import transform
import settings

E = 953
path = os.path.join(
    os.getcwd(),
    os.path.join(
        "unit_test",
        "exposure_map_cpp"
    )
)

def main():
    df = pd.read_csv(
        os.path.join(path, "../../data/exposure_map/w{}_{}/{}/expmap_E{}.csv".format(settings.WEEK_BEGIN, settings.WEEK_END, settings.IRF_NAME, E)),
        header=None
    )
    exp_map = df.to_numpy()[:,0].reshape(settings.N_BINS_PHI_NADIR, settings.N_BINS_THETA_NADIR)
    # exit()
    plt.figure()
    x, y = np.mgrid[
        slice(settings.PHI_NADIR_MIN, settings.PHI_NADIR_MAX + settings.D_PHI, settings.D_PHI),
        slice(settings.THETA_NADIR_MIN, settings.THETA_NADIR_MAX + settings.D_THETA, settings.D_THETA),
    ]
    plt.pcolormesh(x, y, exp_map, cmap="jet", norm=matplotlib.colors.LogNorm())
    a = plt.colorbar()
    a.set_label('Exposure ($m^2\ s$)')
    plt.title("Exposure map (week:{}-{}, E:{} GeV, {})".format(settings.WEEK_BEGIN, settings.WEEK_END, E, settings.IRF_NAME))
    # plt.title("Live map (one row of week:{}, rock:{:.02f})".format(WEEK, row['ROCK_ANGLE']))
    plt.xlabel("$\phi_{nadir}$ (deg)")
    plt.ylabel("$\\theta_{nadir}$ (deg)")
    plt.tight_layout()
    plt.show()
    # polar plot
    plt.clf()
    ax = plt.subplot(projection='polar')
    ax.set_theta_zero_location("N")  # theta=0 at the top
    ax.set_theta_direction(-1)  # theta increasing clockwise
    plt.pcolormesh(transform.d2r(x), y, exp_map, cmap="jet", norm=matplotlib.colors.LogNorm())
    # plt.thetagrids([theta * 15 for theta in range(int(settings.PHI_NADIR_MAX)//15)])
    plt.rgrids([theta * 20 for theta in range(int(settings.THETA_NADIR_MAX)//20)])
    plt.grid(alpha=0.5, linestyle='--')
    a = plt.colorbar()
    a.set_label('Exposure ($m^2\ s$)')
    plt.title("Exposure map (week:{}-{}, E:{} GeV, {})".format(settings.WEEK_BEGIN, settings.WEEK_END, E, settings.IRF_NAME))
    plt.tight_layout()
    plt.show()