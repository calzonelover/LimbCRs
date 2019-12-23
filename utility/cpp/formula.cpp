#include <stdio.h>
#include <stdlib.h>
#include <string>
#include <vector>
#include <math.h>

#include "../../settings.h"
#include "../../utility/cpp/datatype.h"
#include "../../utility/cpp/transform.h"

#include "./formula.h"

double Formula::energy_to_rigidity(double energy, ParticleType particle_type){
    // particle_type == "p" or "He"
    double rigidity = sqrt( pow(energy + PROTON_MASS, 2.0f) + PROTON_MASS*PROTON_MASS );
    if (particle_type == Helium) rigidity *= 2;
    return rigidity;
}

double Formula::rigidity_to_energy(double rigidity, ParticleType particle_type){
    double charge = 1.0;
    double mass = PROTON_MASS;
    if (particle_type == Helium){
        charge *= 2;
        mass *= 4;
    }
    auto out = sqrt(pow(charge*rigidity, 2.0) + mass*mass) - mass;
    return out;
}

double Formula::spl(double *x, double *par){
    auto energy = x[0];
    auto norm = par[0];
    auto gamma = par[1];

    auto rigidity = energy_to_rigidity(energy);
    auto out = norm * pow(rigidity, -gamma);
    return out;
}

double Formula::bpl(double *x, double *par){
    auto energy = x[0];
    auto rigidity = Formula::energy_to_rigidity(energy); 
    auto norm = par[0];
    auto gamma1 = par[1];
    auto gamma2 = par[2];
    auto rigidity_break = Formula::energy_to_rigidity(par[3]);

    auto norm2 = norm * pow(rigidity_break, gamma2 - gamma1);
    auto out = (rigidity < rigidity_break) ? norm * pow(rigidity, -gamma1) : norm2 * pow(rigidity, -gamma2);
    return out;
}