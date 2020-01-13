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
#include "../../settings.h"
#include "flxmap.h"

int main(int argc, char** argv){
    /*
    // Histogram (cntmap and flxmap)
    TFile *read_file = new TFile("data/root/extracted_data.root","READ");
    auto histogram = new Histogram();
    histogram->load(read_file);
    // for (unsigned int week=WEEK_BEGIN; week <= WEEK_END; week++){
    //     std::vector<FT1> ft1_rows = FileIO::readPhotonCSV(week);
    //     std::cout << "# of week: " << week << " FT1 = " << ft1_rows.size() << std::endl;
    //     for (auto ft1_row : ft1_rows){
    //         histogram->fillPhoton(ft1_row);
    //         // std::cout << ft1_row.P8R2_SOURCE_V6 << ", " << ft1_row.P8R2_ULTRACLEANVETO_V6 << ", " << ft1_row.energy_gev << std::endl;
    //     }
    // }
    // histogram->computeFlux2();
    // histogram->save();   

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

    */

    // Expmaps
    auto expmaps = FileIO::readExposureMap();
    int p[4] = {0, 15, 30, 49};
    Visualize::plotMapQuadrant(
        expmaps, p,
        "expmaps", "Exposure Maps",
        "polar_expmaps.png", "SURF2POLZ"
    );
    Visualize::plotMapQuadrant(
        expmaps, p,
        "expmaps", "Exposure Maps",
        "cartesian_expmaps.png", "COLZ"
    );
    // read_file->Close();
    return 0;
}