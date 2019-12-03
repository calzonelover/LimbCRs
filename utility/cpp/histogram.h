#ifndef HISTOGRAM
#define HISTOGRAM

class Histogram {
    private:
        float *energy_mid_bins;
        std::vector<TH2F*> cnt_maps, exp_maps, flx_maps;
    public:
        Histogram();
        static void assignEnergyBin(float *_energy_mid_bins, float energy_start_gev, float energy_end_gev);
        static void init2DHistogram(std::vector<TH2F*> _cnt_maps, std::vector<TH2F*> _flx_maps, float *_energy_mid_bins);
        static void assignExposureMap(std::vector<TH2F*> _exp_maps);

        float* get_energy_mid_bins();
        std::vector<TH2F*> get_cnt_maps();
        std::vector<TH2F*> get_flx_maps();
};

#endif