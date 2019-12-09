#include <stdio.h>
#include <stdlib.h>
#include <string>
#include <vector>
#include <sstream>
#include <iostream>
#include <fstream>
#include <ctime>
#include <math.h>

#include "TH1F.h"
#include "TH2F.h"
#include "TFile.h"

#include "../../settings.h"
#include "../../utility/cpp/io.h"
#include "../../utility/cpp/parser.h"

#include "histogram.h"

Histogram::Histogram(){
    energy_mid_bins = (float*)malloc(N_E_BINS*sizeof(float));
    energy_edge_bins = (float*)malloc((N_E_BINS+1)*sizeof(float));
    Histogram::assignEnergyBin(energy_mid_bins, energy_edge_bins);
    Histogram::init2DHistogram(cnt_maps, flx_maps, energy_mid_bins);
    Histogram::assignExposureMap(exp_maps);
    counts = new TH1F("count", "Count", N_E_BINS, energy_edge_bins);
    fluxes = new TH1F("flux", "Flux", N_E_BINS, energy_edge_bins);
}

void Histogram::assignEnergyBin(float *_energy_mid_bins, float *_energy_edge_bins, float energy_start_gev, float energy_end_gev){
    float divider, e2d, e1d, ln;
    for (unsigned int i=0; i <= N_E_BINS; i++){
        _energy_edge_bins[i] = energy_start_gev * pow(energy_end_gev/energy_start_gev, float(i)/float(N_E_BINS));
    }
    for (unsigned i=0; i < N_E_BINS; i++){
        divider = 1.0f - float(GAMMA);
        e2d = pow(_energy_edge_bins[i+1], divider);
        e1d = pow(_energy_edge_bins[i], divider);
        ln = log(0.5f*(e2d - e1d)+ e1d);
        _energy_mid_bins[i] = exp(ln/(divider));
    }
}

void Histogram::init2DHistogram(std::vector<TH2F*> _cnt_maps, std::vector<TH2F*> _flx_maps, float *_energy_mid_bins){
    for (unsigned int i_energy_bin=0; i_energy_bin < N_E_BINS; i_energy_bin++){
        auto cntmap_name = "cntmap" + Parser::parseIntOrder(i_energy_bin);
        auto cntmap_title = "Count map " + Parser::parseDecimal(_energy_mid_bins[i_energy_bin], 2) + " GeV";
        // std::cout << cntmap_name << "\t" << cntmap_title << std::endl;
        _cnt_maps.push_back(new TH2F(
            cntmap_name.c_str(), cntmap_title.c_str(),
            N_BINS_PHI_NADIR, PHI_NADIR_MIN, PHI_NADIR_MAX,
            N_BINS_THETA_NADIR, THETA_NADIR_MIN, THETA_NADIR_MAX
        ));
        auto flxmap_name = "flxmap" + Parser::parseIntOrder(i_energy_bin);
        auto flxmap_title = "Flux map " + Parser::parseDecimal(_energy_mid_bins[i_energy_bin], 2) + " GeV";
        // std::cout << flxmap_name << "\t" << flxmap_title << std::endl;
        _flx_maps.push_back(new TH2F(
            flxmap_name.c_str(), flxmap_title.c_str(),
            N_BINS_PHI_NADIR, PHI_NADIR_MIN, PHI_NADIR_MAX,
            N_BINS_THETA_NADIR, THETA_NADIR_MIN, THETA_NADIR_MAX
        ));
    }
}

void Histogram::assignExposureMap(std::vector<TH2F*> _exp_maps){
    _exp_maps = FileIO::readExposureMap();
}


int Histogram::findBin(float energy){
    int matched_bin_i;
    for (unsigned int i=0; i<N_E_BINS; i++){
        if (energy > energy_edge_bins[i] &&  energy < energy_edge_bins[i+1]){
            matched_bin_i = i;
            break;
        }
    }
    return matched_bin_i;
}

void Histogram::fillPhoton(float energy, float theta_nad, float phi_nad){
    auto bin_index = findBin(energy);
    cnt_maps[bin_index]->Fill(phi_nad, theta_nad);
    counts->Fill(energy);
}

void Histogram::computeFlux(){
    auto d_phi = (PHI_NADIR_MAX - PHI_NADIR_MIN)/N_BINS_PHI_NADIR;
    auto d_theta = (THETA_NADIR_MAX - THETA_NADIR_MIN)/N_BINS_THETA_NADIR;
    for (unsigned int i_energy_bin=0; i_energy_bin<N_E_BINS; i_energy_bin++){
        auto cntmap = (TH2F*) cnt_maps[i_energy_bin]->Clone();
        auto expmap = (TH2F*) exp_maps[i_energy_bin]->Clone();
        cntmap->Divide(expmap);
        flx_maps[i_energy_bin] = cntmap;
        // For fluxes
        auto solid_angle_i = 0.0f;
        auto i_min = PHI_NADIR_MIN/d_phi;
        auto i_max = PHI_NADIR_MAX/d_phi;
        auto j_min = THETA_NADIR_MIN/d_theta;
        auto j_max = THETA_NADIR_MAX/d_theta;
        for (unsigned int i=i_min; i < i_max; i++){
            for (unsigned int j=j_min; j < j_max; j++){
                solid_angle_i += exp_maps[i_energy_bin]->GetBinContent(i+1, j+1);
            }
        }
        fluxes->SetBinContent(
            i_energy_bin+1,
            counts->GetBinContent(i_energy_bin+1)/(solid_angle_i * (energy_edge_bins[i+1] - energy_edge_bins[i]))
        );
    }
    // calc fluxes
    int(floor(energy_mid_bins[i_energy]))
}

void Histogram::save(){
    TFile out_file("data/root/extracted_data.root","RECREATE");
    for (unsigned int i=0; i<N_E_BINS; i++){
        cnt_maps[i]->Write();
        exp_maps[i]->Write();
        flx_maps[i]->Write();
    }
    out_file.Close();
};

void Histogram::load(){
    TFile read_file("data/root/extracted_data.root","READ");
    for (unsigned int i=0; i<N_E_BINS; i++){
        auto cntmap_name = "cntmap" + Parser::parseIntOrder(i);
        read_file.GetObject(cntmap_name.c_str(), cnt_maps[i]);
        auto expmap_name = "expmap" + Parser::parseIntOrder(i);
        read_file.GetObject(expmap_name.c_str(), exp_maps[i]);
        auto flxmap_name = "flxmap" + Parser::parseIntOrder(i);
        read_file.GetObject(flxmap_name.c_str(), flx_maps[i]);      
    }
    read_file.Close();   
};


float* Histogram::get_energy_mid_bins(){
    return energy_mid_bins;
}
float* Histogram::get_energy_edge_bins(){
    return energy_mid_bins;
}

std::vector<TH2F*> Histogram::get_cnt_maps(){
    return cnt_maps;
}
std::vector<TH2F*> Histogram::get_exp_maps(){
    return exp_maps;
}
std::vector<TH2F*> Histogram::get_flx_maps(){
    return flx_maps;
}