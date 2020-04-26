#ifndef _MODEL
#define _MODEL

#include "./datatype.h"

#include "TH1F.h"
#include "TGraph.h"
#include "TF1.h"

class Model {
    private:
        std::string ticket_key;
        std::string generateRandomString(size_t length);
    public:
        Model(SpectrumModel spectrum_model);
        ~Model();
        void computeGammaSpectrum(std::vector<float> _params);
        TGraph* readResult();
        TGraph* readResult(float multiple_x_degree);
};

#endif