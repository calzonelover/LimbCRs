#ifndef _FORMULA
#define _FORMULA

#include "datatype.h"

class Formula {
    public:
        static double energy_to_rigidity(double energy, ParticleType particle_type = Proton);
        static double rigidity_to_energy(double rigidity, ParticleType particle_type = Proton);
        static double spl(double *x, double *par);
        static double bpl(double *x, double *par);
};

#endif