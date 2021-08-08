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
#include "TLatex.h"
#include "TStyle.h"
#include "TMath.h"
#include "TF1.h"
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
#include "../../utility/cpp/model.h"
#include "../../utility/cpp/optimizer.h"
#include "../../settings.h"

int main(int argc, char **argv)
{

    /// settings
    // SPL: PS
    // N_all: 0.0110524 , N_0: 2.26008 , g1: 2.62515 , g2: 2.65902 , E_b: 322.662
    // Loss: 298.208 , Loss SD: 0.0981467
    // BPL: PS
    // N_all: 0.0110726 , N_0: 4.04837 , g1: 2.90502 , g2: 2.65259 , E_b: 326.956
    // Loss: 297.471 , Loss SD: 0.0653248

    // PS result 2
    std::vector<float> optimized_params_spl{
        0.0110524, 2.26008, 2.62515, 2.65902, 322.662};
    std::vector<float> optimized_params_bpl{
        0.0110726, 4.04837, 2.90502, 2.65259, 326.956};

    TFile *read_file = new TFile("data/root/extracted_data.root", "READ");
    auto histogram = new Histogram();
    histogram->load(read_file);

    std::vector<NADIR_BOUND> nadir_bounds{
        {.phi_lower = 0.0f, .phi_upper = 30.0f, .theta_lower = THETA_E_NAD_MIN, .theta_upper = THETA_E_NAD_MAX},
        {.phi_lower = 150.0f, .phi_upper = 210.0f, .theta_lower = THETA_E_NAD_MIN, .theta_upper = THETA_E_NAD_MAX},
        {.phi_lower = 330.0f, .phi_upper = 360.0f, .theta_lower = THETA_E_NAD_MIN, .theta_upper = THETA_E_NAD_MAX},
    };
    compute_multi_region_flux(histogram, nadir_bounds);

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

    Model *spl_model = new Model(SPL);
    spl_model->computeGammaSpectrum(optimized_params_spl);
    TGraph *gSPL = spl_model->readResult(2.75f);
    delete spl_model;

    Model *bpl_model = new Model(BPL);
    bpl_model->computeGammaSpectrum(optimized_params_bpl);
    TGraph *gBPL = bpl_model->readResult(2.75f);
    delete bpl_model;

    // visualize
    auto c = new TCanvas("model_obs_spl", "model_obs_spl", 900, 700);

    c->SetLogx();
    c->SetLogy();
    flx_hist->SetStats(0);
    // flx_hist->GetYaxis()->SetTitle("#gamma-ray Flux #times E^{2.75} (GeV^{1.75}m^{-2}s^{-1}sr^{-1})");
    flx_hist->GetYaxis()->SetTitle("");
    // flx_hist->GetXaxis()->SetTitle("E (GeV)");
    flx_hist->GetXaxis()->SetTitle("");
    flx_hist->GetXaxis()->SetTitleOffset(1.2);
    flx_hist->SetTitle("Measurement");
    flx_hist->Draw("E1");
    flx_hist->SetMarkerStyle(20);
    flx_hist->SetMarkerColor(2);
    flx_hist->SetLineColor(2);

    // draw band
    err_band_flx_hist->SetFillColor(2);
    err_band_flx_hist->SetFillColorAlpha(2, 0.3);

    gSPL->SetLineWidth(2);
    gSPL->SetLineStyle(2);
    gSPL->SetFillColor(0);
    gSPL->SetLineColor(4);
    gSPL->SetTitle("SPL model of CR proton");
    gSPL->Draw("same");

    gBPL->SetLineWidth(3);
    gBPL->SetLineStyle(5);
    gBPL->SetFillColor(0);
    gBPL->SetLineColor(8);
    gBPL->SetTitle("BPL model of CR proton");
    gBPL->Draw("same");

    c->BuildLegend(0.2, 0.2, 0.6, 0.42);
    flx_hist->SetTitle("");
    err_band_flx_hist->Draw("E3same");

    flx_hist->Draw("E1same");
    gSPL->Draw("same");
    gBPL->Draw("same");

    flx_hist->GetYaxis()->SetLabelFont(43); // Absolute font size in pixel (precision 3)
    flx_hist->GetYaxis()->SetLabelSize(25);
    flx_hist->GetXaxis()->SetLabelFont(43); // Absolute font size in pixel (precision 3)
    flx_hist->GetXaxis()->SetLabelSize(25);

    c->cd();
    TPad *pad1 = new TPad("pad1", "pad1", 0.0, 0.0, 0.055, 1.0);
    pad1->Range(0, 0, 1, 1);
    pad1->SetBottomMargin(0);
    pad1->SetGridx();
    pad1->Draw();
    pad1->cd();
    TLatex *tt = new TLatex();
    tt->SetTextAlign(12);
    tt->SetTextSize(0.5);
    tt->SetTextAngle(90);
    tt->DrawLatex(0.5, 0.35, "#gamma-ray Flux #times E^{2.75} (GeV^{1.75}m^{-2}s^{-1}sr^{-1})");
    c->cd();
    TPad *pad2 = new TPad("pad2", "pad2", 0.7, 0.0, 1.0, 0.045);
    pad2->Range(0, 0, 1, 1);
    pad2->SetBottomMargin(0);
    pad2->SetGridx();
    pad2->Draw();
    pad2->cd();
    TLatex *tt2 = new TLatex();
    tt2->SetTextAlign(32);
    tt2->SetTextSize(0.8);
    tt2->SetTextAngle(0);
    tt2->DrawLatex(0.5, 0.5, "E (GeV)");

    // flx_hist->SetTitle("Flux Model from Simulated Annealing");
    c->SaveAs("fitted_result.pdf");

    read_file->Close();
    return 0;
}