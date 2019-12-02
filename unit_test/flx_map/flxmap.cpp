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

#include "../../utility/cpp/io.h"
#include "../../utility/cpp/parser.h"
#include "../../utility/cpp/histogram.h"
#include "../../utility/cpp/datatype.h"
#include "../../settings.h"
#include "flxmap.h"

// void init2DHistogram(std::vector<TH2F*> cnt_maps, std::vector<TH2F*> flx_maps){
//     for (unsigned int i_energy_bin=0; i_energy_bin < N_E_BINS; i_energy_bin++){
//         auto cntmap_name = "cntmap" + Parser::parseIntOrder(i_energy_bin);
//         auto cntmap_title = "Count map " + Parser::parseDecimal(energy_mid_bins[i_energy_bin], 2) + " GeV";
//         std::cout << cntmap_name << "\t" << cntmap_title << std::endl;
//         cnt_maps.push_back(new TH2F(
//             cntmap_name.c_str(), cntmap_title.c_str(),
//             N_BINS_PHI_NADIR, PHI_NADIR_MIN, PHI_NADIR_MAX,
//             N_BINS_THETA_NADIR, THETA_NADIR_MIN, THETA_NADIR_MAX
//         ));
//         auto flxmap_name = "flxmap" + Parser::parseIntOrder(i_energy_bin);
//         auto flxmap_title = "Flux map " + Parser::parseDecimal(energy_mid_bins[i_energy_bin], 2) + " GeV";
//         // std::cout << flxmap_name << "\t" << flxmap_title << std::endl;
//         flx_maps.push_back(new TH2F(
//             flxmap_name.c_str(), flxmap_title.c_str(),
//             N_BINS_PHI_NADIR, PHI_NADIR_MIN, PHI_NADIR_MAX,
//             N_BINS_THETA_NADIR, THETA_NADIR_MIN, THETA_NADIR_MAX
//         ));
//     }
// }

int main(int argc, char** argv){
    std::cout << "RUN!!" << std::endl;

    auto histogram = new Histogram();
    auto bla = histogram->get_energy_mid_bins();
    for (unsigned int i=0; i<50;i++) std::cout << bla[i] << std::endl; 
    
    // energy_mid_bins = (float*)malloc(N_E_BINS*sizeof(float));    
    // Histogram::assignEnergyBin(energy_mid_bins, E_START_GEV, E_STOP_GEV);
    // Histogram::init2DHistogram(cnt_maps, flx_maps, energy_mid_bins);


    // for (unsigned int week=WEEK_BEGIN; week <= WEEK_END; week++){
    //     std::vector<FT1> ft1_rows = FileIO::readPhotonCSV(week);
    //     std::cout << "# of week: " << week << " FT1 = " << ft1_rows.size() << std::endl;
    //     for (auto ft1_row : ft1_rows){
    //         std::cout << ft1_row.P8R2_SOURCE_V6 << ", " << ft1_row.P8R2_ULTRACLEANVETO_V6 << ", " << ft1_row.energy_gev << std::endl;
    //     }
    // }
    return 0;
}