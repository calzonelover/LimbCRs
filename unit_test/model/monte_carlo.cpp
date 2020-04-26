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


int main(int argc, char** argv){
    /// settings
    // PS
    std::vector<float> optimized_params_spl{
        0.0108668 , 2.82851 , 2.70266 , 2.65207 , 342.546
    };
    std::vector<float> optimized_params_bpl{
        0.0108818 , 1.98848 , 2.86015 , 2.63161 , 333.115
    };
    // SA


    TFile *read_file = new TFile("data/root/extracted_data.root","READ");
    auto histogram = new Histogram();
    histogram->load(read_file);
    auto flx_hist = histogram->get_flx_hist();
    auto get_energy_mid_bins = histogram->get_energy_mid_bins();
    for (unsigned int i=0; i<N_E_BINS; i++){
        flx_hist->SetBinContent(
            i+1,
            pow(get_energy_mid_bins[i], 2.75f)*flx_hist->GetBinContent(i+1)
        );
        flx_hist->SetBinError(
            i+1,
            pow(get_energy_mid_bins[i], 2.75f)*flx_hist->GetBinError(i+1)
        );
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
    flx_hist->GetYaxis()->SetTitle("E^{2.75}Flux (GeV^{1.75}m^{-2}s^{-1}sr^{-1})");
    flx_hist->GetXaxis()->SetTitle("E (GeV)");
    flx_hist->SetTitle("Measurement");
    flx_hist->Draw("E1");

    gSPL->SetLineWidth(2);
    gSPL->SetLineStyle(2);
    gSPL->SetFillColor(0);
    gSPL->SetLineColor(4);
    gSPL->SetTitle("Model incident proton SPL");
    gSPL->Draw("same");

    gBPL->SetLineWidth(3);
    gBPL->SetLineStyle(5);
    gBPL->SetFillColor(0);
    gBPL->SetLineColor(8);
    gBPL->SetTitle("Model incident proton BPL");
    gBPL->Draw("same");

    c->BuildLegend();

    flx_hist->SetTitle("Flux Model from Simulated Annealing");
    // flx_hist->SetTitle("Flux Model from Particle Swarm algorithm");
    c->SaveAs("fitted_result.pdf");

    read_file->Close();
    return 0;
}