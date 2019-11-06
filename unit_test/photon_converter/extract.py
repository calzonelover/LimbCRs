import ROOT as rt
import numpy as np
import math
import astropy.io.fits as pyfits
import os

import settings

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
    ft1_out = rt.TFile(os.path.join('data', 'raw', 'extracted_photon.root'),'RECREATE')
    t1 = rt.TTree(
        'photon_w%03d_%03d_E%d_%d'%(
            settings.WEEK_BEGIN, settings.WEEK_END,
            settings.E_START_GEV, settings.E_STOP_GEV
        )
        ,'Data events'
    )

    # Init value to assign in branch
    TIME = np.zeros(1,dtype=float)
    ENERGY_GEV = np.zeros(1, dtype=float)
    ZENITH = np.zeros(1, dtype=float)
    ZENITHSHIFT = np.zeros(1, dtype=float)
    NADIR = np.zeros(1, dtype=float)
    NADIRSHIFT = np.zeros(1, dtype=float)
    THETA = np.zeros(1, dtype=float)
    PHI = np.zeros(1, dtype=float)
    ALTITUDE_KM = np.zeros(1,dtype=float)
    PHI_EARTH = np.zeros(1,dtype=float)
    ROCK = np.zeros(1,dtype=float)

    # create the branch of our tre
    t1.Branch('TIME',TIME,'TIME/D')
    t1.Branch('ENERGY_GEV',ENERGY_GEV,'ENERGY_GEV/D')
    t1.Branch('ZENITH',ZENITH,'ZENITH/D')
    t1.Branch('ZENITHSHIFT',ZENITHSHIFT,'ZENITHSHIFT/D')
    t1.Branch('NADIR',NADIR,'NADIR/D')
    t1.Branch('NADIRSHIFT',NADIRSHIFT,'NADIRSHIFT/D')
    t1.Branch('THETA',THETA,'THETA/D')
    t1.Branch('PHI',PHI,'PHI/D')
    t1.Branch('ALTITUDE_KM',ALTITUDE_KM,'ALTITUDE_KM/D')
    t1.Branch('PHI_EARTH',PHI_EARTH,'PHI_EARTH/D')
    t1.Branch('ROCK',ROCK,'ROCK/D')

    ft1_files = [os.path.join(RAW_PATH, 'Photon', 'lat_photon_weekly_w%03d_p302_v001.fits'%i) for i in range(settings.WEEK_BEGIN, settings.WEEK_END+1)]
    ft2_files = [os.path.join(RAW_PATH, 'Spacecraft', 'lat_spacecraft_weekly_w%03d_p202_v001.fits'%i) for i in range(settings.WEEK_BEGIN, settings.WEEK_END+1)]
    for ft1_file, ft2_file in zip(ft1_files, ft2_files):
        print(ft1_file)
        ft1 = pyfits.open(ft1_file)
        photons = ft1[1].data
        ft2 = pyfits.open(ft2_file)
        sps = ft2[1].data
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
                TIME[0] = photon['TIME']
                ENERGY_GEV[0] = energy_gev
                ZENITH[0] = photon['ZENITH_ANGLE']
                ZENITHSHIFT[0] = zenith_shift
                NADIR[0] = nadir
                NADIRSHIFT[0] = nadir_shift
                THETA[0] = photon['THETA']
                PHI[0] = photon['PHI']
                ALTITUDE_KM[0] = sp['RAD_GEO']/1000.0
                PHI_EARTH[0] = photon['EARTH_AZIMUTH_ANGLE']
                ROCK[0] = sp['ROCK_ANGLE']
                t1.Fill()
    ft1_out.Write()
    ft1_out.Close()