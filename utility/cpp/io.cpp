#include <stdio.h>
#include <stdlib.h>
#include <string>
#include <vector>
#include <sstream>
#include <iostream>
#include <fstream>
#include <ctime>
#include <math.h>

#include "TH2F.h"

#include "../../settings.h"

#include "../../utility/cpp/parser.h"
#include "../../utility/cpp/histogram.h"
#include "datatype.h"
#include "io.h"

std::vector<FT1> FileIO::readPhotonCSV(int _week, bool skipHeader){
    std::string week = std::to_string(_week);
    while (week.size() < 3){
        week = "0" + week;
    }

    std::string _filename = std::string(PHOTON_PATH) + "ft1_w" + week + ".csv";
    std::ifstream file(_filename);
    std::vector<FT1> ft1_rows;
    if (!file.good()){
        std::cout << "file " << _filename << " does not exist"  << std::endl;
        std::cout << "Program exit!" << std::endl;
        exit(0);
    }
    
    std::string line;
    int row_i = 0;
    auto row_begin = skipHeader? 1 : 0;
    while (getline(file, line,'\n')){
        if (row_i > row_begin && !file.eof()){
            std::istringstream templine(line);
            std::vector<float> row;
            std::string data;
            while (std::getline(templine, data,','))
            {
                row.push_back(atof(data.c_str()));
            }
            FT1 row_ft1 = {
                .P8R2_SOURCE_V6 = row[1] ? true : false,
                .P8R2_ULTRACLEANVETO_V6 = row[2] ? true : false,
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


std::vector<TH2F*> FileIO::readExposureMap(bool skipHeader){
    std::string line;
    auto energy_mid_bins = (float*)malloc(N_E_BINS*sizeof(float));
    Histogram::assignEnergyBin(energy_mid_bins, E_START_GEV, E_STOP_GEV);

    std::vector<TH2F*> exp_maps;
    for (unsigned int i_energy=0; i_energy<N_E_BINS; i_energy++){
        auto expmap_name = "expmap" + Parser::parseIntOrder(i_energy);
        auto expmap_title = "Exposure map " + Parser::parseDecimal(energy_mid_bins[i_energy], 2) + " GeV";
        exp_maps.push_back(new TH2F(
            expmap_name.c_str(), expmap_title.c_str(),
            N_BINS_PHI_NADIR, PHI_NADIR_MIN, PHI_NADIR_MAX,
            N_BINS_THETA_NADIR, THETA_NADIR_MIN, THETA_NADIR_MAX
        ));

        std::string _filename = "data/exposure_map/w" + std::to_string(WEEK_BEGIN) + "_" + std::to_string(WEEK_END) + "/" + std::string(IRF_NAME) +"/expmap_E" + std::to_string(int(floor(energy_mid_bins[i_energy]))) + ".csv";
        std::ifstream file(_filename);
        if (!file.good()){
            std::cout << "file " << _filename << " does not exist"  << std::endl;
            std::cout << "Program exit!" << std::endl;
            exit(0);
        }
        for (unsigned int i=0; i < N_BINS_PHI_NADIR; i++){
            for (unsigned int j=0; j < N_BINS_THETA_NADIR; j++){
                if (getline(file, line,'\n')){
                    if (!file.eof()){
                        exp_maps[i_energy]->SetBinContent(i, j, std::stof(line));
                    }
                }
            }
        }
        file.close();
    }
    return exp_maps;
}