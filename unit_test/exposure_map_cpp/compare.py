'''
    Python 2.7
'''

import ROOT as rt

import csv
import numpy as np
import math
import os

from utility import transform
import settings

E = 10
MAP_OLD_I = 0

path_new = os.path.join(
    os.getcwd(),
    'data',
    'exposure_map',
    'w%d_%d'%(settings.WEEK_BEGIN, settings.WEEK_END)
)

path_old = os.path.join(
    os.getcwd(),
    'old_work',
    'ExpMap_P8R2_ULTRACLEANVETO_V6_w010-w399.root'
) 

def main():
    # new
    new_expmap_np = np.genfromtxt(os.path.join(path_new, settings.IRF_NAME,'expmap_E%d.csv'%E), dtype = float, delimiter = ',')[:,0].reshape(settings.N_BINS_PHI_NADIR, settings.N_BINS_THETA_NADIR)
    print(new_expmap_np.shape)
    new_expmap = rt.TH2F(
        'new_expmap','new_expmap',
        settings.N_BINS_PHI_NADIR, settings.PHI_NADIR_MIN, settings.PHI_NADIR_MAX,
        settings.N_BINS_THETA_NADIR, settings.THETA_NADIR_MIN, settings.THETA_NADIR_MAX
    )
    for j in range(settings.N_BINS_PHI_NADIR):
        for i in range(settings.N_BINS_THETA_NADIR):
            new_expmap.SetBinContent(j+1, i+1, new_expmap_np[j, i])
    # old
    name_expmap = ['expmap%03d'%i for i in range(50)]
    f_expmap = rt.TFile(path_old)
    expmap = f_expmap.Get(name_expmap[MAP_OLD_I])
    expmap.Scale(1./10000.) # cm^2 -> m^2
    # divide
    div_expmap = expmap.Clone('div_expmap')
    div_expmap.Divide(new_expmap)
    # subtract
    sub_expmap = expmap.Clone('sub_expmap')
    sub_expmap.Add(new_expmap, -1)

    ## visualize
    canvas = rt.TCanvas('C','C',900,900)
    canvas.Divide(2,2)


    lbOS=-0.13 #Z-axis label offset
    lbS=0.05   #Z-axis label size
    ttOS=0.5   #Z-axis tltle offset
    ttS=0.04   #Z-axis tltle size

    ## old
    canvas.cd(1)
    expmap.SetStats(0)
    rt.gPad.SetTheta(-90)
    rt.gPad.SetPhi(-90)
    expmap.Draw('SURF2POLZ')
    expmap.GetXaxis().SetTitle('#phi (degree)')
    expmap.GetYaxis().SetTitle('#theta_{nadir} (degree)')
    expmap.GetYaxis().SetRangeUser(0.,80.)
    expmap.GetZaxis().SetLabelOffset(lbOS)
    expmap.GetZaxis().SetLabelSize(lbS)
    expmap.GetZaxis().SetTitleOffset(ttOS)
    expmap.GetZaxis().SetTitleSize(ttS)
    expmap.GetZaxis().SetTitle('Exposure (m^{2}s)')
    expmap.SetTitle('old_expmap %d GeV'%E)
    ## new
    canvas.cd(2)
    new_expmap.SetStats(0)
    rt.gPad.SetTheta(-90)
    rt.gPad.SetPhi(-90)
    new_expmap.Draw('SURF2POLZ')
    new_expmap.GetXaxis().SetTitle('#phi (degree)')
    new_expmap.GetYaxis().SetTitle('#theta_{nadir} (degree)')
    new_expmap.GetYaxis().SetRangeUser(0.,80.)
    new_expmap.GetZaxis().SetLabelOffset(lbOS)
    new_expmap.GetZaxis().SetLabelSize(lbS)
    new_expmap.GetZaxis().SetTitleOffset(ttOS)
    new_expmap.GetZaxis().SetTitleSize(ttS)
    new_expmap.GetZaxis().SetTitle('Exposure (m^{2}s)')
    new_expmap.SetTitle('new_expmap %d GeV'%E)
    ## divide
    canvas.cd(3)
    div_expmap.SetStats(0)
    rt.gPad.SetTheta(-90)
    rt.gPad.SetPhi(-90)
    div_expmap.Draw('SURF2POLZ')
    div_expmap.GetXaxis().SetTitle('#phi (degree)')
    div_expmap.GetYaxis().SetTitle('#theta_{nadir} (degree)')
    div_expmap.GetYaxis().SetRangeUser(0.,80.)
    div_expmap.GetZaxis().SetLabelOffset(lbOS)
    div_expmap.GetZaxis().SetLabelSize(lbS)
    div_expmap.GetZaxis().SetTitleOffset(ttOS)
    div_expmap.GetZaxis().SetTitleSize(ttS)
    div_expmap.GetZaxis().SetTitle('Exposure (m^{2}s)')
    div_expmap.SetTitle('old/new_expmap %d GeV'%E)
    ## subtract
    canvas.cd(4)
    sub_expmap.SetStats(0)
    rt.gPad.SetTheta(-90)
    rt.gPad.SetPhi(-90)
    sub_expmap.Draw('SURF2POLZ')
    sub_expmap.GetXaxis().SetTitle('#phi (degree)')
    sub_expmap.GetYaxis().SetTitle('#theta_{nadir} (degree)')
    sub_expmap.GetYaxis().SetRangeUser(0.,80.)
    sub_expmap.GetZaxis().SetLabelOffset(lbOS)
    sub_expmap.GetZaxis().SetLabelSize(lbS)
    sub_expmap.GetZaxis().SetTitleOffset(ttOS)
    sub_expmap.GetZaxis().SetTitleSize(ttS)
    sub_expmap.GetZaxis().SetTitle('Exposure (m^{2}s)')
    sub_expmap.SetTitle('old-new_expmap %d GeV'%E)

    canvas.cd(1).SetLogz()
    canvas.cd(2).SetLogz()
    # raw_input()
    canvas.SaveAs(os.path.join('unit_test', 'exposure_map_cpp', 'log', 'compare_prev_w10_399.png'))
    print("hi")