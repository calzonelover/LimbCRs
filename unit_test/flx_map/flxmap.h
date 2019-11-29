#ifndef FLXMAP
#define FLXMAP

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


// Variables
std::vector<TH2F*> cnt_maps, flx_maps;
float *energy_mid_bins;
#endif