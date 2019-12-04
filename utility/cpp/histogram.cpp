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

}




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