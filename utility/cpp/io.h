#ifndef FILEIO
#define FILEIO

#include "TH2F.h"
#include "datatype.h"

class FileIO {
    public:
        static std::string get_current_dir();
        static std::vector<FT1> readPhotonCSV(int _week, bool skipHeader=true);
        static std::vector<TH2F*> readExposureMap();
        static void readDataModel(std::string path, float *energy_mid_bins, float *gamma_ray_fluxes);
};

#endif