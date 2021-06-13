import os

import pandas as pd
import ROOT as rt


ATTRS = ("obj_loss", "norm_all", "norm", "gamma1", "gamma2", "e_break")
OUTPUT_PATH = "unit_test/monte_carlo/log"
N = 200


def plot(model_name, disturb_mode, title, attr, xtitle, x_min, x_max):
    df = pd.read_csv("%s_%s_result.csv" % (model_name, disturb_mode))

    data = df[attr].tolist()

    f_name = "%s_%s_gaus" % (model_name, disturb_mode)
    f1 = rt.TF1(f_name, "gaus", x_min, x_max)

    hist = rt.TH1F(title, title, 20, x_min, x_max)
    for d in data:
        hist.Fill(d)

    C = rt.TCanvas('C', 'C', 800, 700)
    hist.SetStats(0)
    hist.SetTitle(title)
    hist.GetYaxis().SetTitle("#")
    hist.GetXaxis().SetTitle(xtitle)
    hist.Fit(f_name)
    hist.Draw()

    mean = f1.GetParameter(1)
    sigma = f1.GetParameter(2)

    xlabel = rt.TLatex()
    xlabel.SetNDC()
    xlabel.SetTextSize(0.05)
    xlabel.SetTextColor(1)
    xlabel.SetTextAlign(22)
    xlabel.SetTextAngle(0)
    xlabel.DrawLatex(0.75, 0.85, "#mu=%.2f, \sigma=%.2f" % (mean, sigma))
    xlabel.Draw()

    C.SaveAs(os.path.join(OUTPUT_PATH, "%s_%s_%s.pdf" %
                          (model_name, attr, disturb_mode)))

    # hist.Fit("gaus"
    # plt.plot(bins, best_fit_line)
    # plt.show()


def main():
    # SPL
    plot(
        model_name="SPLwHe", disturb_mode="sys",
        title="SPL: #Gamma_{1} (Systematic Error, N=%d)" % N, attr="gamma1", xtitle="\Gamma_{1}",
        x_min=2.6, x_max=3.0
    )
    plot(
        model_name="SPLwHe", disturb_mode="tot",
        title="SPL: #Gamma_{1} (Total Error, N=%d)" % N, attr="gamma1", xtitle="\Gamma_{1}",
        x_min=2.6, x_max=3.0
    )
    # BPL
    plot(
        model_name="BPLwHe", disturb_mode="sys",
        title="BPL: #Gamma_{1} (Systematic Error, N=%d)" % N, attr="gamma1", xtitle="\Gamma_{1}",
        x_min=2.6, x_max=3.2
    )
    plot(
        model_name="BPLwHe", disturb_mode="tot",
        title="BPL: #Gamma_{1} (Total Error, N=%d)" % N, attr="gamma1", xtitle="\Gamma_{1}",
        x_min=2.6, x_max=3.2
    )

    plot(
        model_name="BPLwHe", disturb_mode="sys",
        title="BPL: #Gamma_{2} (Systematic Error, N=%d)" % N, attr="gamma2", xtitle="\Gamma_{2}",
        x_min=2.5, x_max=3.0
    )
    plot(
        model_name="BPLwHe", disturb_mode="tot",
        title="BPL: #Gamma_{2} (Total Error, N=%d)" % N, attr="gamma2", xtitle="\Gamma_{2}",
        x_min=2.5, x_max=3.0
    )

    plot(
        model_name="BPLwHe", disturb_mode="sys",
        title="BPL: E_{break} (Systematic Error, N=%d)" % N, attr="e_break", xtitle="E_{break}",
        x_min=310, x_max=370
    )
    plot(
        model_name="BPLwHe", disturb_mode="tot",
        title="BPL: E_{break} (Total Error, N=%d)" % N, attr="e_break", xtitle="E_{break}",
        x_min=310, x_max=370
    )
