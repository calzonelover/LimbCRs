import re
from operator import itemgetter
import os
import pandas as pd
from matplotlib import pyplot as plt


def plot_exp_map():
    STATIC_PATH = "effective_area/static_table"
    PHOTON_CLASS = "P8R2_ULTRACLEANVETO_V6"
    OUTPUT_PATH = "unit_test/visual_exp"

    path = os.path.join(STATIC_PATH, PHOTON_CLASS)
    files = os.listdir(path)

    # plot fix theta, vary energy
    THETAS = (10, 25, 40)
    data1 = {"x": []}
    fig, axs = plt.subplots(figsize=(8, 6))
    for f in files:
        energy_gev = int(re.findall(r"\d+", f)[0])
        data1["x"].append(energy_gev)
        df = pd.read_csv(os.path.join(path, f))
        for theta in THETAS:
            key = "theta%d_eff" % theta
            eff_m2 = df.iloc[theta]["eff_m2"]
            try:
                data1[key].append(eff_m2)
            except KeyError:
                data1[key] = [eff_m2, ]
    sorted_energy_indices = sorted((i, e) for i, e in enumerate(data1["x"]))
    sorted_energy_indices = sorted(sorted_energy_indices, key=itemgetter(1))
    x = []
    y = {}
    for i, e in sorted_energy_indices:
        x.append(e)
        for theta in THETAS:
            key = "theta%d_eff" % theta
            try:
                y[key].append(data1[key][i])
            except KeyError:
                y[key] = [data1[key][i], ]
    for i, theta in enumerate(THETAS):
        key = "theta%d_eff" % theta
        axs.plot(
            x, y[key],
            "o-",
            label="$\Theta$ = %d$^\circ$" % theta
        )
    plt.xscale("log")
    plt.title(
        "%s (total) effective area, averaged over $\phi$"
        % PHOTON_CLASS
    )
    plt.ylabel(r"Effective area (m$^2$)")
    plt.xlabel("Energy (GeV)")
    plt.legend()
    plt.savefig(os.path.join(OUTPUT_PATH, "custom_eff_energy.png"))
    # plt.show()

    plt.cla()
    plt.clf()

    # plot fix energy vary theta
    ENERGYS = (79, 218, 792)
    data = {}
    for energy in ENERGYS:
        data[energy] = {}
        f_path = os.path.join(path, "eff_E%d.csv" % energy)
        df = pd.read_csv(f_path)
        data[energy]["x"] = df["theta_lat"].tolist()
        data[energy]["y"] = df["eff_m2"].tolist()

    fig, axs = plt.subplots(figsize=(8, 6))
    for i, energy in enumerate(ENERGYS):
        axs.plot(
            data[energy]["x"],
            data[energy]["y"],
            "o-",
            label="%d GeV" % energy
        )
    plt.title(
        "%s (total) effective area, averaged over $\phi$"
        % PHOTON_CLASS
    )
    plt.ylabel(r"Effective area (m$^2$)")
    plt.xlabel(r"$\Theta$ (deg)")
    plt.legend()
    # plt.show()
    plt.savefig(os.path.join(OUTPUT_PATH, "custom_eff_theta.png"))
