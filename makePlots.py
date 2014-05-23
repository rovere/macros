import sys
import struct
import re
from ROOT import *
from array import array
from uncertainties import ufloat

def makeFrame(name, xll, yll, xur, yur):
    c = TCanvas(name, name, 1024, 1024)
    c.SetTickx(1)
    c.SetTicky(1)
    x = array("f", [xll, xur])
    y = array("f", [yll, yur])
    g = TGraphErrors(len(x), x, y)
    g.SetMarkerSize(0)
    g.Draw("AP")
    c.Update()
    return (c, g)  # keep it alive....

def doPlot(title, xtitle, ytitle, x, y, exl, exh, eyl, eyh):
    color = kBlack
    marker_style = 20
    gr = TGraphAsymmErrors(len(x), x, y, exl, exh, eyl, eyh)
#     gr.SetTitle(title)
#     gr.GetXaxis().SetTitle(xtitle)
#     gr.GetXaxis().SetNdivisions(510, kTRUE)
#     gr.GetXaxis().SetLimits(x[0]-exl[0], x[-1]+exh[-1])
#     gr.GetYaxis().SetTitle(ytitle)
#     gr.SetMinimum(0.95)
#     gr.SetMaximum(1.005)
#     gr.GetYaxis().SetTitleOffset(1.4)
    gr.SetMarkerStyle(marker_style)
    gr.SetMarkerColor(color)
    gr.SetMarkerSize(2)
#    gr.SetFillColor(color)
#    gr.SetLineColor(color)
#    gr.SetLineStyle(line_type)
    gr.SetLineWidth(2)
#    gr.SetFillStyle(fill_pattern)
    gr.Draw("P")
    return gr

def doPlotSolid(title, xtitle, ytitle, x, y, exl, exh, eyl, eyh):
    color = kRed - 4
    marker_style = 20
    gr = TGraphAsymmErrors(len(x), x, y, exl, exh, eyl, eyh)
    gr.SetTitle(title)
    setTextProperties(gr.GetXaxis(), label=true)
    setTextProperties(gr.GetYaxis(), label=true)
    setTextProperties(gr.GetXaxis(), title=true)
    setTextProperties(gr.GetYaxis(), title=true)
    gr.GetXaxis().SetTitle(xtitle)
    gr.GetXaxis().SetNdivisions(510, kTRUE)
    gr.GetXaxis().SetLimits(x[0]-exl[0], x[-1]+exh[-1])
    gr.GetYaxis().SetTitle(ytitle)
    gr.GetYaxis().SetTitleOffset(1.5)
    gr.SetMinimum(0.79)
    gr.SetMaximum(1.04)
#    gr.GetYaxis().SetTitleOffset(1.4)
    gr.SetMarkerStyle(marker_style)
    gr.SetMarkerColor(color)
    gr.SetMarkerSize(2)
    gr.SetFillColor(color)
    gr.SetLineColor(color)
    gr.SetLineWidth(2)
#    gr.SetFillStyle(fill_pattern)
    gr.Draw("A2")
    return gr

def importData(text_card):
    ### Reads in a formatted file and returns a tuple of arrays, one array for each meaningful column, properly converted to float.
    try:
        f = open(text_card, 'r')
        #Ignore first 2 lines, i.e. labels and separator
        x_min_a = array('f')
        x_avg_a = array('f')
        x_max_a = array('f')
        eff_a = array('f')
        err_m_a = array('f')
        err_p_a = array('f')
        ref_a = array('f')
        ref_err_m_a = array('f')
        ref_err_p_a = array('f')
        x_min = 0
        x_avg = 0
        x_max = 0
        eff = 0
        err_m = 0
        err_p = 0
        ref = 0
        ref_err_m = 0
        ref_err_p = 0
        line_counter = 0
        for line in f:
            if line_counter > 1 :
                m = re.match('\s*([-]*\d+\.\d+)\s+([-]*\d+\.\d+)\s+([-]*\d+\.\d+)\s+([-]*\d+\.\d+)\s+-\s+(\d+\.\d+)/\+\s+(\d+\.\d+)\s+(\d+\.\d+)\s*-\s*(\d+\.\d+)/\+\s*(\d+\.\d+)', line)
