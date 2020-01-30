#include <stdio.h>
#include <stdlib.h>
#include <string>
#include <vector>
#include <sstream>
#include <iostream>
#include <fstream>
#include <math.h>


#include "./model.h"
#include "./io.h"

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
    sprintf(script, "rm model/%s.out", ticket_key.c_str());
    system(script);
}

void Model::computeGammaSpectrum(
        float norm, float gamma1,
        float gamma2, float energy_break
    ){
    char script[100];
    sprintf(
        script, "./model/%s.out %s.csv %f %f %f %f",
        ticket_key.c_str(), "bla",
        norm,
        gamma1, gamma2,
        energy_break
    );
    std::cout << script << std::endl;
    system(script);
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