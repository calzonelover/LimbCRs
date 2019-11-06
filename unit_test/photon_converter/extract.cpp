#include <stdio.h>
#include <stdlib.h>
#include <string>
#include <vector>
#include <sstream>
#include <iostream>
#include <fstream>
#include <ctime>
#include <math.h>

#include <TFITS.h>
#include <TFile.h>
#include <TTree.h>
// #include "/work/jab/Downloads/cfitsio-3.47/include/fitsio.h"

int main(){
    TFITSHDU *f = new TFITSHDU("/work/bus/Data/Photon/lat_photon_weekly_w546_p302_v001.fits");

    std::cout << "hi" << std::endl;
}