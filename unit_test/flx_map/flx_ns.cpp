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
#include "../../utility/cpp/transform.h"
#include "../../settings.h"
#include "flxmap.h"

int main(int argc, char **argv)
{
    std::vector<NADIR_BOUND> nadir_bounds{
        {.phi_lower = 0.0f, .phi_upper = 30.0f, .theta_lower = THETA_E_NAD_MIN, .theta_upper = THETA_E_NAD_MAX},
        {.phi_lower = 150.0f, .phi_upper = 210.0f, .theta_lower = THETA_E_NAD_MIN, .theta_upper = THETA_E_NAD_MAX},
        {.phi_lower = 330.0f, .phi_upper = 360.0f, .theta_lower = THETA_E_NAD_MIN, .theta_upper = THETA_E_NAD_MAX},
    };

    // Histogram (cntmap and flxmap)
    TFile *read_file = new TFile("data/root/extracted_data.root", "READ");
    auto histogram = new Histogram();
    histogram->load(read_file);

    std::cout << "First cnt bin before: " << histogram->get_cnt_hist()->GetBinContent(1) << std::endl;
    std::cout << "First flx bin before: " << histogram->get_flx_hist()->GetBinContent(1) << std::endl;
    compute_multi_region_flux(histogram, nadir_bounds);
    std::cout << "First cnt bin after: " << histogram->get_cnt_hist()->GetBinContent(1) << std::endl;
    std::cout << "First flx bin after: " << histogram->get_flx_hist()->GetBinContent(1) << std::endl;

    // Flux
    auto new_flx_hist = (TH1F *)histogram->get_flx_hist();
    auto get_energy_mid_bins = histogram->get_energy_mid_bins();
    for (unsigned int i = 0; i < N_E_BINS; i++)
    {
        new_flx_hist->SetBinContent(
            i + 1,
            pow(get_energy_mid_bins[i], 2.75f) * new_flx_hist->GetBinContent(i + 1));
        new_flx_hist->SetBinError(
            i + 1,
            pow(get_energy_mid_bins[i], 2.75f) * new_flx_hist->GetBinError(i + 1));
    }
    // error band
    TH1F *err_band_flx_hist = (TH1F *)new_flx_hist->Clone();
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
            _sys_err * new_flx_hist->GetBinContent(i + 1) + new_flx_hist->GetBinError(i + 1));
    }

    auto c2 = new TCanvas("flxhist", "Gamma-ray Flux", 900, 700);
    c2->SetLogx();
    c2->SetLogy();
    c2->cd();
    new_flx_hist->SetStats(0);
    new_flx_hist->SetTitle("#gamma-Ray Spectrum (North-South)");
    new_flx_hist->Draw("E1");
    new_flx_hist->SetMarkerStyle(20);
    new_flx_hist->SetMarkerColor(2);
    new_flx_hist->SetLineColor(2);
    new_flx_hist->GetXaxis()->SetTitle("E (GeV)");
    new_flx_hist->GetYaxis()->SetTitle("#gamma-Ray Flux #times E^{2.75} (E^{1.75}m^{-2}s^{-1}sr^{-1})");

    err_band_flx_hist->SetFillColor(2);
    err_band_flx_hist->SetFillColorAlpha(2, 0.3);
    err_band_flx_hist->Draw("E3same");
    c2->SaveAs("flx_hist.png");
    read_file->Close();

    return 0;
}