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
#include "TH1F.h"

#include "../../utility/cpp/io.h"
#include "../../utility/cpp/parser.h"
#include "../../utility/cpp/histogram.h"
#include "../../utility/cpp/visualize.h"
#include "../../utility/cpp/datatype.h"
#include "../../settings.h"

int main(int argc, char** argv){
    TH1F *nadir_dist, *shifted_nadir_dist;
    float *_energy_mid_bins, float *_energy_edge_bins;
    energy_mid_bins = (float*)malloc(N_E_BINS*sizeof(float));
    energy_edge_bins = (float*)malloc((N_E_BINS+1)*sizeof(float));
    Histogram::assignEnergyBin(energy_mid_bins, energy_edge_bins);
    for (unsigned int i_energy_bin=0; i_energy_bin < N_E_BINS; i_energy_bin++){
        auto flxmap_name = "flxmap" + Parser::parseIntOrder(i_energy_bin);
        auto flxmap_title = "Flux map " + Parser::parseDecimal(_energy_mid_bins[i_energy_bin], 2) + " GeV";
        nadir_dist.push_back(new TH1F(
            flxmap_name.c_str(), flxmap_title.c_str(),
            N_BINS_THETA_NADIR, THETA_NADIR_MIN, THETA_NADIR_MAX
        ));
    }
    // Fill histograms
    for (unsigned int week=WEEK_BEGIN; week <= WEEK_END; week++){
        std::vector<FT1> ft1_rows = FileIO::readPhotonCSV(week);
        std::cout << "# of week: " << week << " FT1 = " << ft1_rows.size() << std::endl;
        for (auto photon : ft1_rows){
            if (
                photon.P8R2_ULTRACLEANVETO_V6 && photon.energy_gev > E_START_GEV && photon.energy_gev < E_STOP_GEV
                && photon.theta_lat < THETA_LAT_CUTOFF
            ){
                auto bin_i = Histogram::findbin(_energy_edge_bins, photon.energy_gev);
                nadir_dist[bin_i]->Fill(photon.nadir);
            }
        }
    }
    // Plot and save
    for (unsigned int i_energy_bin=0; i_energy_bin < N_E_BINS; i_energy_bin++){
        auto name = "nadir_dist_" + std::to_string(i_energy_bin);
        auto title = "Nadir dist E" + energy_edge_bins[i_energy_bin] + " - " + energy_edge_bins[i_energy_bin+1] + " GeV";
        auto c = new TCanvas("Nadir_dist", "theta nadir distribution", 800, 600);
        c->SetLogy();
        c->cd();
        nadir_dist[i_energy_bin]->SetStats(0);
        nadir_dist[i_energy_bin]->Draw("E1");
        nadir_dist[i_energy_bin]->SetTitle(title.c_str);
        nadir_dist[i_energy_bin]->GetXaxis()->SetTitle("#theta_{nad}");
        nadir_dist[i_energy_bin]->GetYaxis()->SetTitle("Count");
        c->SaveAs(name.c_str());
    }
    return 0;
}