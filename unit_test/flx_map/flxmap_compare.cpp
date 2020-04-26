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
#include "TH2F.h"
#include "TCanvas.h"

#include "../../utility/cpp/io.h"
#include "../../utility/cpp/parser.h"
#include "../../utility/cpp/histogram.h"
#include "../../utility/cpp/datatype.h"
#include "../../settings.h"
#include "flxmap.h"

int main(int argc, char** argv){
    auto histogram1 = new Histogram(true);
    auto histogram2 = new Histogram(true);
    for (unsigned int week=WEEK_BEGIN; week <= WEEK_END; week++){
        std::vector<FT1> ft1_rows = FileIO::readPhotonCSV(week);
        std::cout << "# of week: " << week << " FT1 = " << ft1_rows.size() << std::endl;
        for (auto photon : ft1_rows){
            if (
                photon.P8R2_ULTRACLEANVETO_V6 && photon.energy_gev > E_START_GEV && photon.energy_gev < E_STOP_GEV
                && photon.theta_lat < THETA_LAT_CUTOFF
            ){
                histogram1->fillPhoton(photon);
                histogram2->fillPhoton(photon);
            }
        }
    }
    histogram1->computeFlux1();
    histogram2->computeFlux2();

    auto flx_hist1 = histogram1->get_flx_hist();
    auto flx_hist2 = histogram2->get_flx_hist();
    flx_hist1->Divide(flx_hist2);

    auto c2 = new TCanvas("flxhist", "Gamma-ray Flux", 900, 700);
    c2->SetLogx();
    c2->SetLogy();
    c2->cd();
    flx_hist1->SetStats(0);
    flx_hist1->SetTitle("#gamma-Ray Spectrum");
    flx_hist1->Draw("E1");
    flx_hist1->GetXaxis()->SetTitle("E (GeV)");
    flx_hist1->GetYaxis()->SetTitle("#gamma-Ray Flux method1/method2");
    c2->SaveAs("flx_hist_compare.png");
    return 0;
}