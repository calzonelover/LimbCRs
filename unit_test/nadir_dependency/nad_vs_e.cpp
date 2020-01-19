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

int main(int argc, char** argv){
    float *_energy_mid_bins, float *_energy_edge_bins;
    energy_mid_bins = (float*)malloc(N_E_BINS*sizeof(float));
    energy_edge_bins = (float*)malloc((N_E_BINS+1)*sizeof(float));
    Histogram::assignEnergyBin(energy_mid_bins, energy_edge_bins);

    for (unsigned int week=WEEK_BEGIN; week <= WEEK_END; week++){
        std::vector<FT1> ft1_rows = FileIO::readPhotonCSV(week);
        std::cout << "# of week: " << week << " FT1 = " << ft1_rows.size() << std::endl;
        for (auto ft1_row : ft1_rows){
            
        }
    } 
    return 0;
}