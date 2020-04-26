#include <ctime>
#include <stdio.h>
#include <stdlib.h>
#include <string>
#include <vector>
#include <math.h>

#include "TH1F.h"
#include "TH2F.h"
#include "TFile.h"
#include "TMath.h"

#include "./datatype.h"
#include "./histogram.h"
#include "./model.h"

#include "optimizer.h"

std::vector<float>  Optimizer::_pertube_state(std::vector<float> _params, unsigned int _n){
    std::srand((unsigned) time(0));
    unsigned int i = 0;
    while (i < _n){
        int n_perturbed_param = std::rand() % _params.size();
        auto _rand = ((float) rand()) / (float) RAND_MAX;
        _params[n_perturbed_param] *= 1.0 + 0.001*(_rand - 0.5);
        // if (n_perturbed_param < 2){
        //     _params[n_perturbed_param] *= 1.0 + 0.001*(_rand - 0.5);
        // } else {
        //     _params[n_perturbed_param] *= 1.0 + 0.0001*(_rand - 0.5);
        // }
        i++;
    }
    return _params;
}

std::vector<float>  Optimizer::_optimize_simulated_annealing(SpectrumModel _spectrum_model, Histogram *_histogram){
    std::vector<float> optimized_params;
    optimized_params.push_back(INI_TOTAL_NORM); optimized_params.push_back(INI_NORM_PL);
    optimized_params.push_back(INI_GAMMA1); optimized_params.push_back(INI_GAMMA2);
    optimized_params.push_back(INI_E_BREAK);
    std::srand((unsigned) time(0));

    Model *InteractionModel = new Model(_spectrum_model);

    float t = float(SA_T); unsigned int n = 0;
    float _sumLoglikelihood, _old_sumLoglikelihood;
    TGraph *flux_model;

    InteractionModel->computeGammaSpectrum(optimized_params);
    flux_model = InteractionModel->readResult();
    _old_sumLoglikelihood = Optimizer::loglikelihood(flux_model, _histogram);
    while (t > SA_T_STOP){
        while (n < SA_N_ACCEPTED_MAX){
            optimized_params = _pertube_state(optimized_params, 1);
            InteractionModel->computeGammaSpectrum(optimized_params);
            flux_model = InteractionModel->readResult();
            _sumLoglikelihood = Optimizer::loglikelihood(flux_model, _histogram);
            // std::cout << "T: " << t << ", Loss: " << _sumLoglikelihood << std::endl;
            auto _diff_energy = _sumLoglikelihood - _old_sumLoglikelihood;
            if (_diff_energy < 0){
                _old_sumLoglikelihood = _sumLoglikelihood;
                n++;
            } else {
                auto prob = TMath::Exp(-_diff_energy/t);
                auto _rand = ((float) rand()) / (float) RAND_MAX;
                if (_rand > prob) n++; 
            }
        }
        t *= SA_T_DECAY;
        n = 0;
        std::cout << "N_all: " << optimized_params[0] << " , N_0: " << optimized_params[1] << " , g1: " << optimized_params[2] << " , g2: " << optimized_params[3] << " , E_b: " << optimized_params[4] << std::endl;;
        std::cout << "T: " << t << ", Loss: " << _sumLoglikelihood << std::endl;
    }
    delete InteractionModel;
    return optimized_params;
}


float Optimizer::_compute_sd(std::vector<float> _particle_profits){
    float mean = 0.0f;
    for (auto _particle_profit : _particle_profits) mean += _particle_profit;
    mean /= float(_particle_profits.size());

    float dv = 0.0f;
    for (auto _particle_profit : _particle_profits){
        dv += (_particle_profit - mean)*(_particle_profit - mean);
    }
    float sd = sqrt(dv/float(_particle_profits.size()));
    return sd;
}

