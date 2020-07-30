#ifndef HISTOGRAM
#define HISTOGRAM

#include "TFile.h"

#include "../../settings.h"
#include "../../utility/cpp/datatype.h"

class Histogram {
    private:
        float *energy_mid_bins, *energy_edge_bins;
        TH2F *solid_angle_map;
        TH1F *count_hist, *flux_hist; // save & load
        std::vector<TH2F*> cnt_maps, exp_maps, flx_maps; // save & load
    public:
        Histogram(bool is_init=true);
        static void assignEnergyBin(float *_energy_mid_bins, float *_energy_edge_bins, float energy_start_gev = float(E_START_GEV), float energy_end_gev = float(E_STOP_GEV));
        static void assignSolidAngleMap(TH2F *map);        
        static void init2DHistogram(std::vector<TH2F*> &_cnt_maps, std::vector<TH2F*> &_flx_maps, float *_energy_mid_bins);
        static float sumOverRegion(
            TH2F *map,
            float phi_nad_min = PHI_NADIR_MIN, float phi_nad_max = PHI_NADIR_MAX,
            float theta_nad_min = THETA_E_NAD_MIN, float theta_nad_max = THETA_E_NAD_MAX
        );

        static int findBin(float energy, float *_energy_edge_bins);
        void fillPhoton(FT1 photon);
        void computeFlux1(); // WIP
        void computeFlux2(); // WIP

        void save();
        void load(TFile *read_file);

        float* get_energy_mid_bins();
        float* get_energy_edge_bins();
        TH2F* get_solid_angle_map();
        std::vector<TH2F*> get_cnt_maps();
        std::vector<TH2F*> get_exp_maps();
        std::vector<TH2F*> get_flx_maps();

        TH1F* get_cnt_hist();
        TH1F* get_flx_hist();
};

#endif