#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include <vector>
#include <math.h>

// ROOT
#include "TColor.h"
#include "TPad.h"
#include "TStyle.h"
#include "TH2F.h"
#include "TCanvas.h"

#include "../../settings.h"

#include "../../utility/cpp/parser.h"
#include "../../utility/cpp/histogram.h"
#include "datatype.h"
#include "visualize.h"

float Visualize::lbOS = -0.13; // Z-axis label offset
float Visualize::lbS = 0.05;   // Z-axis label size
float Visualize::ttOS = 0.5;   // Z-axis tltle offset
float Visualize::ttS = 0.04;   // Z-axis tltle 
ColorPalatte Visualize::palette = kRainbow;
int Visualize::fixTheta = -90;
int Visualize::fixPhi = -90;


void Visualize::plotHist(
    TH1F *hist,
    std::string hist_name, std::string hist_title,
    std::string file_name, std::string plot_mode,
    std::string y_label
    ){
    char _hist_name[hist_name.size()+1], _hist_title[hist_title.size()+1];
    char _file_name[file_name.size()+1], _plot_mode[plot_mode.size()+1];
    char _y_label[y_label.size()+1];
    strcpy(_hist_name, hist_name.c_str()); strcpy(_hist_title, hist_title.c_str()); 
    strcpy(_file_name, file_name.c_str()); strcpy(_plot_mode, plot_mode.c_str()); 
    strcpy(_y_label, y_label.c_str());
    auto c = new TCanvas(_hist_name, _hist_name, 900, 900);
}

void Visualize::plotMapQuadrant(
        std::vector<TH2F*> maps, int *selected_indices,
        std::string map_name, std::string map_title,
        std::string file_name, std::string plot_mode,
        std::string z_label
    ){
    char _map_name[map_name.size()+1], _map_title[map_title.size()+1];
    char _file_name[file_name.size()+1], _plot_mode[plot_mode.size()+1];
    char _z_label[z_label.size()+1];
    strcpy(_map_name, map_name.c_str()); strcpy(_map_title, map_title.c_str()); 
    strcpy(_file_name, file_name.c_str()); strcpy(_plot_mode, plot_mode.c_str()); 
    strcpy(_z_label, z_label.c_str());

    auto c = new TCanvas(_map_name, _map_name, 900, 900);
    c->Divide(2,2);
    gStyle->SetPalette(palette);
    for (unsigned int i=1; i<=4; i++){
        auto j = selected_indices[i - 1];
        c->cd(i);
        maps[j]->SetStats(0);
        gPad->SetTheta(-90);
        gPad->SetPhi(-90);
        maps[j]->Draw(_plot_mode);
        maps[j]->GetXaxis()->SetTitle("#phi (degree)");
        maps[j]->GetYaxis()->SetTitle("#theta_{nadir} (degree)");
        maps[j]->GetYaxis()->SetRangeUser(THETA_NADIR_MIN, THETA_NADIR_MAX);
        maps[j]->GetZaxis()->SetLabelOffset(lbOS);
        maps[j]->GetZaxis()->SetLabelSize(lbS);
        maps[j]->GetZaxis()->SetTitleOffset(ttOS);
        maps[j]->GetZaxis()->SetTitleSize(ttS);
        maps[j]->GetZaxis()->SetTitle(_z_label);
        c->cd(i)->SetLogz();
    }
    c->cd();
    c->SaveAs(_file_name);
}