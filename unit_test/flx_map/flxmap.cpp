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
    
    auto histogram = new Histogram(false);
    auto bla = histogram->get_energy_mid_bins();
    for (unsigned int i=0; i<50;i++) std::cout << Parser::parseDecimal(bla[i], 3) << std::endl;

    for (unsigned int week=WEEK_BEGIN; week <= WEEK_END; week++){
        std::vector<FT1> ft1_rows = FileIO::readPhotonCSV(week);
        std::cout << "# of week: " << week << " FT1 = " << ft1_rows.size() << std::endl;
        for (auto ft1_row : ft1_rows){
            histogram->fillPhoton(ft1_row.energy_gev, ft1_row.nadir, ft1_row.phi_earth);
            // std::cout << ft1_row.P8R2_SOURCE_V6 << ", " << ft1_row.P8R2_ULTRACLEANVETO_V6 << ", " << ft1_row.energy_gev << std::endl;
        }
    }
    histogram->computeFlux2();
    histogram->save();
    return 0;
}