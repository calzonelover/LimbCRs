#include <stdio.h>
#include <stdlib.h>
#include <string>
#include <vector>
#include <math.h>

#include "../../settings.h"
#include "../../utility/cpp/datatype.h"
#include "../../utility/cpp/transform.h"

#include "./formula.h"

double Formula::energy_to_rigidity(double energy, ParticleType particle_type = Proton){
    // particle_type == "p" or "He"
    double rigidity = sqrt( pow(energy + PROTON_MASS, 2.0f) + PROTON_MASS*PROTON_MASS );
    if (particle_type == Helium) rigidity *= 2;
    return rigidity;
}

double Formula::rigidity_to_energy(double rigidity, ParticleType particle_type = Proton){
    
}

double Formula::spl(double *x, double *par){
    // par[0] is normalization factor R0
    // par[1] is gamma
    double energy = x[0];
    double norm = par[0];
    double gamma = par[1];

    double rigidity = energy_to_rigidity(energy);
    double out = norm * pow(rigidity, -gamma);
    return out;
}

double Formula::bpl(double *x, double *par){
    // par[0] is normalization factor R0
    // par[1] is gamma
    double energy = x[0];
    double norm = par[0];
    double gamma = par[1];

    double rigidity = energy_to_rigidity(energy);
    double out = norm * pow(rigidity, -gamma);
    return out;
}