#include <stdio.h>
#include <stdlib.h>
#include <string>
#include <vector>
#include <math.h>

#include "../../settings.h"
#include "histogram.h"

void Histogram::assignEnergyBin(float *_energy_mid_bins, float energy_start_gev = float(E_START_GEV), float energy_end_gev = float(E_STOP_GEV)){
    float divider, e2d, e1d, ln;
    float *energy_edge_bins = (float*)malloc((N_E_BINS+1)*sizeof(float));
    for (unsigned int i=0; i <= N_E_BINS; i++){
        energy_edge_bins[i] = energy_start_gev * pow(energy_end_gev/energy_start_gev, float(i)/float(N_E_BINS));
    }
    for (unsigned i=0; i < N_E_BINS; i++){
        divider = 1.0f - float(GAMMA);
        e2d = pow(energy_edge_bins[i+1], divider);
        e1d = pow(energy_edge_bins[i], divider);
        ln = log(0.5f*(e2d - e1d)+ e1d);
        _energy_mid_bins[i] = exp(ln/(divider));
    }
    free(energy_edge_bins);
}