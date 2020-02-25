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
#include "TCanvas.h"
#include "TGraph.h"

#include "../../utility/cpp/io.h"
#include "../../utility/cpp/parser.h"
#include "../../utility/cpp/histogram.h"
#include "../../utility/cpp/visualize.h"
#include "../../utility/cpp/datatype.h"
#include "../../settings.h"

int main(int argc, char** argv){
    std::vector<TH1F*> nadir_dist, shifted_nadir_dist;
    float *energy_mid_bins, *energy_edge_bins;
    energy_mid_bins = (float*)malloc(N_E_BINS*sizeof(float));
    energy_edge_bins = (float*)malloc((N_E_BINS+1)*sizeof(float));
    Histogram::assignEnergyBin(energy_mid_bins, energy_edge_bins);
    for (unsigned int i_energy_bin=0; i_energy_bin < N_E_BINS; i_energy_bin++){
        auto title = "#theta_{nad} distribution (E " + std::to_string(energy_edge_bins[i_energy_bin])
                    + " - " + std::to_string(energy_edge_bins[i_energy_bin+1]) + " GeV)";        
        auto name = "ThetaNadirDist" + Parser::parseIntOrder(i_energy_bin);
        nadir_dist.push_back(new TH1F(
            name.c_str(), title.c_str(),
            N_BINS_THETA_NADIR, THETA_NADIR_MIN, THETA_NADIR_MAX
        ));
        auto title_sh = "#theta_{shifted_nad} distribution (E " + std::to_string(energy_edge_bins[i_energy_bin])
                    + " - " + std::to_string(energy_edge_bins[i_energy_bin+1]) + " GeV)";        
        auto name_sh = "ThetaShiftedNadirDist" + Parser::parseIntOrder(i_energy_bin);        
        shifted_nadir_dist.push_back(new TH1F(
            name_sh.c_str(), title_sh.c_str(),
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
                auto bin_i = Histogram::findBin(photon.energy_gev, energy_edge_bins);
                nadir_dist[bin_i]->Fill(photon.nadir);
                shifted_nadir_dist[bin_i]->Fill(photon.shifted_nadir);
            }
        }
    }

    auto d_theta = (THETA_NADIR_MAX - THETA_NADIR_MIN)/N_BINS_THETA_NADIR;
    auto theta_nadir_min_bin = int(floor(THETA_NADIR_MIN/d_theta));
    auto theta_nadir_max_bin = (THETA_NADIR_MAX/d_theta > floor(THETA_NADIR_MAX/d_theta)) ? int(floor(THETA_NADIR_MAX/d_theta)) + 1 : int(floor(THETA_NADIR_MAX/d_theta));
    // Plot and save
    for (unsigned int i_energy_bin=0; i_energy_bin < N_E_BINS; i_energy_bin++){
        auto name = "nadir_dist_" + std::to_string(i_energy_bin);
        auto c = new TCanvas("Nadir_dist", "theta nadir distribution", 800, 600);
        c->SetLogy();
        c->cd();
        // nadir
        nadir_dist[i_energy_bin]->SetStats(0);
        nadir_dist[i_energy_bin]->SetLineColor(2);
        nadir_dist[i_energy_bin]->Draw("hist");
        nadir_dist[i_energy_bin]->GetXaxis()->SetTitle("#theta_{nad}");
        nadir_dist[i_energy_bin]->GetXaxis()->SetRangeUser(60, 80);
        nadir_dist[i_energy_bin]->GetYaxis()->SetTitle("Count");
        // color band
        auto *nadir_dist_h = (TH1F*)nadir_dist[i_energy_bin]->Clone("nadir_dist_h");
        nadir_dist_h->GetXaxis()->SetRange(THETA_E_NAD_MIN,THETA_E_NAD_MAX);
        nadir_dist_h->SetFillColorAlpha(5, 0.3);
        nadir_dist_h->GetXaxis()->SetRangeUser(THETA_E_NAD_MIN, THETA_E_NAD_MAX);
        nadir_dist_h->Draw("same");
        int n_limb_nad = nadir_dist[i_energy_bin]->Integral(theta_nadir_min_bin, theta_nadir_max_bin);
        // shifted nadir
        shifted_nadir_dist[i_energy_bin]->SetStats(0);
        shifted_nadir_dist[i_energy_bin]->SetLineColor(4);
        shifted_nadir_dist[i_energy_bin]->Draw("histsame");
        shifted_nadir_dist[i_energy_bin]->GetXaxis()->SetTitle("#theta_{shifted_nad}");
        shifted_nadir_dist[i_energy_bin]->GetXaxis()->SetRangeUser(60, 80);
        shifted_nadir_dist[i_energy_bin]->GetYaxis()->SetTitle("Count"); 
        // color band
        auto *shifted_nadir_dist_h = (TH1F*)shifted_nadir_dist[i_energy_bin]->Clone("shifted_nadir_dist_h");
        shifted_nadir_dist_h->GetXaxis()->SetRange(THETA_E_NAD_MIN,THETA_E_NAD_MAX);
        shifted_nadir_dist_h->SetFillColorAlpha(7, 0.3);
        shifted_nadir_dist_h->GetXaxis()->SetRangeUser(THETA_E_NAD_MIN, THETA_E_NAD_MAX);
        shifted_nadir_dist_h->Draw("same");
        int n_limb_shifted_nad = shifted_nadir_dist[i_energy_bin]->Integral(theta_nadir_min_bin, theta_nadir_max_bin);

        nadir_dist[i_energy_bin]->SetTitle("#theta_{nad}");
        nadir_dist_h->SetTitle(("N_{Limb, #theta_{nad}} = " + std::to_string(n_limb_nad)).c_str());
        shifted_nadir_dist[i_energy_bin]->SetTitle("#theta_{shifted_nad}");
        shifted_nadir_dist_h->SetTitle(("N_{Limb, #theta_{shifted_nad}} = " + std::to_string(n_limb_shifted_nad)).c_str());
        c->BuildLegend(0.7, 0.7, 1.0, 1.0);
        c->SaveAs((name + ".png").c_str());       
    }
    // for (unsigned int i_energy_bin=0; i_energy_bin < N_E_BINS; i_energy_bin++){
    //     auto name = "shifted_nadir_dist_" + std::to_string(i_energy_bin);
    //     auto c = new TCanvas("ShiftedNadir_dist", "shfited theta nadir distribution", 800, 600);
    //     c->SetLogy();
    //     c->cd();
    //     // shifted nadir
    //     shifted_nadir_dist[i_energy_bin]->SetStats(0);
    //     shifted_nadir_dist[i_energy_bin]->Draw();
    //     shifted_nadir_dist[i_energy_bin]->GetXaxis()->SetTitle("#theta_{shifted_nad}");
    //     shifted_nadir_dist[i_energy_bin]->GetXaxis()->SetRangeUser(60, 80);
    //     shifted_nadir_dist[i_energy_bin]->GetYaxis()->SetTitle("Count");
    //     // color band
    //     auto *nadir_dist_h = (TH1F*)nadir_dist[i_energy_bin]->Clone("nadir_dist_h");
    //     nadir_dist_h->GetXaxis()->SetRange(THETA_E_NAD_MIN,THETA_E_NAD_MAX);
    //     nadir_dist_h->SetFillColorAlpha(2, 0.5);
    //     nadir_dist_h->GetXaxis()->SetRangeUser(THETA_E_NAD_MIN, THETA_E_NAD_MAX);
    //     nadir_dist_h->Draw("same");
    //     c->SaveAs((name + ".png").c_str());
    // }
    return 0;
}