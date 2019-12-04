#ifndef DATATYPE
#define DATATYPE

enum ColorPalatte {
    kRainbow = 55,
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

#endif