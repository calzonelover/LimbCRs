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

TH1F *get_phi_nad_dist(TH2F *cnt_map, TH2F *exp_map)
{
    int SCALE_PHI = 5;

    auto flx_map = (TH2F *)cnt_map->Clone();
    flx_map->Divide(exp_map);

    // flx_map->Rebin2D(SCALE_PHI, 1);
    // flx_map->GetYaxis()->SetRange(THETA_E_NAD_MIN, THETA_E_NAD_MAX);
    // flx_map->GetYaxis()->SetBit(TAxis::kAxisRange);
    // int bin_y_min = flx_map->GetYaxis()->FindBin(THETA_E_NAD_MIN);
    // int bin_y_max = flx_map->GetYaxis()->FindBin(THETA_E_NAD_MAX);
    // std::cout << bin_y_min << ", " << bin_y_max << std::endl;
    // auto phi_nad_dist = (TH1F *)flx_map->ProjectionX();

    // flx_map->Rebin2D(SCALE_PHI, 1);
    auto phi_nad_dist = (TH1F *)flx_map->ProjectionX();
    auto delta_theta_nad = THETA_E_NAD_MAX - THETA_E_NAD_MIN;
    auto phi_nadir = PHI_NADIR_MIN;
    for (unsigned int i = 0; i < phi_nad_dist->GetNbinsX(); i++)
    {
        auto dphi = phi_nad_dist->GetBinWidth(i);
        std::cout << phi_nadir << ", " << phi_nadir + dphi << std::endl;
        std::cout << THETA_E_NAD_MIN << ", " << THETA_E_NAD_MAX << std::endl;
        auto cnt_div_exp_sum = Histogram::sumOverRegion(
            flx_map,
            phi_nadir, phi_nadir + dphi, THETA_E_NAD_MIN, THETA_E_NAD_MAX);
        // auto cnt_div_exp_sum = flx_map->Integral();
        std::cout << cnt_div_exp_sum << std::endl;
        phi_nad_dist->SetBinContent(i + 1, cnt_div_exp_sum);
        phi_nadir += dphi;
    }

    phi_nad_dist->Rebin(SCALE_PHI);
    for (unsigned int i = 0; i < phi_nad_dist->GetNbinsX(); i++)
    {
        phi_nad_dist->SetBinContent(i + 1, phi_nad_dist->GetBinContent(i + 1) / phi_nad_dist->GetBinWidth(i + 1));
    }

    return phi_nad_dist;
}

int main(int argc, char **argv)
{
    // Histogram (cntmap and flxmap)
    TFile *read_file = new TFile("data/root/extracted_data.root", "READ");
    auto histogram = new Histogram();
    histogram->load(read_file);

    // Flux
    auto cnt_maps = histogram->get_cnt_maps();
    auto exp_maps = histogram->get_exp_maps();

    std::vector<TH1F *> phi_nad_dists;

    for (unsigned int i_energy_bin = 0; i_energy_bin < N_E_BINS; i_energy_bin++)
    {
        phi_nad_dists.push_back(get_phi_nad_dist(cnt_maps[i_energy_bin], exp_maps[i_energy_bin]));
    }

    auto phi_nad_dist = (TH1F *)phi_nad_dists[0]->Clone();
    for (unsigned int i_energy_bin = 1; i_energy_bin < N_E_BINS; i_energy_bin++)
    {
        phi_nad_dist->Add(phi_nad_dists[i_energy_bin]);
    }

    auto c2 = new TCanvas("flxhist", "Gamma-ray Flux", 900, 500);
    // c2->SetLogx();
    // c2->SetLogy();
    c2->cd();
    phi_nad_dist->SetStats(0);
    phi_nad_dist->SetTitle("");
    phi_nad_dist->GetXaxis()->SetTitle("#phi_{nadir} (degree)");
    phi_nad_dist->GetYaxis()->SetTitle("#gamma-ray intensity (# photons / m^{-2}s^{-1}rad^{-1})");
    phi_nad_dist->Draw();
    // phi_nad_dist->SetMarkerStyle(20);
    // phi_nad_dist->SetMarkerColor(2);
    // phi_nad_dist->SetLineColor(2);

    c2->SaveAs("flx_phi_nadir_hist.png");
    read_file->Close();

    return 0;
}