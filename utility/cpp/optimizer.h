#ifndef _OPTIMIZER
#define _OPTIMIZER

#include "./datatype.h"
#include "./model.h"
#include "./histogram.h"

#include "TH1F.h"

// Simulated Annealing (SA)
#define SA_T 300.0
#define SA_T_DECAY 0.95
#define SA_T_STOP 0.0001
#define SA_N_ACCEPTED_MAX 30

// Particle Swarm Algorithm (PS)
#define PS_N_PARTICLES 40
#define PS_OMEGA 0.2
#define PS_C_LOCAL 0.2
#define PS_C_GLOBAL 0.3
#define PS_STOP_SD_LOSS 0.1


class Optimizer {
    private:
        static std::vector<float>  _pertube_state(std::vector<float> _params, unsigned int _n=1);
        static std::vector<float>  _optimize_simulated_annealing(SpectrumModel _spectrum_model, Histogram *_histogram);

        static float _compute_sd(std::vector<float> _particle_profits);
        static std::vector<float>  _optimize_particle_swarm(SpectrumModel _spectrum_model, Histogram *_histogram);        
    public:
        static std::vector<float> optimize(SpectrumModel _spectrum_model, Histogram *_histogram, OptimizeAlg _optimizedAlg);
        static float loglikelihood(TGraph *_model_flux, Histogram *_histogram);
};

#endif