#ifndef _MODEL
#define _MODEL

#include "./datatype.h"

class Model {
    public:
        void init(SpectrumModel spectrum_model);
        static void computeGammaSpectrum(
            SpectrumModel spectrum_model,
            float norm, float gamma1,
            float gamma2, float energy_break
        );
        static std::string generate(int length);
};

#endif