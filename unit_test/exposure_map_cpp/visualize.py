import pandas as pd
import numpy as np
import math
import os
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from utility import transform
import settings

WEEK = 164
path = os.path.join(
    os.getcwd(),
    os.path.join(
        "unit_test",
        "exposure_map_cpp"
    )
)

def main():
    df = pd.read_csv(
        os.path.join(path, "livemap_w{0:02d}.csv".format(WEEK)),
        header=None
    )
    exp_map = df.to_numpy()[:,0].reshape(settings.N_BINS_PHI_NADIR, settings.N_BINS_THETA_NADIR)
    print(exp_map)
    plt.figure()
    x, y = np.mgrid[
        slice(settings.PHI_NADIR_MIN, settings.PHI_NADIR_MAX + settings.D_PHI, settings.D_PHI),
        slice(settings.THETA_NADIR_MIN, settings.THETA_NADIR_MAX + settings.D_THETA, settings.D_THETA),
    ]
    plt.pcolormesh(x, y, exp_map, cmap="viridis", norm=matplotlib.colors.LogNorm())
    a = plt.colorbar()
    a.set_label('Livetime (s)')
    plt.title("Live map (week:{})".format(WEEK))
    # plt.title("Live map (one row of week:{}, rock:{:.02f})".format(WEEK, row['ROCK_ANGLE']))
    plt.xlabel("$\phi_{nadir}$ (deg)")
    plt.ylabel("$\\theta_{nadir}$ (deg)")
    plt.show()