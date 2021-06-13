import os
import math
import subprocess
import uuid

import numpy as np
from scipy.interpolate import CubicSpline
import ROOT as rt


PATH = "model/tmp"


class Model:
    def __init__(self, name):
        self.name = name
        self.ticket = str(uuid.uuid4())
        self.path = os.path.join(PATH, self.ticket)
        self.create_dummy_folder()

        self.disturbed_result = None

    def assign_disturbed_result(self, disturbed_result):
        self.disturbed_result = disturbed_result

    def sum_log_pois(
        self,
        params
    ):
        norm_all, norm, gamma1, gamma2, e_break = params

        if self.disturbed_result is None:
            assert LookupError("Please assign data")
        energies, fluxs = self.get_forward_result(
            norm_all,
            norm,
            gamma1,
            gamma2,
            e_break
        )

        cs = CubicSpline(np.array(energies, dtype=float),
                         np.array(fluxs, dtype=float))

        sumlogpois = 0
        for observed_bin_i in range(len(self.disturbed_result["energy_bins"])):
            observed_energy = self.disturbed_result["energy_bins"][observed_bin_i]
            observed_cnt = self.disturbed_result["cnt_hist"][observed_bin_i]
            observed_exp_val = self.disturbed_result["exp_vals"][observed_bin_i]

            model_flux_val = cs(observed_energy).tolist()
            model_cnt_val = int(model_flux_val * observed_exp_val)

            if rt.TMath.Poisson(observed_cnt, model_cnt_val) in (0, np.nan, -np.nan):
                sumlogpois += 308.
            if rt.TMath.Poisson(observed_cnt, model_cnt_val) != 0:
                sumlogpois += - math.log10(
                    rt.TMath.Poisson(observed_cnt, model_cnt_val)
                )
        # print(sumlogpois, params)
        return sumlogpois

    def get_forward_result(
        self,
        norm_all,
        norm,
        gamma1,
        gamma2,
        e_break
    ):
        out_csv = "%s.csv" % self.name
        run_cmd(
            cmd=[
                "./model/%s.out" % self.name,
                out_csv,
                str(norm_all), str(norm), str(
                    gamma1), str(gamma2), str(e_break)
            ],
            running_path=self.path
        )

        f_output = os.path.join(self.path, "model", "simdata", out_csv)
        with open(f_output, "r") as f:
            rows = f.read().splitlines()
            energy_mid_bins, gamma_ray_fluxs = [], []
            for row in rows:
                record = row.strip().split()
                assert len(record) == 2
                energy_mid_bins.append(record[0])
                gamma_ray_fluxs.append(record[1])

        return energy_mid_bins, gamma_ray_fluxs

    def create_dummy_folder(self):
        os.makedirs(os.path.join(self.path, "model", "simdata"))
        run_cmd([
            "cp",
            "model/%s.f" % self.name, "model/gamfrag.dat", "model/frag.f",
            os.path.join(self.path, "model")
        ])
        run_cmd(
            cmd=["gfortran", "%s.f" % self.name,
                 "frag.f", "-o", "%s.out" % self.name],
            running_path=os.path.join(self.path, "model")
        )

    def delete_dummy_folder(self):
        run_cmd(["rm", "-rf", self.path])

    def __del__(self):
        self.delete_dummy_folder()


def run_cmd(cmd, running_path=None):
    params = {
        "stdout": subprocess.PIPE,
        "stderr": subprocess.PIPE,
    }
    if running_path:
        params["cwd"] = running_path
    process = subprocess.Popen(cmd, **params)
    process.wait()
    stdout, stderr = process.communicate()
    if process.returncode != 0:
        raise RuntimeError(stderr)
