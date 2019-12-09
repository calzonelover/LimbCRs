#ifndef HISTOGRAM
#define HISTOGRAM

#include "../../settings.h"

class Histogram {
    private:
        float *energy_mid_bins, *energy_edge_bins;
        std::vector<TH2F*> cnt_maps, exp_maps, flx_maps;
        TH1F *counts, *fluxes;
    public:
        Histogram();
        static void assignEnergyBin(float *_energy_mid_bins, float *_energy_edge_bins, float energy_start_gev = float(E_START_GEV), float energy_end_gev = float(E_STOP_GEV));
        static void init2DHistogram(std::vector<TH2F*> _cnt_maps, std::vector<TH2F*> _flx_maps, float *_energy_mid_bins);
        static void assignExposureMap(std::vector<TH2F*> _exp_maps);

        int findBin(float energy);
        void fillPhoton(float energy, float theta_nad, float phi_nad);
        void computeFlux(); // WIP

        void save();
        void load();

        float* get_energy_mid_bins();
        float *get_energy_edge_bins();
        std::vector<TH2F*> get_cnt_maps();
        std::vector<TH2F*> get_exp_maps();
        std::vector<TH2F*> get_flx_maps();
};

#endif