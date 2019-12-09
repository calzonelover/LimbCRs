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
#include "../../utility/cpp/transform.h"

#include "histogram.h"

Histogram::Histogram(bool is_load){
    energy_mid_bins = (float*)malloc(N_E_BINS*sizeof(float));
    energy_edge_bins = (float*)malloc((N_E_BINS+1)*sizeof(float));
    Histogram::assignEnergyBin(energy_mid_bins, energy_edge_bins);
    count_hist = new TH1F("count_hist", "Count", N_E_BINS, energy_edge_bins);
    flux_hist = new TH1F("flux_hist", "Flux", N_E_BINS, energy_edge_bins);
    Histogram::assignSolidAngleMap(solid_angle_map);
    Histogram::init2DHistogram(cnt_maps, flx_maps, energy_mid_bins);
    Histogram::assignExposureMap(exp_maps);
    if (is_load) this->load();
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

void Histogram::assignSolidAngleMap(TH2F *map){
    map = new TH2F(
        "solid_angle_map", "Solid Angle Map",
        N_BINS_PHI_NADIR, PHI_NADIR_MIN, PHI_NADIR_MAX,
        N_BINS_THETA_NADIR, THETA_NADIR_MIN, THETA_NADIR_MAX    
    );
    auto d_phi = (PHI_NADIR_MAX - PHI_NADIR_MIN)/N_BINS_PHI_NADIR;
    auto d_theta = (THETA_NADIR_MAX - THETA_NADIR_MIN)/N_BINS_THETA_NADIR;
    for (unsigned int i=1; i <= N_BINS_PHI_NADIR; i++){
        for (unsigned int j=1; j <= N_BINS_THETA_NADIR; j++){
            auto phi_nadir_min = i*d_phi;
            auto phi_nadir_max = phi_nadir_min + d_phi;
            auto theta_nadir_min = j*d_theta;
            auto theta_nadir_max = theta_nadir_min + d_phi;
            map->SetBinContent(
                i, j,
                Transform::getSolidAngle(
                    theta_nadir_min, theta_nadir_max,
                    phi_nadir_min, phi_nadir_max
                )
            );
        }
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

float Histogram::sumOverRegion(TH2F *map, float theta_nad_min, float theta_nad_max, float phi_nad_min, float phi_nad_max){
    auto d_phi = (PHI_NADIR_MAX - PHI_NADIR_MIN)/N_BINS_PHI_NADIR;
    auto d_theta = (THETA_NADIR_MAX - THETA_NADIR_MIN)/N_BINS_THETA_NADIR;

    auto sum = 0.0f;
    auto i_min = int(floor(PHI_NADIR_MIN/d_phi));
    auto i_max = (floor(PHI_NADIR_MAX/d_phi) > PHI_NADIR_MAX/d_phi) ? int(floor(PHI_NADIR_MAX/d_phi)) + 1 : int(floor(PHI_NADIR_MAX/d_phi));
    auto j_min = int(floor(THETA_NADIR_MIN/d_theta));
    auto j_max = (floor(THETA_NADIR_MAX/d_theta) > THETA_NADIR_MAX/d_theta) ? int(floor(THETA_NADIR_MAX/d_theta)) + 1 : int(floor(THETA_NADIR_MAX/d_theta));

    for (unsigned int i=i_min+1; i <= i_max; i++){
        for (unsigned int j=j_min+1; j <= j_max; j++){
            sum += map->GetBinContent(i, j);
        }
    }
    return sum;
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
    count_hist->Fill(energy);
}

void Histogram::computeFlux1(){
    for (unsigned int i_energy_bin=0; i_energy_bin<N_E_BINS; i_energy_bin++){
        flx_maps[i_energy_bin] = (TH2F*) cnt_maps[i_energy_bin]->Clone();
        flx_maps[i_energy_bin]->Divide(exp_maps[i_energy_bin]);
        // count hist
        count_hist->SetBinError(i_energy_bin+1, sqrt(count_hist->GetBinContent(i_energy_bin+1)));
        // For flux hist
        auto expSolidMap = (TH2F*) exp_maps[i_energy_bin]->Clone();
        expSolidMap->Multiply(solid_angle_map);
        auto expSolidMap_val_i = Histogram::sumOverRegion(expSolidMap);
        auto dE = energy_edge_bins[i_energy_bin+1] - energy_edge_bins[i_energy_bin];
        flux_hist->SetBinContent(
            i_energy_bin+1,
            count_hist->GetBinContent(i_energy_bin+1)/(expSolidMap_val_i * dE)
        );
        flux_hist->SetBinError(
            i_energy_bin+1,
            sqrt(count_hist->GetBinContent(i_energy_bin+1)) * flux_hist->GetBinContent(i_energy_bin+1)
        );
    }
}

void Histogram::computeFlux2(){
    for (unsigned int i_energy_bin=0; i_energy_bin<N_E_BINS; i_energy_bin++){
        flx_maps[i_energy_bin] = (TH2F*) cnt_maps[i_energy_bin]->Clone();
        flx_maps[i_energy_bin]->Divide(exp_maps[i_energy_bin]);
        // count hist
        count_hist->SetBinError(i_energy_bin+1, sqrt(count_hist->GetBinContent(i_energy_bin+1)));
        // For flux hist
        auto flxmap_val_i = Histogram::sumOverRegion(flx_maps[i_energy_bin]);
        auto solid_angle = Transform::getSolidAngle();
        auto dE = energy_edge_bins[i_energy_bin+1] - energy_edge_bins[i_energy_bin];
        flux_hist->SetBinContent(
            i_energy_bin+1,
            flxmap_val_i/(solid_angle * dE)
        );
        flux_hist->SetBinError(
            i_energy_bin+1,
            sqrt(count_hist->GetBinContent(i_energy_bin+1)) * flux_hist->GetBinContent(i_energy_bin+1)
        );
    }
}


void Histogram::save(){
    TFile out_file("data/root/extracted_data.root","RECREATE");
    for (unsigned int i=0; i<N_E_BINS; i++){
        cnt_maps[i]->Write();
        exp_maps[i]->Write();
        flx_maps[i]->Write();
    }
    count_hist->Write();
    flux_hist->Write();
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
    read_file.GetObject("count_hist", count_hist);
    read_file.GetObject("flux_hist", flux_hist);
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