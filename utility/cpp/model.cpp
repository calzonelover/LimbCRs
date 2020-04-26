#include <stdio.h>
#include <stdlib.h>
#include <string>
#include <vector>
#include <sstream>
#include <iostream>
#include <fstream>
#include <math.h>

#include "TH1F.h"
#include "TGraph.h"
#include "TF1.h"

#include "./model.h"
#include "./io.h"
#include "./histogram.h"

Model::Model(SpectrumModel spectrum_model){
    ticket_key = generateRandomString(6);    
    std::string model_name;
    if (spectrum_model == SPL){
        model_name = "SPLwHe";
    } else if (spectrum_model == BPL){
        model_name = "BPLwHe";
    } else {
        std::cout << "About to call function" << std::endl;
        exit(0); 
    }
    char script[100];
    sprintf(script, "gfortran model/%s.f ./model/frag.f -o model/%s.out", model_name.c_str(), ticket_key.c_str());
    system(script);
}

Model::~Model(){
    char script[100];
    sprintf(
        script, "rm -rf model/%s.out model/simdata/%s.csv",
        ticket_key.c_str(), ticket_key.c_str()
    );
    system(script);
}

void Model::computeGammaSpectrum(std::vector<float> _params){
    float norm_all = _params[0], norm = _params[1];
    float gamma1 = _params[2], gamma2 = _params[3];
    float energy_break = _params[4];
    // float norm_all = _params->at(0), norm = _params->at(1);
    // float gamma1 = _params->at(2), gamma2 = _params->at(3);
    // float energy_break = _params->at(4);
    char script[100];
    sprintf(
        script, "./model/%s.out %s.csv %f %f %f %f %f",
        ticket_key.c_str(), ticket_key.c_str(),
        norm_all, norm,
        gamma1, gamma2,
        energy_break
    );
    // std::cout << script << std::endl;
    system(script);
}

TGraph* Model::readResult(){
    float *energy_mid_bins = (float*)malloc(N_E_BINS*sizeof(float));
    float *gamma_ray_fluxs = (float*)malloc((N_E_BINS+1)*sizeof(float));

    std::string _filename = "model/simdata/" + ticket_key + ".csv";
    //
    // char script[100];
    // sprintf(script, "cat %s", _filename.c_str());
    // system(script);
    //
    std::ifstream _file(_filename);
    if (!_file.good()){
        std::cout << "file " << _filename << " does not exist"  << std::endl;
        std::cout << "Program exit!" << std::endl;
        exit(0);
    }

    unsigned int i = 0;
    std::string line;
    float e_gev_i, model_flux_i;
    while (getline(_file, line, '\n')){
        if (!_file.eof()){
            std::istringstream templine(line);
            templine >> energy_mid_bins[i];
            templine >> gamma_ray_fluxs[i];
        }
        i++;
    }
    auto _flux_model = new TGraph(N_E_BINS,energy_mid_bins,gamma_ray_fluxs);
    return _flux_model;
}

TGraph* Model::readResult(float multiple_x_degree){
    float *energy_mid_bins = (float*)malloc(N_E_BINS*sizeof(float));
    float *gamma_ray_fluxs = (float*)malloc((N_E_BINS+1)*sizeof(float));

    std::string _filename = "model/simdata/" + ticket_key + ".csv";
    std::ifstream _file(_filename);
    if (!_file.good()){
        std::cout << "file " << _filename << " does not exist"  << std::endl;
        std::cout << "Program exit!" << std::endl;
        exit(0);
    }

    unsigned int i = 0;
    std::string line;
    float e_gev_i, model_flux_i;
    while (getline(_file, line, '\n')){
        if (!_file.eof()){
            std::istringstream templine(line);
            templine >> energy_mid_bins[i];
            templine >> gamma_ray_fluxs[i];
        }
        i++;
    }
    for (unsigned int i=0; i<N_E_BINS; i++){
        // std::cout << "bin: " << i << ", flux:" << gamma_ray_fluxs[i] \
            << ", flux275: " << pow(energy_mid_bins[i], multiple_x_degree) << std::endl;
        gamma_ray_fluxs[i] *= pow(energy_mid_bins[i], multiple_x_degree);        
    }
    auto _flux_model = new TGraph(N_E_BINS,energy_mid_bins,gamma_ray_fluxs);
    return _flux_model;
}


std::string Model::generateRandomString(size_t length){
  const char* charmap = "ascdefghijklmnopqrstupwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ012345678";
  const size_t charmapLength = strlen(charmap);
  auto generator = [&](){ return charmap[rand()%charmapLength]; };
  std::string result;
  result.reserve(length);
  generate_n(back_inserter(result), length, generator);
  return result;
}