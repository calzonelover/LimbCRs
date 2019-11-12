from mpi4py import MPI
import numpy as np
import pandas as pd
import math
import astropy.io.fits as pyfits
import os

import settings, utility

RAW_PATH = '/work/bus/Data'

def zenith_to_nadir(zenith_angle):
    return 180.0 - zenith_angle

def mev_to_gev(e):
    return e/1000.0

def get_shifted_zenith(zenith, altitude_m):
    altitude_km = altitude_m/1000.0
    return zenith + 0.0211*(550.0-altitude_km)

def get_sp(sps, photon_time):
    i_sp = np.searchsorted(sps[:,]['START'], photon_time) - 1
    return sps[i_sp]

def main():
    comm = MPI.COMM_WORLD
    size = comm.Get_size()
    rank = comm.Get_rank()
    status = MPI.Status()

    if rank == 0:
        print("Total # of process {}".format(size))
    print("Initialize process # {}".format(rank))

    if rank == 0:
        weeksent = settings.WEEK_BEGIN
        # first send
        for i_dest in range(1, size):
            if weeksent <= settings.WEEK_END:
                comm.send(weeksent, dest=i_dest, tag=settings.TAG_INPROGRESS)
                weeksent += 1
        # loop later
        for week_i in range(settings.WEEK_BEGIN, settings.WEEK_END+1):
            slave_i = comm.recv(source=MPI.ANY_SOURCE, tag=MPI.ANY_TAG, status=status)
            if weeksent <= settings.WEEK_END:
                comm.send(weeksent, dest=slave_i, tag=settings.TAG_INPROGRESS)
                weeksent += 1
            else:
                comm.send(weeksent, dest=slave_i, tag=settings.TAG_DONE)
    else:
        while True:
            week_i = comm.recv(source=0, tag=MPI.ANY_TAG, status=status)
            if status.tag == settings.TAG_DONE:
                break
            # process FT1 and FT2 file to write photon weekly
            ft1_file = os.path.join(settings.PATH_RAW_DATA, 'Photon', 'lat_photon_weekly_w%03d_p302_v001.fits'%week_i)
            ft2_file = os.path.join(settings.PATH_RAW_DATA, 'Spacecraft', 'lat_spacecraft_weekly_w%03d_p202_v001.fits'%week_i)
            ft1 = pyfits.open(ft1_file)
            photons = ft1[1].data
            ft2 = pyfits.open(ft2_file)
            sps = ft2[1].data

            extracted_photons = []
            for photon in photons:
                sp = get_sp(sps, photon['TIME'])
                energy_gev = mev_to_gev(photon['ENERGY'])
                nadir = zenith_to_nadir(photon['ZENITH_ANGLE'])
                zenith_shift = get_shifted_zenith(photon['ZENITH_ANGLE'], sp['RAD_GEO'])
                nadir_shift = zenith_to_nadir(zenith_shift)
                if (
                    energy_gev > settings.E_START_GEV and energy_gev < settings.E_STOP_GEV
                    and ( nadir < settings.THETA_NADIR_MAX or nadir_shift < settings.THETA_NADIR_MAX )
                    and photon['THETA'] < settings.THETA_LAT_CUTOFF
                ):
                    extracted_photons.append({
                        'time': photon['TIME'],
                        'energy_gev': energy_gev,
                        'zenith': photon['ZENITH_ANGLE'],
                        'shifted_zenith': zenith_shift,
                        'nadir': nadir,
                        'shifted_nadir': nadir_shift,
                        'theta_lat': photon['THETA'],
                        'phi_lat': photon['PHI'],
                        'altitude_km': sp['RAD_GEO']/1000.0,
                        'phi_earth': photon['EARTH_AZIMUTH_ANGLE'],
                        'rocking_angle': sp['ROCK_ANGLE'],
                    })
            df = pd.DataFrame(extracted_photons)
            df.to_csv(os.path.join(settings.PATH_EXTRACTED_DATA, 'photon', 'ft1_w%03d'%week_i))
            print('Finished week {} from slave {}'.format(week_i, rank))
            comm.send(rank, dest=0, tag=settings.TAG_INPROGRESS)