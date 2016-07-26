from ROOT import TCanvas, TGraph, TGraphAsymmErrors, TLegend, TLatex, TMarker, TFile, TTree, TH2D
from array import array
from sys import argv,stdout
from tdrStyle import *
import plotConfig
from glob import glob 

setTDRStyle()

VERBOSE=False

resonantXsecs = {
  900 : 3.09067,
  1100 : 1.307,
  1300 : 0.6149,
  1500 : 0.314,
  1700 : 0.1699,
  1900 : 0.0962,
  2100 : 0.05673,
  2300 : 0.03456,
  2500 : 0.02148,
  2700 : 0.01375,
  2900 : 0.008956,
    }

fcncXsecs = {
  50 : 2223,
  100 :  750.4,
  150 :  370.85,
  200 :  187.1545,
  300 :  48.4024,
  500 :  9.23265,
  700 :  2.836662,
  900 :  1.098356,
  1100 : 0.4855015,
  1300 : 0.2350739,
  1500 : 0.12218969,
  1700 : 0.06657825,
  1900 : 0.03860199,
  2100 : 0.02303869,
    }

BLIND=False

class Limit():
  def __init__(self,mMed,mChi,xsec):
    self.mMed=mMed
    self.mChi=mChi
    self.xsec=xsec
    self.cent=0
    self.up1=0
    self.up2=0
    self.down1=0
    self.down2=0
    self.obs=0

def findIntersect1D(g1,g2,x1,x2):
  orientation = (g1.Eval(x1)<g2.Eval(x1))
  for iX in xrange(1000):
    x = (x2-x1)*iX/1000.+x1
    if orientation != (g1.Eval(x)<g2.Eval(x)):
      # return TGraph(1,array('f',[x]),array('f',[g1.Eval(x)]))
      return TMarker(x,g1.Eval(x),1)
      # return x
  print 'Could not find intersection!'
  return None


