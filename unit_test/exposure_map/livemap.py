# import pyIrfLoader
# import ROOT as rt
import numpy as np
import math
import pyfits
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
        "data",
        "static"
    )
)

def main():
    exp_map = np.zeros(shape=(settings.N_BINS_PHI_NADIR, settings.N_BINS_THETA_NADIR), dtype=float)
    f = pyfits.open(os.path.join(path, "lat_spacecraft_weekly_w{0:3d}_p202_v001.fits").format(WEEK))
    rows = f[1].data
    for i, row in enumerate(rows):
        print("{}/{} ROCK:{} T_START: {}, T_STOP: {}".format(i+1, len(rows), row['ROCK_ANGLE'],row['START'], row['STOP']))
        t_eq_sp = transform.get_T_eq_sp(transform.d2r(row['DEC_ZENITH']), transform.d2r(row['RA_ZENITH']))
        inv_t_eq_sp = np.linalg.inv(t_eq_sp)
        t_eq_p = transform.get_T_eq_p(
            transform.d2r(row['DEC_SCX']),
            transform.d2r(row['RA_SCX']),
            transform.d2r(row['DEC_SCZ']),
            transform.d2r(row['RA_SCZ'])
        )
        for i_phi_nadir in range(settings.N_BINS_PHI_NADIR):
            for i_theta_nadir in range(settings.N_BINS_THETA_NADIR):
                phi_nadir = transform.d2r(settings.D_PHI * i_phi_nadir)
                theta_nadir = transform.d2r(settings.D_THETA * i_theta_nadir)
                r_sp = np.array([
                    -math.cos(theta_nadir),
                    math.sin(theta_nadir)*math.sin(phi_nadir),
                    math.sin(theta_nadir)*math.cos(phi_nadir)
                ])
                r_p = np.matmul(
                    t_eq_p,
                    np.matmul(
                        inv_t_eq_sp,
                        r_sp
                    )
                )
                rho = math.sqrt(r_p[0]*r_p[0]+r_p[1]*r_p[1])
                theta_p = math.pi/2 - math.atan(r_p[2]/rho)
                phi_p = math.acos(r_p[0]/rho) if r_p[1] < 0 else 2*math.pi - math.acos(r_p[0]/rho)
                if transform.r2d(theta_p) < settings.THETA_LAT_CUTOFF:
                    exp_map[i_phi_nadir, i_theta_nadir] += row['LIVETIME']
    # cartesian plot
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
    plt.savefig("livemap.png")
    # plt.show()
    # polar plot
    plt.clf()
    ax = plt.subplot(projection='polar')
    ax.set_theta_zero_location("N")  # theta=0 at the top
    ax.set_theta_direction(-1)  # theta increasing clockwise
    plt.pcolormesh(transform.d2r(x), y, exp_map, cmap="viridis", norm=matplotlib.colors.LogNorm())
    # plt.thetagrids([theta * 15 for theta in range(int(settings.PHI_NADIR_MAX)//15)])
    plt.rgrids([theta * 30 for theta in range(int(settings.THETA_NADIR_MAX)//30)])
    plt.grid(alpha=0.5, linestyle='--')
    a = plt.colorbar()
    a.set_label('Livetime (s)')
    plt.title("Live map (week:{})".format(WEEK))
    # plt.title("Live map (one row of week:{}, rock:{:.02f})".format(WEEK, row['ROCK_ANGLE']))
    plt.savefig("livemap_polar.png")
    # plt.show()
    # ref https://stackoverflow.com/questions/36513312/polar-heatmaps-in-python

def find_lat_looking():
    path = os.path.join(
        os.getcwd(),
        os.path.join(
            "data",
            "static"
        )
    )
    for f in os.scandir(path):
        if f.is_file() and f.name.endswith('.fits'):
            f_dat = pyfits.open(os.path.join(path, f))
            rows = f_dat[1].data
            for row in rows:
                if abs(row['ROCK_ANGLE']) > 170:
                    print(f, row['ROCK_ANGLE'])