from ROOT import *
from array import array
from tdrStyle import *
from os import getenv
setTDRStyle()

vtag=False

def plot_ratio(process):

    highest = {}
    lowest = {}

    baseDir = getenv('CMSSW_BASE')+'/src/MonoX-2/'
    f = TFile(baseDir + 'combined_model.root','READ')
        
    if (process=='dimuon'):
        dirname = "Z_constraints_category_monotop"
        base    = "zmm_weights_monotop"
        label = "R_{Z(#mu#mu)}"
        addsys  = sqrt(0.02*0.02)

    if (process=='dielectron'):
        dirname = "Z_constraints_category_monotop"
        base    = "zee_weights_monotop"
        label   = "R_{Z(ee)}"
        addsys  = sqrt(0.04*0.04 + 0.01*0.01)

    if (process=='photon'):
        dirname = "Z_constraints_category_monotop" 
        base    = "photon_weights_monotop"
        label   = "R_{#gamma}"
        addsys  = 0

    if (process=='singleelectronw'):
        dirname = "W_constraints_category_monotop" 
        base    = "wenWCR_weights_monotop"
        label   = "R_{W(e#nu)}"
        addsys  = sqrt(0.05*0.05 + 0.01*0.01 + 0.03*0.03)

    if (process=='singlemuonw'):
        dirname = "W_constraints_category_monotop" 
        base    = "wmnWCR_weights_monotop"
        label   = "R_{W(#mu#nu)}"
        addsys  = sqrt(0.03*0.03 + 0.01*0.01)
        #addsys  = 0 

    if (process=='singleelectrontop'):
        dirname = "Top_constraints_category_monotop" 
        base    = "topenTopCR_weights_monotop"
        label   = "R_{t#bar{t}(e#nub)}"
        addsys  = sqrt(0.05*0.05 + 0.01*0.01 + 0.03*0.03)

    if (process=='singlemuontop'):
        dirname = "Top_constraints_category_monotop" 
        base    = "topmnTopCR_weights_monotop"
        label   = "R_{t#bar{t}(#mu#nub)}"
        addsys  = sqrt(0.03*0.03 + 0.01*0.01)


    ratio = f.Get(dirname+"/"+base)
    up_final = ratio.Clone("ratio")
    down_final = ratio.Clone("ratio")

    for b in range(ratio.GetNbinsX()+1):
        up_final.SetBinContent(b,0.0)
        down_final.SetBinContent(b,0.0)
        highest[b] = 0
        lowest [b] = 100.0

    f.cd(dirname)
    for key in gDirectory.GetListOfKeys():
        if ('TH1' in key.GetClassName()):
            if (process in key.GetName()) or (base in key.GetName()):
                print key.GetName()
                if ('Up' in key.GetName()):
                    up = f.Get(dirname+"/"+key.GetName())
                    for b in range(ratio.GetNbinsX()+1):
                        diff = up.GetBinContent(b) - ratio.GetBinContent(b)
                        highest[b] =  sqrt(highest[b]**2 + diff**2)
                        #if up.GetBinContent(b) > highest[b]:
                        #    highest[b] = up.GetBinContent(b)
                        #else:
                        #    highest[b] = highest[b]
                        up_final.SetBinContent(b,highest[b])

                if ('Down' in key.GetName()):
                    down = f.Get(dirname+"/"+key.GetName())
                    for b in range(ratio.GetNbinsX()+1):
                        if down.GetBinContent(b) < lowest[b]:
                            lowest[b] = down.GetBinContent(b)
                        else:
                            lowest[b] = lowest[b]
                        down_final.SetBinContent(b,lowest[b])
              
    gStyle.SetOptStat(0)

    c = TCanvas("c","c",600,600)  
    c.SetTopMargin(0.06)
    c.cd()
    c.SetRightMargin(0.04)
    c.SetTopMargin(0.07)
    c.SetLeftMargin(0.12)


    uncertband = ratio.Clone("ratio")
    for b in range(ratio.GetNbinsX()+1):
        #err1 = abs(down_final.GetBinContent(b) -  ratio.GetBinContent(b))
        err1 = abs(up_final.GetBinContent(b) -  ratio.GetBinContent(b))
        #uncertband.SetBinError(b,max(err1,err2))
        #uncertband.SetBinError(b,err1)
        uncertband.SetBinError(b,up_final.GetBinContent(b) + addsys)
        #print "Uncert",b,ratio.GetBinContent(b),down_final.GetBinContent(b),up_final.GetBinContent(b), max(err1,err2)

    #uncertband.SetFillStyle(3144);
    #uncertband.SetFillColor(33);

    #uncertband.SetFillStyle(0);
    uncertband.SetFillColor(ROOT.kGray+1);

    uncertband.GetYaxis().SetTitle(label)
    uncertband.GetYaxis().CenterTitle()
    uncertband.GetYaxis().SetTitleSize(0.4*c.GetLeftMargin())
    uncertband.GetXaxis().SetTitle("U [GeV]")
    uncertband.GetXaxis().SetTitleSize(0.4*c.GetBottomMargin())
    uncertband.SetMaximum(1.5*ratio.GetMaximum())
    uncertband.SetMinimum(0.5*ratio.GetMinimum())
    uncertband.GetYaxis().SetTitleOffset(1.15)

    ratio.SetMarkerStyle(20)
    ratio.SetLineColor(1)
    ratio.SetLineWidth(2)

    uncertband.Draw("e2")    
    ratio.Draw("same")

    legend = TLegend(.60,.75,.92,.92)
    legend.AddEntry(ratio,"Transfer Factor (Stat Uncert)" , "p")
    legend.AddEntry(uncertband,"Stat + Sys Uncert" , "f")

    legend.SetShadowColor(0);
    legend.SetFillColor(0);
    legend.SetLineColor(0);

    legend.Draw("same")

    latex2 = TLatex()
    latex2.SetNDC()
    latex2.SetTextSize(0.035)
    latex2.SetTextAlign(31) # align right
    #latex2.DrawLatex(0.87, 0.95, "2.24 pb^{-1} (13 TeV)");
    latex2.DrawLatex(0.87, 0.95, "2.1 pb^{-1} (13 TeV)");

    latex3 = TLatex()
    latex3.SetNDC()
    latex3.SetTextSize(0.75*c.GetTopMargin())
    latex3.SetTextFont(62)
    latex3.SetTextAlign(11) # align right
    latex3.DrawLatex(0.22, 0.85, "CMS");
    latex3.SetTextSize(0.5*c.GetTopMargin())
    latex3.SetTextFont(52)
    latex3.SetTextAlign(11)
    latex3.DrawLatex(0.20, 0.8, "Preliminary");
    
    gPad.RedrawAxis()

    #c.SaveAs("/afs/cern.ch/user/z/zdemirag/www/Monojet/moriond/rfactor_"+process+".pdf")
    #c.SaveAs("/afs/cern.ch/user/z/zdemirag/www/Monojet/moriond/rfactor_"+process+".png")
    #c.SaveAs("/afs/cern.ch/user/z/zdemirag/www/Monojet/moriond/rfactor_"+process+".C")
    #c.SaveAs("rfactor_"+process+".root")

    c.SaveAs("/afs/cern.ch/user/s/snarayan/www/figs/monotop/fits_wcr/rfactor_"+process+".pdf")
    c.SaveAs("/afs/cern.ch/user/s/snarayan/www/figs/monotop/fits_wcr/rfactor_"+process+".png")
    c.SaveAs("/afs/cern.ch/user/s/snarayan/www/figs/monotop/fits_wcr/rfactor_"+process+".C")

    #c.SaveAs("rfactor_"+process+".root")

    f_out = TFile(process+".root","recreate")
    f_out.cd()
    ratio.Write()
    f_out.Close()

    del c
  
plot_ratio('dimuon')
plot_ratio('dielectron')
plot_ratio('photon')
plot_ratio('singlemuonw')
plot_ratio('singleelectronw')
plot_ratio('singlemuontop')
plot_ratio('singleelectrontop')
