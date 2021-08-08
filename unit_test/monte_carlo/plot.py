import os

import numpy as np
import pandas as pd
import ROOT as rt
from scipy.optimize import curve_fit

F_PREFIX = "-".join(("SPLwHe", "BPLwHe"))
ATTRS = ("obj_loss", "norm_all", "norm", "gamma1", "gamma2", "e_break")
OUTPUT_PATH = "unit_test/monte_carlo/log"
N = 2000


def my_gaussian(_mu):
    def _gaussian(x, a0, sig):
        return a0 * np.exp(-np.power(x - _mu, 2.) / (2 * np.power(sig, 2.)))
    return _gaussian


def plot(model_name, disturb_mode, title, attr, xtitle, x_min, x_max, x0, x_sd, n_bins=16):

    df = pd.read_csv("%s_%s_result.csv" % (F_PREFIX, disturb_mode))

    _attr = "%s_%s" % (model_name, attr)
    data = df[_attr].tolist()

    f_name = "%s_%s_%s_gaus" % (model_name, disturb_mode, attr)
    f1 = rt.TF1(
        f_name,
        "gaus",
        # "[0]*exp(-0.5*(x-[1])*(x-[1])/([2]*[2]))",
        x_min, x_max
    )
    # f1.SetParameters(50, 3.0, 0.4)
    # f1.SetParLimits(1, 2.79, 2.79)
    # fitHits->FixParameter(1, exp_mean);

    hist = rt.TH1F(title, title, n_bins, x_min, x_max)
    for d in data:
        hist.Fill(d)
    x = [hist.GetXaxis().GetBinCenter(i+1) for i in range(hist.GetNbinsX())]
    y = [hist.GetBinContent(i+1) for i in range(hist.GetNbinsX())]
    gaussian = my_gaussian(_mu=x0)
    popt, _ = curve_fit(
        gaussian,
        x, y,
        bounds=((100, x_sd * 0.5), (800, x_sd * 2.0)),
        p0=(600, x_sd),
        # method="dogbox"
    )
    a0 = popt[0]
    mean = x0
    sigma = popt[1]
    f1.SetParameters(a0, mean, sigma)
    print(x)
    print(y)
    print(popt)

    C = rt.TCanvas('C', 'C', 800, 700)
    hist.SetStats(0)
    hist.SetTitle(title)
    hist.GetYaxis().SetTitle("#")
    hist.GetXaxis().SetTitle(xtitle)
    # hist.Fit(f_name, "L")
    hist.Draw()
    f1.Draw("same")

    # mean = f1.GetParameter(1)
    # sigma = f1.GetParameter(2)

    xlabel = rt.TLatex()
    xlabel.SetNDC()
    xlabel.SetTextSize(0.05)
    xlabel.SetTextColor(1)
    xlabel.SetTextAlign(22)
    xlabel.SetTextAngle(0)
    xlabel.DrawLatex(0.72, 0.85, "#mu_{fix}=%.2f, \sigma=%.2f" % (mean, sigma))
    xlabel.Draw()

    C.SaveAs(os.path.join(OUTPUT_PATH, "%s_%s_%s.pdf" %
                          (model_name, attr, disturb_mode)))


def main():
    # SPL
    plot(
        model_name="SPLwHe", disturb_mode="sys",
        title="SPL: #Gamma_{1} (Statistical Error, N=%d)" % N, attr="gamma1", xtitle="\Gamma_{1}",
        x_min=2.4, x_max=3.1, x0=2.70, x_sd=0.03
    )
    plot(
        model_name="SPLwHe", disturb_mode="tot",
        title="SPL: #Gamma_{1} (Total Error, N=%d)" % N, attr="gamma1", xtitle="\Gamma_{1}",
        x_min=2.4, x_max=3.1, x0=2.70, x_sd=0.04
    )
    # BPL
    plot(
        model_name="BPLwHe", disturb_mode="sys",
        title="BPL: #Gamma_{1} (Statistical Error, N=%d)" % N, attr="gamma1", xtitle="\Gamma_{1}",
        x_min=2.6, x_max=3.2, x0=2.86, x_sd=0.05
    )
    plot(
        model_name="BPLwHe", disturb_mode="tot",
        title="BPL: #Gamma_{1} (Total Error, N=%d)" % N, attr="gamma1", xtitle="\Gamma_{1}",
        x_min=2.6, x_max=3.2, x0=2.86, x_sd=0.08
    )

    plot(
        model_name="BPLwHe", disturb_mode="sys",
        title="BPL: #Gamma_{2} (Statistical Error, N=%d)" % N, attr="gamma2", xtitle="\Gamma_{2}",
        x_min=2.4, x_max=2.9, x0=2.63, x_sd=0.05
    )
    plot(
        model_name="BPLwHe", disturb_mode="tot",
        title="BPL: #Gamma_{2} (Total Error, N=%d)" % N, attr="gamma2", xtitle="\Gamma_{2}",
        x_min=2.4, x_max=2.9, x0=2.63, x_sd=0.08
    )

    plot(
        model_name="BPLwHe", disturb_mode="sys",
        title="BPL: E_{break} (Statistical Error, N=%d)" % N, attr="e_break", xtitle="E_{break}",
        x_min=290, x_max=380, x0=333, x_sd=5
    )
    plot(
        model_name="BPLwHe", disturb_mode="tot",
        title="BPL: E_{break} (Total Error, N=%d)" % N, attr="e_break", xtitle="E_{break}",
        x_min=290, x_max=380, x0=333, x_sd=9
    )
