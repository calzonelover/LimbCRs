#include <stdio.h>
#include <stdlib.h>
#include <string>
#include <vector>
#include <sstream>
#include <iostream>
#include <fstream>
#include <ctime>
#include <math.h>

// ROOT
#include "TColor.h"
#include "TPad.h"
#include "TLatex.h"
#include "TStyle.h"
#include "TMath.h"
#include "TF1.h"
#include "TH1F.h"
#include "TH2F.h"
#include "TFile.h"
#include "TCanvas.h"


#include "../../utility/cpp/io.h"
#include "../../utility/cpp/parser.h"
#include "../../utility/cpp/histogram.h"
#include "../../utility/cpp/datatype.h"
#include "../../utility/cpp/formula.h"
#include "../../utility/cpp/visualize.h"
#include "../../utility/cpp/model.h"
#include "../../utility/cpp/optimizer.h"
#include "../../settings.h"


std::vector<std::vector<float>> read_other_instrument_data(std::string instrument){
    std::string path = "data/static";
    if (instrument == "AMS"){
        path += "/AMS_data.dat";
    } else if (instrument == "PAMELA") {
        path += "/PAMELA_data.dat";
    } else {
        std::cout << "Instrument name: " << instrument << " does not exists in the static data !" << std::endl;
        exit(0);
    }
    std::ifstream file(path);
    if (!file.good()){
        std::cout << "file " << path << " does not exist"  << std::endl;
        std::cout << "Program exit!" << std::endl;
        exit(0);
    }
    std::vector<std::vector<float>> _measured_data;
    std::vector<float> energyEdgeBins, binFluxs, statErrs, sysErrs;

    std::string line;
    int row_i = 0;
    while (getline(file, line,'\n')){
        if (!file.eof()){
            std::istringstream templine(line);
            std::vector<float> row;
            std::string data;
            while (std::getline(templine, data, ' ')){
                row.push_back(atof(data.c_str()));
            }
            energyEdgeBins.push_back(row[0]);
            binFluxs.push_back(row[1]);
            statErrs.push_back(row[2]);
            sysErrs.push_back(row[3]);
            // std::cout << row[0] << " " << row[1] << " " << row[2] << " " << row[3] << std::endl;
        }
        row_i++;
    }
    binFluxs.pop_back();
    statErrs.pop_back();
    sysErrs.pop_back();

    _measured_data.push_back(energyEdgeBins);
    _measured_data.push_back(binFluxs);
    _measured_data.push_back(statErrs);
    _measured_data.push_back(sysErrs);

    // float *_energyEdgeBins = (float*)malloc(N_E_BINS*sizeof(energyEdgeBins.size()));
    // float *_binFluxs = (float*)malloc(N_E_BINS*sizeof(binFluxs.size()));
    // float *_statErrs = (float*)malloc(N_E_BINS*sizeof(statErrs.size()));
    // float *_sysErrs = (float*)malloc(N_E_BINS*sizeof(sysErrs.size()));
    // _measured_data.push_back(_energyEdgeBins);
    // _measured_data.push_back(_binFluxs);
    // _measured_data.push_back(_statErrs);
    // _measured_data.push_back(_sysErrs);
    return _measured_data;
}


