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
#include "TH2F.h"
#include "TCanvas.h"

#include "../../utility/cpp/io.h"
#include "../../utility/cpp/parser.h"
#include "../../utility/cpp/histogram.h"
#include "../../utility/cpp/datatype.h"
#include "../../settings.h"
#include "flxmap.h"

int main(int argc, char** argv){
    std::cout << "RUN!!" << std::endl;

    auto expmaps = FileIO::readExposureMap();
    std::cout << expmaps.size() << std::endl;
    auto c = new TCanvas("expmaps","Exposure Maps",900,900);
    c->Divide(2,2);
    float lbOS = -0.13; // Z-axis label offset
    float lbS = 0.05;   // Z-axis label size
    float ttOS = 0.5;   // Z-axis tltle offset
    float ttS = 0.04;   // Z-axis tltle size
    for (unsigned int i=0; i<4; i++){
        c->cd(i);
        expmaps[13*i]->SetStats(0);
        gPad->SetTheta(-90);
        gPad->SetPhi(-90);
        expmaps[13*i]->Draw("SURF2POLZ");
        expmaps[13*i]->GetXaxis()->SetTitle("#phi (degree)");
        expmaps[13*i]->GetYaxis()->SetTitle("#theta_{nadir} (degree)");
        expmaps[13*i]->GetYaxis()->SetRangeUser(0.,80.);
        expmaps[13*i]->GetZaxis()->SetLabelOffset(lbOS);
        expmaps[13*i]->GetZaxis()->SetLabelSize(lbS);
        expmaps[13*i]->GetZaxis()->SetTitleOffset(ttOS);
        expmaps[13*i]->GetZaxis()->SetTitleSize(ttS);
        expmaps[13*i]->GetZaxis()->SetTitle("Exposure (m^{2}s)");
        c->cd(i)->SetLogz();
    }
    c->cd();
    c->SaveAs("test_expmaps.png");
    // for (unsigned int i=0; i<50;i++) std::cout << expmaps[i] << std::endl; 

    // auto histogram = new Histogram();
    // auto bla = histogram->get_energy_mid_bins();    
    // for (unsigned int i=0; i<50;i++) std::cout << bla[i] << std::endl; 

    return 0;
}