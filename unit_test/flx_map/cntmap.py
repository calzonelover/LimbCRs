import pandas as pd
import numpy as np
import math
import os
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from utility import transform
import settings

def main():
    phi_nadirs = []
    theta_nadirs = []

    for week in range(settings.WEEK_BEGIN, settings.WEEK_END+1):
        week_photon_df = pd.read_csv(os.path.join(settings.PATH_EXTRACTED_DATA, "photon", "ft1_w{0:3d}.csv").format(week))
        phi_nadirs.extend(week_photon_df['phi_earth'])
        theta_nadirs.extend(week_photon_df['nadir'])

    # visualize
    np_cntmap, _, _ = np.histogram2d(
        phi_nadirs,
        theta_nadirs,
        bins=(settings.N_BINS_PHI_NADIR, settings.N_BINS_THETA_NADIR),
        range=([settings.PHI_NADIR_MIN, settings.PHI_NADIR_MAX], [settings.THETA_NADIR_MIN, settings.THETA_NADIR_MAX]),        
    )
    