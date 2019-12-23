#ifndef VISUALIZE
#define VISUALIZE

#include "datatype.h"


class Visualize{
    public:
        static float lbOS; // Z-axis label offset
        static float lbS;   // Z-axis label size
        static float ttOS;   // Z-axis tltle offset
        static float ttS;   // Z-axis tltle 
        static ColorPalatte palette;
        static int fixTheta;
        static int fixPhi;

        static void plotHist(
            TH1F *hist,
            std::string hist_name, std::string hist_title,
            std::string file_name, std::string plot_mode,
            std::string y_label
        );

        static void plot2DHist(
            TH2F* maps,
            std::string map_name, std::string map_title,
            std::string file_name, std::string plot_mode,
            std::string z_label, bool is_z_log = true
        );

        static void plotMapQuadrant(
            std::vector<TH2F*> maps, int *selected_indices,
            std::string map_name, std::string map_title,
            std::string file_name, std::string plot_mode,
            std::string z_label = "Exposure (m^{2}s)"
        );
};

#endif