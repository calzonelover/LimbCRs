import ROOT as rt
from astropy.io import fits

import datetime
import numpy as np
import math
import os
import re

import matplotlib
import matplotlib.pyplot as plt

from utility import transform
import settings


def main():
    CONSIDERED_E_MIN_GEV, CONSIDERED_E_MAX_GEV = 9.0, 1100.0

    REF_MST = datetime.datetime(2001, 1, 1, 0, 0, 0)
    BEGIN_SECOND_NEW_COUNT = (datetime.datetime(2008, 8, 21, 0, 0, 0) - REF_MST).total_seconds()
    END_SECOND_NEW_COUNT = (datetime.datetime(2013, 8, 8, 23, 59, 59) - REF_MST).total_seconds()
    raw_files = [os.path.join(settings.PATH_RAW_DATA, "Photon",'lat_photon_weekly_w%03d_p302_v001.fits'%(i))  for i in range(9,400)]
    ### test begin and end time
    # ft1 = fits.open(raw_files[0])
    # photon = ft1[1].data
    # time_i = datetime.datetime(2001, 1, 1) + datetime.timedelta(seconds=photon[0]['TIME'])
    # print(time_i)
    # ft1 = fits.open(raw_files[-1])
    # photon = ft1[1].data
    # time_l = datetime.datetime(2001, 1, 1) + datetime.timedelta(seconds=photon[-1]['TIME'])
    # print(time_l)
    # Aug 21, 2008 Aug 8, 2013


    '''
        Previous count (work)
    '''

    prev_cntmaps = rt.TFile.Open(os.path.join('data', 'static', 'from_Aj_Warit', 'CntMapP7SOURCEp202_LEO+ARR+50RcknewLATth70.root'),'READ')
    prev_cntmaps.cd()

    x_gap_bins = []
    counts = []

    for i, hist_obj in enumerate(prev_cntmaps.GetListOfKeys()):
        hist = hist_obj.ReadObj()
        min_max_energy_mev = re.findall(r"\d+[.]\d", hist.GetTitle())
        e_min_gev, e_max_gev = float(min_max_energy_mev[0])/1000.0, float(min_max_energy_mev[1])/1000.0
        if e_max_gev < CONSIDERED_E_MIN_GEV or e_min_gev > CONSIDERED_E_MAX_GEV: 
            continue
        # print(hist.ClassName(), hist.GetName(), hist.GetTitle())
        # print("E:", e_min_gev, e_max_gev)
        if i == 0: x_gap_bins.append(e_min_gev)
        x_gap_bins.append(e_max_gev)

        hist.Integral()
        n_bins_x = hist.GetNbinsX()
        n_bins_y = hist.GetNbinsY()
        min_phi_nad = hist.GetXaxis().GetBinLowEdge(1)
        max_phi_nad = hist.GetXaxis().GetBinLowEdge(n_bins_x) + hist.GetXaxis().GetBinWidth(n_bins_x)
        dphi = (max_phi_nad - min_phi_nad) / float(n_bins_x)
        # print(min_phi_nad, max_phi_nad, dphi)
        min_theta_nad = hist.GetYaxis().GetBinLowEdge(1)
        max_theta_nad = hist.GetYaxis().GetBinLowEdge(n_bins_y) + hist.GetYaxis().GetBinWidth(n_bins_y)
        dtheta = (max_theta_nad - min_theta_nad) / float(n_bins_y)
        # print(min_theta_nad, max_theta_nad, dtheta)

        min_bin_phi_i = int(settings.PHI_NADIR_MIN/dphi)
        max_bin_phi_i = int(settings.PHI_NADIR_MAX/dphi) + 1 if settings.PHI_NADIR_MAX/dphi > math.floor(settings.PHI_NADIR_MAX/dphi) else int(settings.PHI_NADIR_MAX/dphi)
        min_bin_theta_i = int(settings.THETA_NADIR_MIN/dtheta)
        max_bin_theta_i = int(settings.THETA_NADIR_MAX/dtheta) + 1 if settings.THETA_NADIR_MAX/dtheta > math.floor(settings.THETA_NADIR_MAX/dtheta) else int(settings.THETA_NADIR_MAX/dtheta)

        min_bin_nad_phi_i = int(settings.PHI_NADIR_MIN/dphi)
        max_bin_nad_phi_i = int(settings.PHI_NADIR_MAX/dphi) + 1 if settings.PHI_NADIR_MAX/dphi > math.floor(settings.PHI_NADIR_MAX/dphi) else int(settings.PHI_NADIR_MAX/dphi)
        min_bin_nad_theta_i = int(settings.THETA_NADIR_CUT_MIN/dtheta)
        max_bin_nad_theta_i = int(settings.THETA_NADIR_CUT_MAX/dtheta) + 1 if settings.THETA_NADIR_CUT_MAX/dtheta > math.floor(settings.THETA_NADIR_CUT_MAX/dtheta) else int(settings.THETA_NADIR_CUT_MAX/dtheta)
        
        count = hist.Integral(min_bin_nad_phi_i, max_bin_nad_phi_i, min_bin_nad_theta_i, max_bin_nad_theta_i)
        counts.append(count)
        # break

    '''
        New count
    '''
    new_hist = rt.TH1F('New count','New count', len(x_gap_bins)-1, np.array(x_gap_bins))
    is_filled = False
    for raw_file in raw_files:
        ft1 = fits.open(raw_file)
        photon = ft1[1].data

        filtering = photon.field('ENERGY') >= CONSIDERED_E_MIN_GEV * 1000.0
        photon = photon[filtering]
        filtering = photon.field('ENERGY') <= CONSIDERED_E_MAX_GEV * 1000.0
        photon = photon[filtering]
        filtering = photon.field('THETA') < settings.THETA_LAT_CUTOFF
        photon = photon[filtering]
        filtering = photon.field('EVENT_CLASS')[:, -settings.EVENT_CLASS_BITS['P8R2_SOURCE_V6']] == True
        photon = photon[filtering]
        filtering = photon.field('TIME') > BEGIN_SECOND_NEW_COUNT
        photon = photon[filtering]
        filtering = photon.field('TIME') < END_SECOND_NEW_COUNT
        photon = photon[filtering]
        for p in photon:
            print(p)
            new_hist.Fill(p["ENERGY"]/1000.0)
            is_filled = True
        if is_filled:
            break

    ### Visualize
    count_hist = rt.TH1F("Old Count", "Old Count", len(x_gap_bins) - 1, np.array(x_gap_bins))
    for bin_i in range(len(x_gap_bins) - 1):
        new_hist.SetBinContent(bin_i + 1, new_hist.GetBinContent(bin_i+1)/new_hist.GetBinWidth(bin_i+1))
        count_hist.SetBinContent(bin_i + 1, counts[bin_i]/count_hist.GetBinWidth(bin_i+1))

    C = rt.TCanvas('C','C',800,600)
    # C.Divide(2,1)
    count_hist.SetTitle('Previous work count map')
    count_hist.GetYaxis().SetTitle('dN/dE')
    count_hist.GetXaxis().SetTitle('E (GeV)')
    count_hist.Draw()
    new_hist.Draw("same")

    C.SetLogx()
    C.SetLogy()
    C.SaveAs("compare_old_count.pdf")
    raw_input()

    

    # latest_summary_data = rt.TFile.Open(os.path.join('data', 'root', 'extracted_data.root'),'READ')
    # new_hist = latest_summary_data.Get("count_hist")
    # for bin_i in range(new_hist.GetNbinsX()):
    #     new_hist.SetBinContent(
    #         bin_i + 1,
    #         new_hist.GetBinContent(bin_i + 1) / new_hist.GetBinWidth(bin_i + 1)
    #     )
    # del latest_summary_data

    # phi_nadirs = []
    # theta_nadirs = []

    # for week in range(settings.WEEK_BEGIN, settings.WEEK_END+1):
    #     week_photon_df = pd.read_csv(os.path.join(settings.PATH_EXTRACTED_DATA, "photon", "ft1_w{0:3d}.csv").format(week))
    #     phi_nadirs.extend(week_photon_df['phi_earth'])
    #     theta_nadirs.extend(week_photon_df['nadir'])

    # visualize
    # np_cntmap, _, _ = np.histogram2d(
    #     phi_nadirs,
    #     theta_nadirs,
    #     bins=(settings.N_BINS_PHI_NADIR, settings.N_BINS_THETA_NADIR),
    #     range=([settings.PHI_NADIR_MIN, settings.PHI_NADIR_MAX], [settings.THETA_NADIR_MIN, settings.THETA_NADIR_MAX]),        
    # )