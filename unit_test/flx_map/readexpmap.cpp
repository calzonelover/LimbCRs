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
#include "TColor.h"
#include "TPad.h"
#include "TStyle.h"
#include "TH2F.h"
#include "TCanvas.h"

#include "../../utility/cpp/io.h"
#include "../../utility/cpp/parser.h"
#include "../../utility/cpp/histogram.h"
#include "../../utility/cpp/datatype.h"
#include "../../utility/cpp/visualize.h"
#include "../../settings.h"
#include "flxmap.h"

int main(int argc, char** argv){
    auto expmaps = FileIO::readExposureMap();
    int p[4] = {0, 15, 30, 49};
    Visualize::plotMapQuadrant(
        expmaps, p,
        "expmaps", "Exposure Maps",
        "polar_expmaps.png", "SURF2POLZ"
    );
    Visualize::plotMapQuadrant(
        expmaps, p,
        "expmaps", "Exposure Maps",
        "cartesian_expmaps.png", "COLZ"
    );
    return 0;
}