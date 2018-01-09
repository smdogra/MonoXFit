from ROOT import *
from collections import defaultdict
from os import getenv
from array import array
from tdrStyle import *
import plotConfig
setTDRStyle()

#plotextralabel = 'Masked'
plotextralabel = ''

new_dic = defaultdict(dict)

def getInt(h):
  nbins = h.GetNbinsX()
  total=0.
  for iB in xrange(1,nbins+1):
    total += h.GetBinContent(iB)*h.GetBinWidth(iB)
  return total

def plotPreFitPostFit(region,cat='category_monotop',combinecat='',blind=False):
  channel = {"singlemuonw":"wmn", 
              "singlemuontop":"tmn",
              "dielectron":"zee",
              "dimuon":"zmm",
              "photon":"pho", 
              "signal":"sig", 
              "singleelectrontop":"ten", 
              "singleelectronw":"wen"}
  extralabels = {"singlemuonw":"Single muon W CR", 
              "singlemuontop":"Single muon t#bar{t} CR",
              "dielectron":"Dielectron CR",
              "dimuon":"Dimuon CR",
              "photon":"Photon CR", 
              "signal":"Signal region", 
              "singleelectrontop":"Single electron t#bar{t} CR", 
              "singleelectronw":"Single electron W CR"}

  extralabel = extralabels[region]
  mainbkg = {"singlemuonw":"wjets", "dimuon":"zll", "photon":"gjets", "signal":None, "singleelectronw":"wjets", "dielectron":"zll", "singlemuontop":"ttbar","singleelectrontop":"ttbar"}

  basedir = getenv('CMSSW_BASE') + '/src/MonoXFit_CSV/'

  f_mlfit = TFile(basedir+'/datacards/mlfit.root','READ')

#   f_data = TFile(basedir+"/mono-x.root","READ")
#   f_data.cd(cat)
#   h_data = None
#   h_data = gDirectory.Get(region+"_data")
#  if region=='signal':
#    h_res = gDirectory.Get('signal_Mres1100_Mchi100'); h_res.SetLineColor(kGreen+3)
#    h_fcnc = gDirectory.Get('signal_monotop_fcnc_mMed900'); h_fcnc.SetLineColor(kViolet+9)
#    h_res.Scale(3.91)
#    h_fcnc.Scale(0.78)
#    for h in [h_res,h_fcnc]:
#    for h in [h_fcnc]:
#      h.Scale(1,"width")
#      h.SetLineWidth(2)
#      h.SetLineStyle(2)

  '''
  if not region=="signal":
    h_data = gDirectory.Get(region+"_data")
  else:
    blind = True
  '''

  b_width = [50,50,50,100,500]

  processesNormal = [
      'qcd',
      'dibosons',
      'stop',
      'wjets',
      'ttbar',
      'zvv',
      'zll',
      'gjets',
      'signal',
  ]


  processes = processesNormal
  
  processNames = {'gjets':'#gamma+jets',
                  'qcd':'QCD',
                  'ttbar':'t#bar{t}',
                  'stop':'Single top',
                  'dibosons':'VV',
                  'zvv':'Z#rightarrow#nu#nu',
                  'zll':'Z#rightarrowll',
                  'wjets':'W#rightarrowl#nu',
                  'signal':'m_{V}=1.1 TeV',
                  }
  
  order = [
           'Z#rightarrow#nu#nu',
           'Z#rightarrowll',
           'W#rightarrowl#nu',
           't#bar{t}',
           'Single top',
           'VV',
           'QCD',
           '#gamma+jets',
           'Data',
      ]
  zcolor = kAzure+5
  colors = {
      'qcd':kGray,
      'dibosons':kViolet-8,    
      'ttbar':kOrange-3,
      'gjets':kCyan-2,
      'zjets':zcolor,
      'zvv':zcolor,
      'zll':zcolor,
      'wjets':kGreen-6,
      'stop':kRed-5,
      'signal':kBlack,
  }

  binLowE = []

  # Pre-Fit
  h_prefit = {}
  print "shapes_prefit/"+combinecat+channel[region]+"/total"
  h_prefit['total'] = f_mlfit.Get("shapes_prefit/"+combinecat+channel[region]+"/total")
  for i in range(1,h_prefit['total'].GetNbinsX()+2):
    binLowE.append(h_prefit['total'].GetBinLowEdge(i))

  h_all_prefit = TH1F("h_all_prefit","h_all_prefit",len(binLowE)-1,array('d',binLowE))    
  h_other_prefit = TH1F("h_other_prefit","h_other_prefit",len(binLowE)-1,array('d',binLowE))    
  h_stack_prefit = THStack("h_stack_prefit","h_stack_prefit")    

  for process in processes:
    h_prefit[process] = f_mlfit.Get("shapes_prefit/"+combinecat+channel[region]+"/"+process)
    if (not h_prefit[process]): continue
    if (str(h_prefit[process].Integral())=="nan"): continue
