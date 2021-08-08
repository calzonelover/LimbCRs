from contextlib import closing
import os
import re
from functools import wraps

import multiprocessing as mp
import numpy as np
import ROOT as rt
from scipy.optimize import basinhopping, fmin, minimize, rosen, rosen_der, rosen_hess

from model import Model
import settings
from .disturb import get_cnts_by_sys_error, get_cnts_by_total_error


ATTRS = ("obj_loss", "norm_all", "norm", "gamma1", "gamma2", "e_break")


def main():
    model_names = ("SPLwHe", "BPLwHe")
    initialguesspars = (
        [0.0108668, 2.82851, 2.70266, 2.6, 342.0],
        [0.0108818, 1.98848, 2.86015, 2.63161, 333.115]
    )
    # run(
    #     model_names=model_names, n_trial=2,
    #     disturb_mode="sys", initialguesspars=initialguesspars
    # )
    print("Run sys.")
    run(
        model_names=model_names, n_trial=2000,
        disturb_mode="sys", initialguesspars=initialguesspars
    )
    print("Run tot.")
    run(
        model_names=model_names, n_trial=2000,
        disturb_mode="tot", initialguesspars=initialguesspars
    )


def run(model_names, n_trial, disturb_mode, initialguesspars):
    extracted_result = fetch_extracted_result()

    f = open('%s_%s_result.csv' % ("-".join(model_names), disturb_mode), 'w')

    attrs = ",".join([
        "%s_%s" % (model_name, attr) for model_name in model_names
        for attr in ATTRS
    ]) + "\n"
    f.write(attrs)

    with closing(mp.Pool(processes=mp.cpu_count())) as workers:
        results = workers.map(
            get_simulated_fitted_result,
            [
                (
                    extracted_result, model_names,
                    disturb_mode, initialguesspars
                )
                for i in range(n_trial)
            ]
        )
    for result in results:
        row_str = []
        for model_result in result:
            fopt, xopt = model_result
            row_str.append(
                "%f,%f,%f,%f,%f,%f"
                % (fopt, xopt[0], xopt[1], xopt[2], xopt[3], xopt[4])
            )
        f.write(",".join(row_str) + "\n")

    f.close()


def unpack(func):
    @ wraps(func)
    def wrapper(arg_tuple):
        return func(*arg_tuple)
    return wrapper


@unpack
def get_simulated_fitted_result(_extracted_result, _model_names, _disturb_mode, _initialguesspars):
    new_extracted_result = _extracted_result.copy()
    new_extracted_result["cnt_hist"] = get_disturbed_flux(
        _extracted_result, _disturb_mode
    )

    outputs = []
    for _model_name, _initialguesspar in zip(_model_names, _initialguesspars):
        _model = Model(_model_name)
        _model.assign_disturbed_result(new_extracted_result)
        xopt, fopt, iter, funcalls, warnflag = fmin(
            _model.sum_log_pois, _initialguesspar,
            full_output=True, ftol=0.01,  # maxiter=40
            disp=False
        )
        outputs.append((fopt, xopt.tolist()))
    return outputs


def get_disturbed_flux(_extracted_result, _disturb_mode):
    if _disturb_mode == "sys":
        return get_cnts_by_sys_error(
            flx_hist=_extracted_result["flx_hist"],
            exp_vals=_extracted_result["exp_vals"]
        )
    elif _disturb_mode == "tot":
        return get_cnts_by_total_error(
            flx_hist=_extracted_result["flx_hist"],
            exp_vals=_extracted_result["exp_vals"],
            energy_bins=_extracted_result["energy_bins"]
        )
    else:
        raise KeyError("Unsupported disturb mode %s" % _disturb_mode)


def fetch_extracted_result():
    def _get_bin_energy_from_titile(title):
        return re.findall("\d+\.\d+", title)[0]

    path_extracted_file = os.path.join('data', 'root', 'extracted_data.root')
    latest_summary_data = rt.TFile.Open(path_extracted_file, 'READ')

    cnt_hist = []
    flx_hist = []
    exp_vals = []
    energy_bins = []
    for bin_i in range(settings.N_E_BINS):
        count_th1f = latest_summary_data.Get("count_hist")
        flux_th1f = latest_summary_data.Get("flux_hist")
        exp_map = latest_summary_data.Get("expmap%03d" % bin_i)

        cnt_val = count_th1f.GetBinContent(bin_i+1)
        flx_val = flux_th1f.GetBinContent(bin_i+1)
        exp_val = cnt_val / flx_val
        # exp_val = sum_over_region(
        #     exp_map,
        #     settings.PHI_NADIR_MIN, settings.PHI_NADIR_MAX,
        #     settings.THETA_NADIR_CUT_MIN, settings.THETA_NADIR_CUT_MAX
        # )
        energy_bin = _get_bin_energy_from_titile(exp_map.GetTitle())

        cnt_hist.append(cnt_val)
        flx_hist.append(flx_val)
        exp_vals.append(exp_val)
        energy_bins.append(energy_bin)

    return {
        "cnt_hist": cnt_hist,
        "flx_hist": flx_hist,
        "exp_vals": exp_vals,
        "energy_bins": energy_bins
    }


def sum_over_region(map, phi_min, phi_max, theta_min, theta_max):
    i_min = map.GetXaxis().FindBin(phi_min)
    i_max = map.GetXaxis().FindBin(phi_max)
    j_min = map.GetYaxis().FindBin(theta_min)
    j_max = map.GetYaxis().FindBin(theta_max)
    return map.Integral(i_min, i_max, j_min, j_max)
