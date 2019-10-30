# import pyfits
import astropy.io.fits as pyfits
import pandas as pd
import os

WEEK_BEGIN = 9
WEEK_END = 550

path_write = os.path.join(
    os.getcwd(),
    os.path.join(
        "data",
        "raw"
    )
)

path_read = "/work/bus/Data/Spacecraft"


def main():
    WEEK = WEEK_BEGIN
    while WEEK <= WEEK_END:
        print("WEEK {}".format(WEEK))
        f = pyfits.open(os.path.join(path_read, "lat_spacecraft_weekly_w{0:03d}_p202_v001.fits".format(WEEK)))
        rows = f[1].data
        selected_rows = list(map(lambda row: {
            'START': row['START'],
            'STOP': row['STOP'],
            'ROCK_ANGLE': row['ROCK_ANGLE'],
            'DEC_ZENITH': row['DEC_ZENITH'],
            'RA_ZENITH': row['RA_ZENITH'],
            'DEC_SCX': row['DEC_SCX'],
            'RA_SCX': row['RA_SCX'],
            'DEC_SCZ': row['DEC_SCZ'],
            'RA_SCZ': row['RA_SCZ'],
            'LIVETIME': row['LIVETIME'],
        }, rows))
        df = pd.DataFrame(selected_rows)
        df.to_csv(os.path.join(path_write, "csv","ft2_w{0:03d}.csv".format(WEEK)))
        WEEK += 1

if __name__ == "__main__":
    main()