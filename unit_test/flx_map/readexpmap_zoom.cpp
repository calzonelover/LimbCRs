#include <stdio.h>
#include <stdlib.h>
#include <string>
#include <vector>
#include <sstream>
#include <iostream>
#include <fstream>
#include <ctime>
#include <math.h>

// ROOT
#include "TColor.h"
#include "TPad.h"
#include "TStyle.h"
#include "TMath.h"
#include "TF1.h"
#include "TH1D.h"
#include "TH1F.h"
#include "TH2F.h"
#include "TFile.h"
#include "TCanvas.h"

#include "../../utility/cpp/io.h"
#include "../../utility/cpp/parser.h"
#include "../../utility/cpp/histogram.h"
#include "../../utility/cpp/datatype.h"
#include "../../utility/cpp/formula.h"
#include "../../utility/cpp/visualize.h"
#include "../../settings.h"
#include "flxmap.h"

void set_hist2d_ranges(std::vector<TH2F *> &maps, float min_y, float max_y, float min_x = PHI_NADIR_MIN, float max_x = PHI_NADIR_MAX)
{
    for (unsigned int i = 0; i < maps.size(); i++)
    {
        maps[i]->GetXaxis()->SetRange(min_x, max_x);
        maps[i]->GetYaxis()->SetRange(min_y, max_y);
    }
}

int main(int argc, char **argv)
{
    float min_y = 60.0f;
    float max_y = THETA_NADIR_MAX - 2;
    unsigned int MERGE_BIN_X = 2;
    unsigned int MERGE_BIN_Y = 5;

    // Histogram (cntmap and flxmap)
    TFile *read_file = new TFile("data/root/extracted_data.root", "READ");
    auto histogram = new Histogram();
    histogram->load(read_file);

    auto cnt_hist = histogram->get_cnt_hist();
    auto c1 = new TCanvas("cnthist", "Count", 900, 700);
    c1->SetLogx();
    c1->SetLogy();
    c1->cd();
    cnt_hist->SetStats(0);
    cnt_hist->Draw("E1");
    cnt_hist->GetXaxis()->SetTitle("Energy (GeV)");
    cnt_hist->GetYaxis()->SetTitle("N");
    c1->SaveAs("count_hist.png");
    // Count
    auto cntmaps = histogram->get_cnt_maps();
    for (auto cntmap : cntmaps)
    {
        cntmap->Rebin2D(MERGE_BIN_X, MERGE_BIN_Y);
    }
    int p[4] = {0, 15, 30, 49};
    Visualize::plotMapQuadrant(
        cntmaps, p,
        "cntmaps", "Count Maps",
        "polar_cntmaps.png", "SURF2POLZ",
        "Count (photons)", min_y, max_y);
    Visualize::plotMapQuadrant(
        cntmaps, p,
        "cntmaps", "Count Maps",
        "cartesian_cntmaps.png", "COLZ",
        "Count (photons)", min_y, max_y);

    // flux
    auto flxmaps = histogram->get_flx_maps();
    for (auto flxmap : flxmaps)
    {
        flxmap->Rebin2D(MERGE_BIN_X, MERGE_BIN_Y);
    }
    Visualize::plotMapQuadrant(
        flxmaps, p,
        "flxmaps", "Flux Maps",
        "polar_flxmaps.png", "SURF2POLZ",
        "Flux (GeV^{-1}s^{-1}sr^{-1}m^{2})",
        min_y, max_y);
    Visualize::plotMapQuadrant(
        flxmaps, p,
        "flxmaps", "Flux Maps",
        "cartesian_flxmaps.png", "COLZ",
        "Flux (GeV^{-1}s^{-1}sr^{-1}m^{2})",
        min_y, max_y);

    TF1 *spl = new TF1("SinglePowerLaw", Formula::spl, 10, 1000, 2);
    spl->SetParameter(0, 5.0);
    spl->SetParameter(1, 2.66);
    cnt_hist->Fit(spl);
    // Flux
    auto flx_hist = histogram->get_flx_hist();
    auto get_energy_mid_bins = histogram->get_energy_mid_bins();
    for (unsigned int i = 0; i < N_E_BINS; i++)
    {
        flx_hist->SetBinContent(
            i + 1,
            pow(get_energy_mid_bins[i], 2.75f) * flx_hist->GetBinContent(i + 1));
        flx_hist->SetBinError(
            i + 1,
            pow(get_energy_mid_bins[i], 2.75f) * flx_hist->GetBinError(i + 1));
    }
    // error band
    TH1F *err_band_flx_hist = (TH1F *)flx_hist->Clone();
    float _sys_err;
    for (unsigned int i = 0; i < N_E_BINS; i++)
    {
        if (get_energy_mid_bins[i] < 100.0)
        {
            _sys_err = 0.05;
        }
        else if (get_energy_mid_bins[i] >= 100.0)
        {
            _sys_err = 0.05 + 0.1 * (log10(1000 * get_energy_mid_bins[i]) - 5.0);
        }
        err_band_flx_hist->SetBinError(
            i + 1,
            _sys_err * flx_hist->GetBinContent(i + 1) + flx_hist->GetBinError(i + 1));
    }

    auto c2 = new TCanvas("flxhist", "Gamma-ray Flux", 900, 700);
    c2->SetLogx();
    c2->SetLogy();
    c2->cd();
    flx_hist->SetStats(0);
    flx_hist->SetTitle("#gamma-Ray Spectrum");
    flx_hist->Draw("E1");
    flx_hist->SetMarkerStyle(20);
    flx_hist->SetMarkerColor(2);
    flx_hist->SetLineColor(2);
    flx_hist->GetXaxis()->SetTitle("E (GeV)");
    flx_hist->GetYaxis()->SetTitle("#gamma-Ray Flux #times E^{2.75} (E^{1.75}m^{-2}s^{-1}sr^{-1})");

    err_band_flx_hist->SetFillColor(2);
    err_band_flx_hist->SetFillColorAlpha(2, 0.3);
    err_band_flx_hist->Draw("E3same");
    c2->SaveAs("flx_hist.png");
    read_file->Close();

    // Expmaps
    auto expmaps = FileIO::readExposureMap();
    for (auto expmap : expmaps)
    {
        expmap->Rebin2D(MERGE_BIN_X, MERGE_BIN_Y);
    }
    // int p[4] = {0, 15, 30, 49};
    Visualize::plotMapQuadrant(
        expmaps, p,
        "expmaps", "Exposure Maps",
        "polar_expmaps.png", "SURF2POLZ",
        "Exposure (m^{2}s)", min_y, max_y);
    Visualize::plotMapQuadrant(
        expmaps, p,
        "expmaps", "Exposure Maps",
        "cartesian_expmaps.png", "COLZ",
        "Exposure (m^{2}s)", min_y, max_y);
    return 0;
}