import astropy.io.fits as pyfits
import pandas as pd
import sqlite3
import os

import settings

WEEK_BEGIN = 9
WEEK_END = 540

path_write = os.path.join(
    os.getcwd(),
    os.path.join(
        "data",
        "raw"
    )
)

path_read = os.path.join(
    os.getcwd(),
    os.path.join(
        "data",
        "raw"
    )
)

# path_read = "/work/bus/Data/Photon"

def mev_to_gev(e):
    return e/1000.0

def main():
    WEEK = WEEK_BEGIN
    while WEEK <= WEEK_END:
        print("WEEK {}".format(WEEK))
        f = pyfits.open(os.path.join(path_read, "lat_photon_weekly_w{0:03d}_p302_v001.fits".format(WEEK)))
        rows = f[1].data
        rows = list(filter(lambda x: 
            x['THETA'] < settings.THETA_LAT_CUTOFF
            and mev_to_gev(x['ENERGY']) >= settings.E_START_GEV
            and mev_to_gev(x['ENERGY']) <= settings.E_STOP_GEV
            and row['EVENT_CLASS'][?] == True # source
            , rows)
        )
        selected_rows = list(map(lambda row: {
            'TIME': row['TIME'],
            'THETA': row['THETA'],
            'THETA_NAD': 180.0 - row['ZENITH_ANGLE'],
            'PHI_NAD': row['EARTH_AZIMUTH_ANGLE'],
            'ENERGY_GEV': mev_to_gev(row['ENERGY']),
            'WEEK': WEEK,
            'EVENT_CLASS': ? if row['EVENT_CLASS'][?] == True else ?,
        }, rows))
        # conn = sqlite3.connect(os.path.join(path_write, "csv", "cut_photon_w{0:03d}-{1:03d}.sqlite".format(WEEK_BEGIN, WEEK_END)))
        # cursor = conn.cursor()
        df = pd.DataFrame(selected_rows)
        df.to_csv(os.path.join(path_write, "csv", "photon_w{0:03d}-{1:03d}.csv".format(WEEK_BEGIN, WEEK_END)))
        WEEK += 1
