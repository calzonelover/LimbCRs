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

std::vector<FT1> readPhotonCSV(int _week);
void assignEnergyBin(float *_energy_mid_bins, float energy_start_gev, float energy_end_gev);

// Variables
// std::string cntmap_name, cntmap_title, flxmap_name, flxmap_title;
std::vector<TH2F*> cnt_maps, flx_maps;
float *energy_mid_bins;
#endif