def makePlot1D(filepath,foutname,plottitle='',masstitle='',scale=False):
  xsecs = resonantXsecs if 'Resonant' in plottitle else fcncXsecs
  limits = {} # mMed : Limit

  runObs=(not BLIND)
  filelist = glob(filepath)
  maxval = 0; minval = 999
  for f in filelist:
    ff = f.split('_')
    mMed = int(ff[1])
    mChi = int(ff[2].split('.')[0])
    xsec = xsecs[mMed]
    if scale:
      l = Limit(mMed,mChi,1)
    else:
      l = Limit(mMed,mChi,xsec)
    fin = TFile(f)
    t = fin.Get('limit')
    nL = t.GetEntries()
    if nL<6:
      runObs=False
    limitNames = ['down2','down1','cent','up1','up2','obs']
    for iL in xrange(nL):
      t.GetEntry(iL)
      val = t.limit
      if scale:
        val /= xsec
      maxval = max(maxval,val)
      minval = min(minval,val)
      setattr(l,limitNames[iL],val)
    limits[mMed] = l
    fin.Close()

  xaxis = []; xseclist = []
  cent = []; obs = []
  up1 = []; up2 = []
  down1 = []; down2 = []
  for m in sorted(limits):
    l = limits[m]
    xaxis.append(m)
    xseclist.append(l.xsec)
    cent.append(l.cent)
    up1.append(l.up1-l.cent)
    up2.append(l.up2-l.cent)
    down1.append(l.cent-l.down1)
    down2.append(l.cent-l.down2)
    if runObs:
      obs.append(l.obs)


  N = len(xaxis)
  
  up1Sigma = array('f',up1)
  up2Sigma = array('f',up2)
  down1Sigma = array('f',down1)
  down2Sigma = array('f',down2)
  cent = array('f',cent)
  if runObs:
    obs = array('f',obs)
  xarray = array('f',xaxis)
  xsecarray = array('f',xseclist)
  zeros = array('f',[0 for i in xrange(N)])

  graphXsec = TGraph(N,xarray,xsecarray)

  graphCent = TGraph(N,xarray,cent)
  if runObs:
    graphObs = TGraph(N,xarray,obs)
  graph1Sigma = TGraphAsymmErrors(N,xarray,cent,zeros,zeros,down1Sigma,up1Sigma)
  graph2Sigma = TGraphAsymmErrors(N,xarray,cent,zeros,zeros,down2Sigma,up2Sigma)

  c = TCanvas('c','c',700,600)
  c.SetLogy()
  c.SetLeftMargin(.15)

  graph2Sigma.GetXaxis().SetTitle(masstitle+' [GeV]')
  if scale:
    graph2Sigma.GetYaxis().SetTitle('Upper limit [#sigma/#sigma_{theory}]')  
  else:
    graph2Sigma.GetYaxis().SetTitle("Upper limit [#sigma] [pb]")  
  graph2Sigma.SetLineColor(5)
  graph1Sigma.SetLineColor(3)
  graph2Sigma.SetFillColor(5)
  graph1Sigma.SetFillColor(3)
  graph2Sigma.SetMinimum(0.5*minval)
  if scale:
    graph2Sigma.SetMaximum(10*max(maxval,max(xsecarray),4))
  else:
    graph2Sigma.SetMaximum(10*max(maxval,max(xsecarray)))
  graphCent.SetLineWidth(2)
  graphCent.SetLineStyle(2)
  if runObs:
    graphObs.SetLineColor(1)
    graphObs.SetLineWidth(3)
  graph1Sigma.SetLineStyle(0)
  graph2Sigma.SetLineStyle(0)
 
  leg = TLegend(0.55,0.7,0.9,0.9)
  leg.AddEntry(graphCent,'Expected','L')
  if runObs:
    leg.AddEntry(graphObs,'Observed','L')
  leg.AddEntry(graph1Sigma,'1 #sigma','F')
  leg.AddEntry(graph2Sigma,'2 #sigma','F')
  leg.SetFillStyle(0)
  leg.SetBorderSize(0)

  graph2Sigma.Draw('A3')
  graph1Sigma.Draw('3 same')
  graphCent.Draw('same L')
  if runObs:
    graphObs.Draw('same L')

  subscript = 'SR' if 'Resonant' in plottitle else 'FC'
  coupling = '0.1' if 'Resonant' in plottitle else '0.25'

  graphXsec.SetLineColor(2)
  graphXsec.SetLineWidth(2)
  graphXsec.SetLineStyle(2)
  graphXsec.Draw('same L')
  if scale:
    graphOne.SetLineColor(2)
    graphOne.SetLineWidth(2)
    graphOne.SetLineStyle(2)
    graphOne.Draw('same L')
  else:
    graphXsec.SetLineColor(2)
    if 'Resonant' in plottitle:
      leg.AddEntry(graphXsec,'Theory #splitline{a_{%s}=b_{%s}=%s}{m_{#chi}=100 GeV}'%(subscript,subscript,coupling),'l')
    else:
      leg.AddEntry(graphXsec,'Theory #splitline{a_{%s}=b_{%s}=%s}{m_{#chi}=10 GeV}'%(subscript,subscript,coupling),'l')
  if runObs:
    obslimit = findIntersect1D(graphObs,graphXsec,xaxis[0],xaxis[-1])
    if obslimit:
      obslimit.SetMarkerStyle(29); obslimit.SetMarkerSize(3)
      obslimit.Draw('p same')
  explimit = findIntersect1D(graphCent,graphXsec,xaxis[0],xaxis[-1])
  if explimit:
    explimit.SetMarkerStyle(30); explimit.SetMarkerSize(3)
    explimit.Draw('p same')

  leg.Draw()

  label = TLatex()
  label.SetNDC()
  label.SetTextFont(62)
  label.SetTextAlign(11)
  label.DrawLatex(0.19,0.85,"CMS")
  label.SetTextFont(52)
  label.DrawLatex(0.28,0.85,"Preliminary")
  label.SetTextFont(42)
  label.SetTextSize(0.6*c.GetTopMargin())
  label.DrawLatex(0.19,0.77,plottitle)
  if scale:
    if 'Resonant' in plottitle:
      label.DrawLatex(0.19,0.7,"a_{SR} = b_{SR} = %s"%coupling)
      label.DrawLatex(0.19,0.64,"m_{#chi}=100 GeV")
    else:
      label.DrawLatex(0.19,0.7,"a_{FC} = b_{FC} = %s"%coupling)
      label.DrawLatex(0.19,0.64,"m_{#chi}=10 GeV")
  label.SetTextSize(0.5*c.GetTopMargin())
  label.SetTextFont(42)
  label.SetTextAlign(31) # align right
  label.DrawLatex(0.9, 0.94,"%.1f fb^{-1} (13 TeV)"%(plotConfig.lumi))

  c.SaveAs(foutname+'.pdf')
  c.SaveAs(foutname+'.png')

plotsdir = plotConfig.plotDir

makePlot1D('../datacards/scan/higgsCombinefcnc_*_10.Asymptotic.mH120.root',plotsdir+'test_fcncv3_obs_limits_xsec','#splitline{Flavor-changing}{neutral current}','M_{V}')
# makePlot('../datacards/fcncv3_obs_limits.txt',plotsdir+'fcncv3_obs_limits','#splitline{Flavor-changing}{neutral current}','M_{V}',True)
# makePlot('../datacards/resonantv3_obs_limits.txt',plotsdir+'resonantv3_obs_limits_xsec','#splitline{Resonant}{production}','M_{#phi}')
# makePlot('../datacards/resonantv3_obs_limits.txt',plotsdir+'resonantv3_obs_limits','#splitline{Resonant}{production}','M_{#phi}',True)