#                if line[0] == '-':
#                    (x_min, x_avg, x_max, eff, a, err_m, b, err_p, ref, c, ref_err_m, d, ref_err_p) = struct.unpack('6s9s9s10s4s4s3s4s10s4s4s3s4s',line.strip())
#                else:
#                    (x_min, x_avg, x_max, eff, a, err_m, b, err_p, ref, c, ref_err_m, d, ref_err_p) = struct.unpack('5s9s9s10s4s4s3s4s10s4s4s3s4s',line.strip())
                if m:
                    (x_min, x_avg, x_max, eff, err_m, err_p, ref, ref_err_m, ref_err_p) = m.groups()
                x_min_a.append(float(x_avg) - float(x_min))
                x_avg_a.append(float(x_avg))
                x_max_a.append(float(x_max) - float(x_avg))
                eff_a.append(float(eff)/100.)
                err_m_a.append(float(err_m)/100.)
                err_p_a.append(float(err_p)/100.)
                ref_a.append(float(ref)/100.)
                ref_err_m_a.append(float(ref_err_m)/100.)
                ref_err_p_a.append(float(ref_err_p)/100.)
            line_counter += 1
        return (x_min_a, x_avg_a, x_max_a, eff_a, err_m_a, err_p_a, ref_a, ref_err_m_a, ref_err_p_a)
    except:
            print "Unexpected error:", sys.exc_info()[0]
            raise

def setTextProperties(obj, label=false, title=false):
    textFont = 42
    textSize = 0.043
    titleOffset = 1.
    if not label and not title:
        obj.SetTextFont(textFont)
        obj.SetTextSize(textSize)
    if label:
        obj.SetLabelFont(textFont)
        obj.SetLabelSize(textSize)
    if title:
        obj.SetTitleFont(textFont)
        obj.SetTitleSize(textSize)
        obj.SetTitleOffset(titleOffset)
    return obj

def preliminary():
    labelcms  = TPaveText(0.20, 0.25, 0.55, 0.35,"NDCBRT");
    labelcms = setTextProperties(labelcms)
#    labelcms.SetTextAlign(22);
    labelcms.SetFillColor(0);
    labelcms.AddText("CMS Preliminary");
    labelcms.AddText("#sqrt{s} = 8 TeV, L = 0.49 fb^{-1}");
#    labelcms.AddText("L = 0.49 fb^{-1}");
    labelcms.SetBorderSize(0);
#    labelcms.SetTextFont(42);
    labelcms.SetLineWidth(2);
    labelcms.Draw();
    return labelcms

def waitKey(quit=False):
    c = raw_input("Quit? ")
    if c not in ['y', 'yes', 'Y']:
        if quit:
            sys.exit()

