#include <stdio.h>
#include <stdlib.h>
#include <string>
#include <vector>
#include <sstream>
#include <iostream>
#include <fstream>
#include <ctime>
#include <math.h>

// ROOT
#include "TColor.h"
#include "TPad.h"
#include "TStyle.h"
#include "TMath.h"
#include "TF1.h"
#include "TH1F.h"
#include "TH2F.h"
#include "TFile.h"
#include "TCanvas.h"

#include "../../utility/cpp/io.h"
#include "../../utility/cpp/parser.h"
#include "../../utility/cpp/histogram.h"
#include "../../utility/cpp/datatype.h"
#include "../../utility/cpp/formula.h"
#include "../../utility/cpp/visualize.h"
#include "../../utility/cpp/model.h"
#include "../../utility/cpp/optimizer.h"
#include "../../settings.h"
#include "test.h"

int main(int argc, char **argv)
{
    // SpectrumModel spectrum_model = SPL;
    // SPL Loss =  356.605

    TFile *read_file = new TFile("data/root/extracted_data.root", "READ");
    auto histogram = new Histogram();
    histogram->load(read_file);

    std::vector<NADIR_BOUND> nadir_bounds{
        {.phi_lower = 0.0f, .phi_upper = 30.0f, .theta_lower = THETA_E_NAD_MIN, .theta_upper = THETA_E_NAD_MAX},
        {.phi_lower = 150.0f, .phi_upper = 210.0f, .theta_lower = THETA_E_NAD_MIN, .theta_upper = THETA_E_NAD_MAX},
        {.phi_lower = 330.0f, .phi_upper = 360.0f, .theta_lower = THETA_E_NAD_MIN, .theta_upper = THETA_E_NAD_MAX},
    };
    compute_multi_region_flux(histogram, nadir_bounds);

    auto out = Optimizer::optimize(SPL, histogram, Particle_swarm);
    // auto out = Optimizer::optimize(SPL, histogram, Simulated_annealing);

    // SPL: PS
    // N_all: 0.0110524 , N_0: 2.26008 , g1: 2.62515 , g2: 2.65902 , E_b: 322.662
    // Loss: 298.208 , Loss SD: 0.0981467
    // BPL: PS
    // N_all: 0.0110726 , N_0: 4.04837 , g1: 2.90502 , g2: 2.65259 , E_b: 326.956
    // Loss: 297.471 , Loss SD: 0.0653248
    // Sigma = 0.6410 ?

    read_file->Close();
    return 0;
}