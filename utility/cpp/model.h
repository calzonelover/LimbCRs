#ifndef _MODEL
#define _MODEL

#include "./datatype.h"

class Model {
    private:
        std::string ticket_key;
        std::string generateRandomString(size_t length);
    public:
        Model(SpectrumModel spectrum_model);
        ~Model();
        void computeGammaSpectrum(
            float norm, float gamma1,
            float gamma2, float energy_break
        );
        // std::vector<float> readResult();
};

#endif