#    h_prefit[process].SetLineColor(colors[process])
    h_prefit[process].SetLineColor(kBlack)
    h_prefit[process].SetFillColor(colors[process])
    h_all_prefit.Add(h_prefit[process])
    if (not process==mainbkg[region]): h_other_prefit.Add(h_prefit[process])
    h_stack_prefit.Add(h_prefit[process])

  # Post-Fit
  h_postfit = {}
  h_postfit['total'] = f_mlfit.Get("shapes_fit_s/"+combinecat+channel[region]+"/total")
  h_all_postfit = TH1F("h_all_postfit","h_all_postfit",len(binLowE)-1,array('d',binLowE))    
  h_other_postfit = TH1F("h_other_postfit","h_other_postfit",len(binLowE)-1,array('d',binLowE))    
  h_stack_postfit = THStack("h_stack_postfit","h_stack_postfit")    
  
  h_postfit['totalv2'] = f_mlfit.Get("shapes_fit_s/"+combinecat+channel[region]+"/total")
  
  # Data
  h_data = h_all_prefit.Clone('data')
  nb = h_data.GetNbinsX()
  for ib in xrange(1,nb+1): h_data.SetBinContent(ib,0)
  g_data = f_mlfit.Get('shapes_prefit/'+combinecat+channel[region]+'/data')
  ys = g_data.GetY()
  yerrs = g_data.GetEYhigh()
  for ib in xrange(1,nb+1):
    width = h_data.GetBinWidth(ib)
    width = 1
    h_data.SetBinContent(ib,ys[ib-1]/width)
    h_data.SetBinError(ib,yerrs[ib-1]/width)

  for process in processes:
    h_postfit[process] = f_mlfit.Get("shapes_fit_s/"+combinecat+channel[region]+"/"+process)
    if (not h_postfit[process]): continue
    if (str(h_postfit[process].Integral())=="nan"): continue
#    h_postfit[process].SetLineColor(colors[process])
    h_postfit[process].SetLineColor(kBlack)
    h_postfit[process].SetFillColor(colors[process])
    if process=='signal':
      h_postfit[process].SetFillStyle(3005)
    h_all_postfit.Add(h_postfit[process])
    if (not process==mainbkg[region]): h_other_postfit.Add(h_postfit[process])
    h_stack_postfit.Add(h_postfit[process])

            
  gStyle.SetOptStat(0)

  c = TCanvas("c","c",600,700)  
  SetOwnership(c,False)
  c.cd()
  c.SetLogy()
  c.SetBottomMargin(0.3)
  c.SetRightMargin(0.06)
  
  dummy = h_all_prefit.Clone("dummy")
  dummy.SetFillColor(0)
  dummy.SetLineColor(0)
  dummy.SetLineWidth(0)
  dummy.SetMarkerSize(0)
  dummy.SetMarkerColor(0) 
  dummy.GetYaxis().SetTitle("Events / GeV")
  dummy.GetXaxis().SetTitle("")
  dummy.GetXaxis().SetTitleSize(0)
  dummy.GetXaxis().SetLabelSize(0)
  dummy.SetMaximum(50*dummy.GetMaximum())
  dummy.SetMinimum(0.001)
  dummy.GetYaxis().SetTitleOffset(1.15)
  dummy.Draw()

  h_stack_postfit.Draw("hist same")

  h_all_prefit.SetLineColor(2)
  h_all_prefit.SetLineWidth(3)
