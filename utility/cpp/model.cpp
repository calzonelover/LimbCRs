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

void Model::init(SpectrumModel spectrum_model){
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
    sprintf(script, "gfortran model/%s.f model/frag.f -o model/%s.out", model_name.c_str(), model_name.c_str());
    system(script);
}

void Model::computeGammaSpectrum(
        SpectrumModel spectrum_model
        float norm, float gamma1,
        float gamma2, float energy_break
    ){
        /*
        RunFlux='./test1.out %f %f %f %f %f'%(A,gamma1,gamma2,Ebreak,normAll)
    	os.system(RunFlux)
        */
}