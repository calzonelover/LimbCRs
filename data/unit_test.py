# import pyIrfLoader
# import ROOT as rt
import numpy as np
import math
import pyfits
import os

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
    phi_ps = []
    theta_ps = []

    f = pyfits.open(os.path.join(path, "lat_spacecraft_weekly_w{0:3d}_p202_v001.fits").format(WEEK))
    rows = f[1].data
    for row in rows:
        if abs(row['ROCK_ANGLE']) > 170:
            t_eq_sp = transform.get_T_eq_sp(transform.d2r(row['DEC_ZENITH']), transform.d2r(row['RA_ZENITH']))
            inv_t_eq_sp = np.linalg.inv(t_eq_sp)
            t_eq_p = transform.get_T_eq_p(
                transform.d2r(row['DEC_SCX']),
                transform.d2r(row['RA_SCX']),
                transform.d2r(row['DEC_SCZ']),
                transform.d2r(row['RA_SCZ'])
            )     
            exp_map = np.zeros(shape=(settings.N_BINS_PHI_NADIR, settings.N_BINS_THETA_NADIR), dtype=float)
            for i_phi_nadir in range(settings.N_BINS_PHI_NADIR):
                for i_theta_nadir in range(settings.N_BINS_THETA_NADIR):
                    phi_nadir = settings.D_PHI * i_phi_nadir
                    theta_nadir = settings.D_THETA * i_theta_nadir
                    r_sp = np.array([
                        -math.cos(theta_nadir),
                        math.sin(theta_nadir)*math.cos(phi_nadir),
                        math.sin(theta_nadir)*math.sin(phi_nadir)
                    ])
                    r_p = np.matmul(
                        np.matmul(
                            t_eq_p,
                            inv_t_eq_sp
                        ),
                        r_sp
                    )
                    rho = math.sqrt(r_p[0]*r_p[0]+r_p[1]*r_p[1])
                    theta_p = math.pi/2 - math.atan(r_p[2]/rho)
                    phi_p = math.acos(r_p[0]/rho)
                    if transform.r2d(theta_p) < 70:
                        if transform.r2d(theta_p) < 0:
                            print("negative !!")
                            break
            break
            # print(
            #     row['ROCK_ANGLE'],
            #     row['LIVETIME'],
            #     row['RA_ZENITH'],
            #     row['DEC_ZENITH'],
            #     row['RA_SCZ'],
            #     row['DEC_SCZ'],
            #     row['RA_SCX'],
            #     row['DEC_SCX'],
            # )

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