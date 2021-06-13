import math
import os
import random

import numpy as np
from scipy.interpolate import CubicSpline


def get_cnts_by_sys_error(
    flx_hist,
    exp_vals
):
    np.random.seed(random.randint(0, 42))
    assert len(flx_hist) == len(exp_vals)
    return [
        np.random.poisson(int(flx * exp))
        for flx, exp in zip(flx_hist, exp_vals)
    ]


def get_cnts_by_total_error(
    flx_hist,
    exp_vals,
    energy_bins
):
    assert len(flx_hist) == len(exp_vals)
    assert len(flx_hist) == len(energy_bins)
    np.random.seed(random.randint(0, 42))

    cs = get_cubic_spline()

    new_cnt_hist = []
    for i in range(len(energy_bins)):
        err = cs(energy_bins[i]).tolist()
        distorted_flx_val = flx_hist[i] * (1 + err)
        new_count_val = int(distorted_flx_val*exp_vals[i])
        new_count_val = np.random.poisson(new_count_val)
        new_cnt_hist.append(new_count_val)
    return new_cnt_hist


def get_cubic_spline():
    def _get_rand_sys_err(energy_gev):
        _magnitude = get_magnitude_sys_err(energy_gev)
        return np.random.uniform(-_magnitude, _magnitude)

    energies = [10.0, 100.0, 1000.0]
    sys_errs = [_get_rand_sys_err(energy) for energy in energies]
    return CubicSpline(energies, sys_errs)


def get_magnitude_sys_err(energy_gev):
    energy_mev = 1000.0 * energy_gev
    if energy_mev < 100:  # 5% + 20% x (2.0-log(E/MeV))
        err = 0.05 * 0.2 * (2.0 - math.log10(energy_mev))
    elif energy_mev > 10000:
        err = 0.05 + 0.1 * (math.log10(energy_mev) - 5.0)
    else:
        err = 0.05
    return err
