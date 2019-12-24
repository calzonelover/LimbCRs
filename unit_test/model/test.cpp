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
#include "../../settings.h"
#include "test.h"

int main(int argc, char** argv){
    SpectrumModel spectrum_model = SPL;
    Model::init(spectrum_model);
    Model::computeGammaSpectrum(spectrum_model, 4, 2.7, 2.0, 300);
    exit(0);

    // Histogram (cntmap and flxmap)
    TFile *read_file = new TFile("data/root/extracted_data.root","READ");
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

    TF1 *spl = new TF1("SinglePowerLaw", Formula::spl, 10, 1000, 2);
    spl->SetParameter(0, 5.0);
    spl->SetParameter(1, 2.66);
    cnt_hist->Fit(spl);
    // Flux
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
    auto c2 = new TCanvas("flxhist", "Gamma-ray Flux", 900, 700);
    c2->SetLogx();
    c2->SetLogy();
    c2->cd();
    flx_hist->SetStats(0);
    flx_hist->SetTitle("#gamma-Ray Spectrum");
    flx_hist->Draw("E1");
    flx_hist->GetXaxis()->SetTitle("E (GeV)");
    flx_hist->GetYaxis()->SetTitle("#gamma-Ray Flux #times E^{2.75} (E^{1.75}m^{-2}s^{-1}sr^{-1})");
    c2->SaveAs("flx_hist.png");

    read_file->Close();
    return 0;
}