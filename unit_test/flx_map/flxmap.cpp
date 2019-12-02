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
# include "TH2F.h"

#include "../../settings.h"
#include "flxmap.h"


std::string parseIntOrder(int _week, int range=3){
    std::string week = std::to_string(_week);
    while (week.size() < range){
        week = "0" + week;
    }
    return week;
}

template <class T>
std::string parseDecimal(T val, int order){
    std::string val_str = std::to_string(val);
    return val_str.substr(0, val_str.find(".")+order+1);
}

void init2DHistogram(std::vector<TH2F*> cnt_maps, std::vector<TH2F*> flx_maps){
    for (unsigned int i_energy_bin=0; i_energy_bin < N_E_BINS; i_energy_bin++){
        auto cntmap_name = "cntmap" + parseIntOrder(i_energy_bin);
        auto cntmap_title = "Count map " + parseDecimal(energy_mid_bins[i_energy_bin], 2) + " GeV";
        // std::cout << cntmap_name << "\t" << cntmap_title << std::endl;
        cnt_maps.push_back(new TH2F(
            cntmap_name.c_str(), cntmap_title.c_str(),
            N_BINS_PHI_NADIR, PHI_NADIR_MIN, PHI_NADIR_MAX,
            N_BINS_THETA_NADIR, THETA_NADIR_MIN, THETA_NADIR_MAX
        ));
        auto flxmap_name = "flxmap" + parseIntOrder(i_energy_bin);
        auto flxmap_title = "Flux map " + parseDecimal(energy_mid_bins[i_energy_bin], 2) + " GeV";
        // std::cout << flxmap_name << "\t" << flxmap_title << std::endl;
        flx_maps.push_back(new TH2F(
            flxmap_name.c_str(), flxmap_title.c_str(),
            N_BINS_PHI_NADIR, PHI_NADIR_MIN, PHI_NADIR_MAX,
            N_BINS_THETA_NADIR, THETA_NADIR_MIN, THETA_NADIR_MAX
        ));
    }
}

int main(int argc, char** argv){
    energy_mid_bins = (float*)malloc(N_E_BINS*sizeof(float));
    assignEnergyBin(energy_mid_bins, E_START_GEV, E_STOP_GEV);

    init2DHistogram(cnt_maps, flx_maps);


    // for (unsigned int week=WEEK_BEGIN; week <= WEEK_END; week++){
    //     std::vector<FT1> ft1_rows = readPhotonCSV(week);
    //     std::cout << "# of week: " << week << " FT1 = " << ft1_rows.size() << std::endl;
    // }

    // TH2F *H_ADC = new TH2F("H_ADC","RawA vs RawB",100,0.,1000.,100,0.,1000.);
    return 0;
}


// Function

void assignEnergyBin(float *_energy_mid_bins, float energy_start_gev = float(E_START_GEV), float energy_end_gev = float(E_STOP_GEV)){
    float divider, e2d, e1d, ln;
    float *energy_edge_bins = (float*)malloc((N_E_BINS+1)*sizeof(float));
    for (unsigned int i=0; i <= N_E_BINS; i++){
        energy_edge_bins[i] = energy_start_gev * pow(energy_end_gev/energy_start_gev, float(i)/float(N_E_BINS));
    }
    for (unsigned i=0; i < N_E_BINS; i++){
        divider = 1.0f - float(GAMMA);
        e2d = pow(energy_edge_bins[i+1], divider);
        e1d = pow(energy_edge_bins[i], divider);
        ln = log(0.5f*(e2d - e1d)+ e1d);
        _energy_mid_bins[i] = exp(ln/(divider));
    }
    free(energy_edge_bins);
}

std::vector<FT1> readPhotonCSV(int _week){
    std::string week = std::to_string(_week);
    while (week.size() < 3){
        week = "0" + week;
    }


    std::string _filename = "../../" + std::string(PHOTON_PATH) + "ft1_w" + week + ".csv";
    std::ifstream file(_filename);
    std::vector<FT1> ft1_rows;
    if (!file.good()){
        std::cout << "file " << _filename << " does not exist"  << std::endl;
        std::cout << "Program exit!" << std::endl;
        exit(0);
    }
    
    std::string line;
    int row_i = 0;
    while (getline(file, line,'\n'))
	{
    if (row_i > 0 && !file.eof()){
        std::istringstream templine(line);
        std::vector<float> row;
        std::string data;
        while (std::getline(templine, data,','))
        {
            row.push_back(atof(data.c_str()));
        }
        FT1 row_ft1 = {
            .P8R2_SOURCE_V6 = row[1],
            .P8R2_ULTRACLEANVETO_V6 = row[2],
            .altitude_km = row[3],
            .energy_gev = row[4],
            .nadir = row[5],
            .phi_earth = row[6],
            .phi_lat = row[7],
            .rocking_angle = row[8],
            .shifted_nadir = row[9],
            .shifted_zenith = row[10],
            .theta_lat = row[11],
            .time = row[12],
            .zenith = row[13],
        };
        ft1_rows.push_back(row_ft1);
    }
    row_i++;
	}
    file.close();
    return ft1_rows;
}