#  h_all_prefit.Scale(1,"width")
  h_all_prefit.Draw("histsame")

  h_all_postfit.SetLineColor(4)
  h_all_postfit.SetLineWidth(3)
  h_all_postfit.Draw("histsame")

  h_all_prefit.SetLineWidth(2)
  h_all_postfit.SetLineWidth(2)
  '''
  h_all_postfit.Scale(1,"width")


  h_other_prefit.SetLineColor(1)
  h_other_prefit.SetFillColor(kGray+1)
  h_other_prefit.Scale(1,"width")
  h_other_prefit.Draw("histsame")
  '''

  if not blind:
    h_data.SetMarkerStyle(20)
    h_data.SetMarkerSize(1.2)
#    h_data.Scale(1,"width")
    h_data.Draw("epsame")

#  if region=='signal':
#    h_res.Draw('hist same')
#    h_fcnc.Draw('hist same')

  legend = TLegend(.55,.55,.95,.90)
  #legend.SetTextSize(0.04)
  yields = {}
  if not blind:
    legend.AddEntry(h_data,"Fake data [sig injected]","elp")
    yields['Data'] = getInt(h_data)
  legend.AddEntry(h_all_prefit, "SM backgrounds (pre-fit)", "l")
  legend.AddEntry(h_all_postfit, "SM backgrounds (post-fit)", "l") 
  for process in processes:
    try:
      hist = h_postfit[process]
      if (not h_postfit[process]): continue
      if (str(h_postfit[process].Integral())=="nan"): continue
      legend.AddEntry(hist,processNames[process],"f")
      yields[processNames[process]] = getInt(hist)
    except KeyError:
      pass
