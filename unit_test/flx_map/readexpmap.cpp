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
#include "TH1F.h"
#include "TH2F.h"
#include "TCanvas.h"

#include "../../utility/cpp/io.h"
#include "../../utility/cpp/parser.h"
#include "../../utility/cpp/histogram.h"
#include "../../utility/cpp/datatype.h"
#include "../../utility/cpp/visualize.h"
#include "../../settings.h"
#include "flxmap.h"

int main(int argc, char** argv){
    // Histogram (cntmap and flxmap)
    auto histogram = new Histogram(false);
    histogram->load();
    // auto bla = histogram->get_energy_mid_bins();
    // for (unsigned int i=0; i<50;i++) std::cout << Parser::parseDecimal(bla[i], 3) << std::endl;

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
    cnt_hist->Draw("E1");
    cnt_hist->GetXaxis()->SetTitle("E (GeV)");
    cnt_hist->GetYaxis()->SetTitle("N");
    c1->SaveAs("count_hist.png");

    // auto flx_hist = histogram->get_flx_hist();
    // auto c2 = new TCanvas("flxhist", "Differential Flux", 900, 700);
    // c2->SetLogx();
    // c2->SetLogt();
    // flx_hist->Draw("E1");

    /*
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
    */
    return 0;
}