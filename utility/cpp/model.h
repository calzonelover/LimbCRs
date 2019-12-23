#ifndef _MODEL
#define _MODEL

#include "./datatype.h"

class Model {
    public:
        static void init(SpectrumModel spectrum_model);
        static void computeGammaSpectrum(
            SpectrumModel spectrum_model
            float norm, float gamma1,
            float gamma2, float energy_break
        );
        static void 
};

#endif