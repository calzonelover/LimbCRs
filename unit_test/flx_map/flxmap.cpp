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

int main(int argc, char** argv){
    auto histogram = new Histogram(true);
    auto bla = histogram->get_energy_mid_bins();
    // for (unsigned int i=0; i<50;i++) std::cout << Parser::parseDecimal(bla[i], 3) << std::endl;

    for (unsigned int week=WEEK_BEGIN; week <= WEEK_END; week++){
        std::vector<FT1> ft1_rows = FileIO::readPhotonCSV(week);
        std::cout << "# of week: " << week << " FT1 = " << ft1_rows.size() << std::endl;
        for (auto photon : ft1_rows){
            if (
                photon.P8R2_ULTRACLEANVETO_V6 && photon.energy_gev > E_START_GEV && photon.energy_gev < E_STOP_GEV
                && photon.theta_lat < THETA_LAT_CUTOFF
            ){
                histogram->fillPhoton(photon);
            }
        }
    }
    histogram->computeFlux2();
    histogram->save();
    return 0;
}