int main(int argc, char** argv){
    /// settings
    auto multiplicative = 2.75f;
    float min_x_plot = 8;
    float max_x_plot = 40000;
    // AMS
    int AMS_MarkerColor = 8;
    int AMS_MarkerStyle = 20;
    // PAMELA
    int PAMELA_MarkerColor = 38;
    int PAMELA_MarkerStyle = 22;
    // model
    int Model_LineColor = 2;
    int Model_LineStyle = 1;
    int Model_LineWidth = 3;

    TF1 *spl = new TF1("SinglePowerLaw", Formula::spl, 60, 2000, 2);
    spl->SetParameter(0, 2.82851);
    spl->FixParameter(1, 2.70266 - multiplicative);

    TF1 *bpl = new TF1("BrokenPowerLaw", Formula::bpl, 60, 2000, 4);
    bpl->SetParameter(0, 1.98848);
    bpl->FixParameter(1, 2.86015 - multiplicative);
    bpl->FixParameter(2, 2.63161 - multiplicative);
    bpl->FixParameter(3, 333.115);

    auto ams_data = read_other_instrument_data("AMS");
    auto pamela_data = read_other_instrument_data("PAMELA");
    
    // auto _n_bins_ams = sizeof(ams_data[0])/sizeof(float);
    // auto _n_bins_pamela = sizeof(pamela_data[0])/sizeof(float);
    // std::cout << _n_bins_ams << ", " << _n_bins_pamela << std::endl;
    // auto ams_flux = new TH1F("ams_flux", "AMS-02", _n_bins_ams, ams_data[0]);
    // auto pamela_flux = new TH1F("flux_hist", "PAMELA", _n_bins_pamela, pamela_data[0]);

    float _ams_energy_edge_bins[ams_data[0].size()];
    std::copy(ams_data[0].begin(), ams_data[0].end(), _ams_energy_edge_bins);
    float _pamela_energy_edge_bins[pamela_data[0].size()];
    std::copy(pamela_data[0].begin(), pamela_data[0].end(), _pamela_energy_edge_bins);    

    std::cout << ams_data[0].size() << ", " <<  pamela_data[0].size() << std::endl;
    auto ams_flux = new TH1F("ams_flux", "AMS-02 (2015)", ams_data[1].size(), _ams_energy_edge_bins);
    auto pamela_flux = new TH1F("flux_hist", "PAMELA (2011)", pamela_data[1].size() , _pamela_energy_edge_bins);
    

    for (unsigned int i=0; i<pamela_data[1].size() ; i++){
        auto emul = pow(0.5*(ams_data[0][i] + ams_data[0][i+1]), multiplicative);
        ams_flux->SetBinContent(i + 1, ams_data[1][i] * emul);
        ams_flux->SetBinError(i + 1, ams_data[2][i] * emul);
    }
    for (unsigned int i=0; i<pamela_data[1].size(); i++){
        auto emul = pow(0.5*(pamela_data[0][i] + pamela_data[0][i+1]), multiplicative);
        pamela_flux->SetBinContent(i + 1, pamela_data[1][i] * emul);
        pamela_flux->SetBinError(i + 1, pamela_data[2][i] * emul);
    }

    auto _cloned_ams_flux = (TH1F*) ams_flux->Clone();
    _cloned_ams_flux->Fit("SinglePowerLaw", "", "", 100, 2000);
    _cloned_ams_flux->Fit("BrokenPowerLaw", "", "", 100, 2000);

    // visualize
    auto c = new TCanvas("model_obs_spl", "model_obs_spl", 900, 700);
    c->Range(0,0,1,1);
    c->Divide(1,2,0,0);
    // c->GetPad(1)->SetRightMargin(0.01f);

    // make up 
    ams_flux->SetStats(0);
	ams_flux->SetLineColor(AMS_MarkerColor);
	ams_flux->SetMarkerStyle(AMS_MarkerStyle);
	ams_flux->SetMarkerColor(AMS_MarkerColor);
	pamela_flux->SetLineColor(PAMELA_MarkerColor);
	pamela_flux->SetMarkerStyle(PAMELA_MarkerStyle);
	pamela_flux->SetMarkerColor(PAMELA_MarkerColor);


    c->cd(1);
	spl->SetLineColor(Model_LineColor);
	spl->SetLineStyle(Model_LineStyle);
	spl->SetLineWidth(Model_LineWidth);

    c->cd(1)->SetLogx();
    c->cd(1)->SetLogy();
    ams_flux->Draw("E1");
    pamela_flux->Draw("E1same");
    pamela_flux->GetXaxis()->SetRangeUser(min_x_plot, max_x_plot);
    spl->Draw("same");
    ams_flux->GetXaxis()->SetRangeUser(min_x_plot, max_x_plot);
    ams_flux->GetYaxis()->SetRangeUser(7000.0, 25000);
    ams_flux->GetYaxis()->SetLabelFont(43); // Absolute font size in pixel (precision 3)
    ams_flux->GetYaxis()->SetLabelSize(25);
    ams_flux->GetXaxis()->SetLabelFont(43); // Absolute font size in pixel (precision 3)
    ams_flux->GetXaxis()->SetLabelSize(25);

    c->cd(2);
    bpl->SetTitle("This work");
	bpl->SetLineColor(Model_LineColor);
	bpl->SetLineStyle(Model_LineStyle);
	bpl->SetLineWidth(Model_LineWidth);

    c->cd(2)->SetLogx();
    c->cd(2)->SetLogy();
    ams_flux->Draw("E1");
    pamela_flux->Draw("E1same");
    bpl->Draw("same");
    c->cd(2)->BuildLegend(0.2, 0.2, 0.5, 0.45);
    ams_flux->SetTitle("");

	c->cd(1);
	TPad *gPadSPL = new TPad("PadSPL", "PadSPL", 0.75, 0.75, 0.9, 0.9);
	gPadSPL->Range(0,0,1,1);
	gPadSPL->SetBottomMargin(0);
	gPadSPL->SetGridx();
	gPadSPL->Draw();
	gPadSPL->cd();
	TLatex *ttSPL = new TLatex();
	ttSPL->SetTextAlign(11);
	ttSPL->SetTextColor(2);
	ttSPL->SetTextSize(0.6);
	ttSPL->DrawLatex(0.5,0.5, "SPL");
	c->cd(2);
	TPad *gPadBPL = new TPad("padBPL", "padBPL", 0.75, 0.75, 0.9, 0.9);
	gPadBPL->Range(0,0,1,1);
	gPadBPL->SetBottomMargin(0);
	gPadBPL->SetGridx();
	gPadBPL->Draw();
	gPadBPL->cd();
	TLatex *ttBPL = new TLatex();
	ttBPL->SetTextAlign(11);
	ttBPL->SetTextColor(2);
	ttBPL->SetTextSize(0.6);
	ttBPL->DrawLatex(0.5,0.5, "BPL");


    c->cd();
	TPad *pad1 = new TPad("pad1", "pad1", 0.0, 0.0, 0.04, 1.0);
	pad1->Range(0,0,1,1);
	pad1->SetBottomMargin(0);
	pad1->SetGridx();
	pad1->Draw();
	pad1->cd();
    TLatex *tt = new TLatex();
	tt->SetTextAlign(12);
	tt->SetTextSize(0.5);
	tt->SetTextAngle(90);
	tt->DrawLatex(0.5,0.4,"Proton Flux #times E^{2.75} (GV^{1.75}m^{-2}s^{-1}sr^{-1})");
	c->cd();
	TPad *pad2 = new TPad("pad2", "pad2", 0.7, 0.0, 1.0, 0.04);
	pad2->Range(0,0,1,1);
	pad2->SetBottomMargin(0);
	pad2->SetGridx();
	pad2->Draw();
	pad2->cd();
	TLatex *tt2 = new TLatex();
	tt2->SetTextAlign(32);
	tt2->SetTextSize(0.8);
	tt2->SetTextAngle(0);
	tt2->DrawLatex(0.5,0.5,"Rigidity (GV)");


    // // flx_hist->SetTitle("Flux Model from Simulated Annealing");
    // flx_hist->SetTitle("Flux Model from Particle Swarm algorithm");
    c->SaveAs("vsother.pdf");

    // read_file->Close();
    return 0;
}