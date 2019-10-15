import pyfits
import pandas as pd

WEEK = 164

def main():
    f = pyfits.open("lat_spacecraft_weekly_w{0:3d}_p202_v001.fits".format(WEEK))
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
    df.to_csv("ft2_w{0:3d}.csv".format(WEEK))

if __name__ == "__main__":
    main()