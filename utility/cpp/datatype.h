#ifndef DATATYPE
#define DATATYPE

enum ColorPalatte {
    kRainbow = 55,
};

enum SpectrumModel {
    SPL,
    BPL
};

enum ParticleType {
    Proton,
    Helium
};

enum OptimizeAlg {
    Simulated_annealing,
    Particle_swarm 
};

typedef struct FT1 {
    bool P8R2_SOURCE_V6;
    bool P8R2_ULTRACLEANVETO_V6;
    float altitude_km;
    float energy_gev;
    float nadir;
    float phi_earth;
    float phi_lat;
    float rocking_angle;
    float shifted_nadir;
    float shifted_zenith;
    float theta_lat;
    float time;
    float zenith;
} FT1;

typedef struct Flux {
    float *energy_geb;
    float *flux;
} Flux;

#endif