std::vector<float> Optimizer::_optimize_particle_swarm(SpectrumModel _spectrum_model, Histogram *_histogram){
    Model *InteractionModel = new Model(_spectrum_model);
    TGraph *flux_model;

    int _best_local_par_i, _best_global_par_i;
    float _best_local_profit, _best_global_profit;
    std::vector<float> _best_local_params, _best_global_params;
    
    std::vector<float> _particle_profits;
    std::vector<std::vector<float>> _particles;
    std::vector<std::vector<float>> _v0_particles;
    // Initialize particle
    for (unsigned int par_i=0; par_i < PS_N_PARTICLES; par_i++){
        std::vector<float> _particle_i{
            ((float) rand() / (float) RAND_MAX) * ((float) INI_TOTAL_NORM_MAX - (float) INI_TOTAL_NORM_MIN) + (float) INI_TOTAL_NORM_MIN,
            ((float) rand() / (float) RAND_MAX) * ((float) INI_NORM_PL_MAX - (float) INI_NORM_PL_MIN) + (float) INI_NORM_PL_MIN,
            ((float) rand() / (float) RAND_MAX) * ((float) INI_GAMMA1_MAX - (float) INI_GAMMA1_MIN) + (float) INI_GAMMA1_MIN,
            ((float) rand() / (float) RAND_MAX) * ((float) INI_GAMMA2_MAX - (float) INI_GAMMA2_MIN) + (float) INI_GAMMA2_MIN,
            ((float) rand() / (float) RAND_MAX) * ((float) INI_E_BREAK_MAX - (float) INI_E_BREAK_MIN) + (float) INI_E_BREAK_MIN
        };
        _particles.push_back(_particle_i);

        InteractionModel->computeGammaSpectrum(_particle_i);
        flux_model = InteractionModel->readResult();
        _particle_profits.push_back(-loglikelihood(flux_model, _histogram));
    }
    _best_local_par_i = std::max_element(_particle_profits.begin(),_particle_profits.end()) - _particle_profits.begin();
    _best_global_par_i = std::max_element(_particle_profits.begin(),_particle_profits.end()) - _particle_profits.begin();
    _best_local_profit = _particle_profits[_best_local_par_i];
    _best_global_profit = _particle_profits[_best_global_par_i];
    _best_local_params = _particles[_best_local_par_i];
    _best_global_params = _particles[_best_global_par_i];
    // compute
    for (unsigned int par_i=0; par_i < PS_N_PARTICLES; par_i++){
        std::vector<float> _dummy_v0;
        for (unsigned int feature_i=0; feature_i < _particles[0].size(); feature_i++){
            _dummy_v0.push_back(0.0f);
        }
        _v0_particles.push_back(_dummy_v0);
    }
    while (_compute_sd(_particle_profits) > PS_STOP_SD_LOSS){
        for (unsigned int par_i=0; par_i < PS_N_PARTICLES; par_i++){
            std::vector<float> _v1_particle;
            auto _coef_local_rand = ((float) rand()) / (float) RAND_MAX;
            auto _coef_global_rand = ((float) rand()) / (float) RAND_MAX;
            for (unsigned int feature_i=0; feature_i < _particles[0].size(); feature_i++){
                _v1_particle.push_back(
                    PS_OMEGA*_v0_particles[par_i][feature_i]
                    + ( PS_C_LOCAL * _coef_local_rand * ( _best_local_params[feature_i] - _particles[par_i][feature_i] ))
                    + ( PS_C_GLOBAL * _coef_global_rand * ( _best_global_params[feature_i] - _particles[par_i][feature_i] ))
                );
            }
            for (unsigned int feature_i=0; feature_i < _particles[0].size(); feature_i++){
                _particles[par_i][feature_i] += _v1_particle[feature_i];
            }
            _v0_particles[par_i] = _v1_particle;

            InteractionModel->computeGammaSpectrum(_particles[par_i]);
            flux_model = InteractionModel->readResult();
            _particle_profits[par_i] = -loglikelihood(flux_model, _histogram);
        }
        // find best
        for (unsigned int par_i=0; par_i < PS_N_PARTICLES; par_i++){
            _best_local_par_i = std::max_element(_particle_profits.begin(),_particle_profits.end()) - _particle_profits.begin();
            _best_global_par_i = std::max_element(_particle_profits.begin(),_particle_profits.end()) - _particle_profits.begin();
            _best_local_profit = _particle_profits[_best_local_par_i];
            _best_global_profit = _particle_profits[_best_global_par_i];
            _best_local_params = _particles[_best_local_par_i];
            _best_global_params = _particles[_best_global_par_i];
        }
        std::cout << "N_all: " << _best_global_params[0] << " , N_0: " << _best_global_params[1] << " , g1: " << _best_global_params[2] << " , g2: " << _best_global_params[3] << " , E_b: " << _best_global_params[4] << std::endl;;
        std::cout << "Loss: " << -_best_global_profit << " , Loss SD: " << _compute_sd(_particle_profits) << std::endl;
    }
    return _best_global_params;
}

std::vector<float> Optimizer::optimize(SpectrumModel _spectrum_model, Histogram *_histogram, OptimizeAlg _optimizedAlg){
    std::vector<float> _optimized_params;
    if (_optimizedAlg == Simulated_annealing){
        _optimized_params = _optimize_simulated_annealing(_spectrum_model, _histogram);
    } else if (_optimizedAlg == Particle_swarm){
        _optimized_params = _optimize_particle_swarm(_spectrum_model, _histogram);
    }else {
        std::cout << "Optimized mode : " << _optimizedAlg << " does not support !" << std::endl;
        exit(0);
    }
    return _optimized_params;
}

float Optimizer::loglikelihood(TGraph *_model_flux, Histogram *_histogram){
    unsigned int n_bins = _histogram->get_cnt_hist()->GetNbinsX();
    auto _get_energy_mid_bins = _histogram->get_energy_mid_bins();

    auto _obs_cnt_hist = _histogram->get_cnt_hist();
    auto _obs_flx_hist = _histogram->get_flx_hist();
    auto _exp_hist = (TH1F*) _obs_cnt_hist->Clone();
    _exp_hist->Divide(_obs_flx_hist);

    float sumLoglikelihood = 0.0f;
    unsigned int model_count_i;
    for (unsigned int i=0; i<n_bins; i++){
        auto model_flux_i = _model_flux->Eval(_get_energy_mid_bins[i], 0, "S");
        model_count_i = int(round(model_flux_i * _exp_hist->GetBinContent(i+1)));
        auto sumLoglikelihood_i = TMath::Poisson(model_count_i, _obs_cnt_hist->GetBinContent(i+1));
        if (sumLoglikelihood_i == 0){
            sumLoglikelihood += 308.0f;
        } else {
            sumLoglikelihood += -TMath::Log(sumLoglikelihood_i);
        }
        // std::cout << i+1 << "flx , "<< _obs_flx_hist->GetBinContent(i+1) << ", "<< model_flux_i << std::endl;
        // std::cout << i+1 << "cnt , "<< _obs_cnt_hist->GetBinContent(i+1) << ", "<< model_count_i << std::endl;
    }
    // std::cout << sumLoglikelihood << std::endl;
    return sumLoglikelihood;
}