def correctEfficiency(t, tt, prompt):
    if not prompt:
        eff_uncorr = t[3].tolist()
        eff_fake = tt[3].tolist()
        eff_uncorr_m = map(lambda x, e: ufloat(x,e), eff_uncorr, t[4].tolist())
        eff_fake_m = map(lambda x, e: ufloat(x,e), eff_fake, tt[4].tolist())
        eff_corr_m = map(lambda eu, ef: (eu-ef)/(1-ef), eff_uncorr_m, eff_fake_m)
        eff_uncorr_p = map(lambda x, e: ufloat(x,e), eff_uncorr, t[5].tolist())
        eff_fake_p = map(lambda x, e: ufloat(x,e), eff_fake, tt[5].tolist())
        eff_corr_p = map(lambda eu, ef: (eu-ef)/(1-ef), eff_uncorr_p, eff_fake_p)
        eff_corr_value = map(lambda x: x.nominal_value, eff_corr_m)
        eff_corr_stddev_m = map(lambda x: x.std_dev, eff_corr_m)
        eff_corr_stddev_p = map(lambda x: x.std_dev, eff_corr_p)
        eff_corr_a = array('f')
        eff_corr_a.fromlist(eff_corr_value)
        eff_corr_err_m_a = array('f')
        eff_corr_err_m_a.fromlist(eff_corr_stddev_m)
        eff_corr_err_p_a = array('f')
        eff_corr_err_p_a.fromlist(eff_corr_stddev_p)
        return (t[0], t[1], t[2], eff_corr_a, eff_corr_err_m_a, eff_corr_err_p_a, t[6], t[7], t[8])
    else:
        eff_uncorr = t[6].tolist()
        eff_fake = tt[6].tolist()
        eff_uncorr_m = map(lambda x, e: ufloat(x,e), eff_uncorr, t[7].tolist())
        eff_fake_m = map(lambda x, e: ufloat(x,e), eff_fake, tt[7].tolist())
        eff_corr_m = map(lambda eu, ef: (eu-ef)/(1-ef), eff_uncorr_m, eff_fake_m)
        eff_uncorr_p = map(lambda x, e: ufloat(x,e), eff_uncorr, t[8].tolist())
        eff_fake_p = map(lambda x, e: ufloat(x,e), eff_fake, tt[8].tolist())
        eff_corr_p = map(lambda eu, ef: (eu-ef)/(1-ef), eff_uncorr_p, eff_fake_p)
        eff_corr_value = map(lambda x: x.nominal_value, eff_corr_m)
        eff_corr_stddev_m = map(lambda x: x.std_dev, eff_corr_m)
        eff_corr_stddev_p = map(lambda x: x.std_dev, eff_corr_p)
        eff_corr_a = array('f')
        eff_corr_a.fromlist(eff_corr_value)
        eff_corr_err_m_a = array('f')
        eff_corr_err_m_a.fromlist(eff_corr_stddev_m)
        eff_corr_err_p_a = array('f')
        eff_corr_err_p_a.fromlist(eff_corr_stddev_p)
        return (t[0], t[1], t[2], t[3], t[4], t[5], eff_corr_a, eff_corr_err_m_a, eff_corr_err_p_a)

if __name__ == '__main__':
    xTitle = "N(primary vertices)"
    yTitle = "Efficiency"
    outputFile = "eff_vtx_dr030e030_corr.png"
    gSystem.Load("/Users/rovere/tdrStyle.C")
    setTDRStyle()
    text_card = sys.argv[1] if len(sys.argv) > 1 else None
    if not text_card:
        sys.exit(1)
    t = importData(text_card)
    tt = None
    if len(sys.argv) > 2:
        import re
        if re.match('.*txt$', sys.argv[2]):
            print "Loading second file to perform eff correction"
            tt = importData(sys.argv[2])
    if tt:
        t = correctEfficiency(t, tt, prompt=false)
        t = correctEfficiency(t, tt, prompt=true)
    r = makeFrame("eff_eta", -2.4, 0.78, 2.4, 1.01)
    legend = TLegend(0.6, 0.25, 0.93, 0.45, "")
    legend.SetFillColor(0)
    gg = doPlotSolid("", xTitle, yTitle, t[1], t[6], t[0], t[2], t[7], t[8])
    g = doPlot("", xTitle, yTitle, t[1], t[3], t[0], t[2], t[4], t[5])
    legend = setTextProperties(legend)
    legend.AddEntry(g, "New Iterations", "lp")
    legend.AddEntry(gg, "Default", "f")
    legend.Draw()
    text = TLatex(-0.5, 0.955, "Run2012C-v1, L = 0.49 fb^{-1}")
#     text.SetTextFont(43)
#     text.SetTextSize(36)
#     text.SetTextAlign(22)
#     text.Draw()
    cms_prel = preliminary()
    r[0].Update()
    r[0].RedrawAxis()
    r[0].SaveAs(outputFile)
    waitKey()