#  if region=='signal':
#    legend.AddEntry(h_res,'Resonant M_{#phi}=1.1 TeV','l')
#    legend.AddEntry(h_fcnc,'FCNC M_{V}=0.9 TeV','l')
  legend.SetShadowColor(0);
  legend.SetFillColor(0);
  legend.SetFillStyle(0)
  legend.SetBorderSize(0)
  legend.SetLineColor(0);
  legend.Draw("same")


  latex2 = TLatex()
  latex2.SetNDC()
  latex2.SetTextSize(0.5*c.GetTopMargin())
  latex2.SetTextFont(42)
  latex2.SetTextSize(0.6*c.GetTopMargin())
  latex2.DrawLatex(0.16, 0.85,extralabel)
  if 'loose' in combinecat:
    latex2.DrawLatex(0.16,0.8,"0.1<BDT<0.45")
  elif 'tight' in combinecat:
    latex2.DrawLatex(0.16,0.8,"BDT>0.45")
  latex2.SetTextAlign(31) # align right
  latex2.SetTextSize(0.5*c.GetTopMargin())
  latex2.DrawLatex(0.94, 0.94,"%.1f fb^{-1} (13 TeV)"%(plotConfig.lumi))
  #latex2.DrawLatex(0.9, 0.94,"2.32 fb^{-1} (13 TeV)")
  latex2.SetTextSize(0.6*c.GetTopMargin())
  latex2.SetTextFont(62)
  latex2.SetTextAlign(11) # align left
  latex2.DrawLatex(0.12, 0.94, "CMS")
  latex2.SetTextSize(0.5*c.GetTopMargin())
  latex2.SetTextFont(52)
  latex2.SetTextAlign(11)
  latex2.DrawLatex(0.21, 0.94, "Preliminary")          

  gPad.RedrawAxis()

  pad = TPad("pad", "pad", 0.0, 0.0, 1.0, 0.9)
  SetOwnership(pad,False)

  pad.SetTopMargin(0.7)
  pad.SetRightMargin(0.06)
  #pad.SetLeftMargin(0.18)
  pad.SetFillColor(0)
  pad.SetGridy(0)
  pad.SetFillStyle(0)
  pad.Draw()
  pad.cd(0)

  met = []; dmet = [];
  ratio_pre = []; ratio_pre_hi = []; ratio_pre_lo = [];
  ratio_post = []; ratio_post_hi = []; ratio_post_lo = [];

  for i in range(1,h_all_prefit.GetNbinsX()+1):

    #ndata = array("d", [0.0])
    #metave = array("d",[0.0])
    #h_data.GetPoint(i-1, metave[0], ndata[0])

    #ndata = h_data.GetY()[i-1]
    if not blind:
      ndata = h_data.GetBinContent(i)
    else:
      ndata = 0
    #print ndata

    if (ndata>0.0 and not blind):
      e_data_hi = h_data.GetBinError(i)/ndata
      e_data_lo = h_data.GetBinError(i)/ndata
    else:
      e_data_hi = 0.0
      e_data_lo = 0.0
      
    n_all_pre = h_all_prefit.GetBinContent(i)
    n_all_post = h_all_postfit.GetBinContent(i)

    met.append(h_all_prefit.GetBinCenter(i))
    dmet.append((h_all_prefit.GetBinLowEdge(i+1)-h_all_prefit.GetBinLowEdge(i))/2)

    if (n_all_pre>0.0):
      ratio_pre.append(ndata/n_all_pre)
      ratio_pre_hi.append(ndata*e_data_hi/n_all_pre)
      ratio_pre_lo.append(ndata*e_data_lo/n_all_pre)
    else:
      ratio_pre.append(0.0)
      ratio_pre_hi.append(0.0)
      ratio_pre_lo.append(0.0)

    if (n_all_post>0.0):
      ratio_post.append(ndata/n_all_post)
      ratio_post_hi.append(ndata*e_data_hi/n_all_post)
      ratio_post_lo.append(ndata*e_data_lo/n_all_post)      
    else:
      ratio_post.append(0.0)
      ratio_post_hi.append(0.0)
      ratio_post_lo.append(0.0)

  a_met = array("d", met)
  v_met = TVectorD(len(a_met),a_met)
          
  a_dmet = array("d", dmet)
  v_dmet = TVectorD(len(a_dmet),a_dmet)
    
  a_ratio_pre = array("d", ratio_pre)
  a_ratio_pre_hi = array("d", ratio_pre_hi)
  a_ratio_pre_lo = array("d", ratio_pre_lo)
  
  v_ratio_pre = TVectorD(len(a_ratio_pre),a_ratio_pre)
  v_ratio_pre_hi = TVectorD(len(a_ratio_pre_hi),a_ratio_pre_hi)
  v_ratio_pre_lo = TVectorD(len(a_ratio_pre_lo),a_ratio_pre_lo)

  a_ratio_post = array("d", ratio_post)
  a_ratio_post_hi = array("d", ratio_post_hi)
  a_ratio_post_lo = array("d", ratio_post_lo)

  v_ratio_post = TVectorD(len(a_ratio_post),a_ratio_post)
  v_ratio_post_hi = TVectorD(len(a_ratio_post_hi),a_ratio_post_hi)
  v_ratio_post_lo = TVectorD(len(a_ratio_post_lo),a_ratio_post_lo)

  g_ratio_pre = TGraphAsymmErrors(v_met,v_ratio_pre,v_dmet,v_dmet,v_ratio_pre_lo,v_ratio_pre_hi)
  g_ratio_pre.SetLineColor(2)
  g_ratio_pre.SetMarkerColor(2)
  g_ratio_pre.SetMarkerStyle(20)

  g_ratio_post = TGraphAsymmErrors(v_met,v_ratio_post,v_dmet,v_dmet,v_ratio_post_lo,v_ratio_post_hi)
  g_ratio_post.SetLineColor(4)
  g_ratio_post.SetMarkerColor(4)
  g_ratio_post.SetMarkerStyle(20)
  
  ratiosys = h_postfit['totalv2'].Clone();
  for hbin in range(0,ratiosys.GetNbinsX()+1): 
        
    ratiosys.SetBinContent(hbin+1,1.0)
    if (h_postfit['totalv2'].GetBinContent(hbin+1)>0):
      ratiosys.SetBinError(hbin+1,h_postfit['totalv2'].GetBinError(hbin+1)/h_postfit['totalv2'].GetBinContent(hbin+1))

    else:
      ratiosys.SetBinError(hbin+1,0)


  dummy2 = TH1F("dummy2","dummy2",len(binLowE)-1,array('d',binLowE))
  for i in range(1,dummy2.GetNbinsX()):
    dummy2.SetBinContent(i,1.0)
  dummy2.GetYaxis().SetTitle("Data / Pred.")
  dummy2.GetXaxis().SetTitle("Recoil [GeV]")
  dummy2.SetLineColor(0)
  dummy2.SetMarkerColor(0)
  dummy2.SetLineWidth(0)
  dummy2.SetMarkerSize(0)
  dummy2.GetYaxis().SetLabelSize(0.03)
  dummy2.GetYaxis().SetNdivisions(5);
  dummy2.GetXaxis().SetNdivisions(510)
  dummy2.GetYaxis().CenterTitle()
  dummy2.GetYaxis().SetTitleSize(0.04)
  dummy2.GetYaxis().SetTitleOffset(1.5)

  dummy2.SetMaximum(2)
  dummy2.SetMinimum(0)
  dummy2.Draw("hist")

  ratiosys.SetFillColor(kGray) #SetFillColor(ROOT.kYellow)
  ratiosys.SetLineColor(kGray) #SetLineColor(1)
  ratiosys.SetLineWidth(1)
  ratiosys.SetMarkerSize(0)
  ratiosys.Draw("e2same")

  f1 = TF1("f1","1",-5000,5000);
  f1.SetLineColor(1);
  f1.SetLineStyle(2);
  f1.SetLineWidth(2);
  f1.Draw("same")

  if not blind:
    g_ratio_pre.Draw("epsame")
    g_ratio_post.Draw("epsame")
    legend2 = TLegend(.65,.25,.8,.29)
    legend3 = TLegend(.8,.25,.95,.29)
    legend2.AddEntry(g_ratio_pre,"pre-fit","elp")
    legend3.AddEntry(g_ratio_post,"post-fit","elp")
    for l in [legend2,legend3]:
      l.SetShadowColor(0);
      l.SetFillColor(0);
      l.SetFillStyle(0)
      l.SetBorderSize(0)
      l.SetLineColor(0);
      l.Draw()

  plotDir = plotConfig.plotDir
  label = region+'_'
  label += cat.replace('category_','')

  for ext in ['pdf','png','C']:
    c.SaveAs(plotDir+"sbStackedPostfit%s_"%plotextralabel+label+"."+ext)

  #c.SaveAs("test.pdf")

  #del c
  #del process
  #del colors
  #del h_prefit


