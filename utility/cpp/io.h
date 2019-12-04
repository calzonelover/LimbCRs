#ifndef FILEIO
#define FILEIO

#include "datatype.h"

class FileIO {
    public:
        static std::vector<FT1> readPhotonCSV(int _week, bool skipHeader=true);
        static std::vector<TH2F*> readExposureMap();
};

#endif