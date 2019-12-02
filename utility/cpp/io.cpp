#include <stdio.h>
#include <stdlib.h>
#include <string>
#include <vector>
#include <sstream>
#include <iostream>
#include <fstream>
#include <ctime>
#include <math.h>

#include "../../settings.h"

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