# plotPreFitPostFit("singlemuonw",combinecat="tight_")
# plotPreFitPostFit("singlemuontop",combinecat="tight_")
# plotPreFitPostFit("dimuon",combinecat="tight_")
# plotPreFitPostFit("photon",combinecat="tight_")
# plotPreFitPostFit("singleelectronw",combinecat="tight_")
# plotPreFitPostFit("singleelectrontop",combinecat="tight_")
# plotPreFitPostFit("dielectron",combinecat="tight_")
plotPreFitPostFit("signal",combinecat="tight_",blind=False)

# plotPreFitPostFit("singlemuonw","category_monotop_loose",combinecat="loose_")
# plotPreFitPostFit("singlemuontop","category_monotop_loose",combinecat="loose_")
# plotPreFitPostFit("dimuon","category_monotop_loose",combinecat="loose_")
# plotPreFitPostFit("photon","category_monotop_loose",combinecat="loose_")
# plotPreFitPostFit("singleelectronw","category_monotop_loose",combinecat="loose_")
# plotPreFitPostFit("singleelectrontop","category_monotop_loose",combinecat="loose_")
# plotPreFitPostFit("dielectron","category_monotop_loose",combinecat="loose_")
plotPreFitPostFit("signal","category_monotop_loose",combinecat="loose_",blind=False)

