from ROOT import TCanvas, TGraph, TGraphAsymmErrors, TLegend, TLatex, TFile, TTree, TH2D, TGraph2D
import ROOT as root
from array import array
from sys import argv,stdout
from tdrStyle import *
import plotConfig
from glob import glob 

setTDRStyle()

XSECUNCERT=0.2
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
  3100 : 0.00598399,
  3300 : 0.0040608,
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

def parseLimitFiles2D(filepath,xsecs=None):
  # returns a dict (mMed,mChi) : Limit
  # if xsecs=None, Limit will have absolute xsec
  # if xsecs=dict of xsecs, Limit will have mu values
  limits = {}
  filelist = glob(filepath)
  for f in filelist:
    ff = f.split('_')
    mMed = int(ff[1])
    mChi = int(ff[2].split('.')[0])
    mChi = int(ff[2].split('.')[0])
    if xsecs:
      xsec = xsecs[mMed]
      # xsec = xsecs[(mMed,mChi)] #FIXME
    else:
      xsec=1
    l = Limit(mMed,mChi,xsec)
    fin = TFile(f)
    t = fin.Get('limit')
    nL = t.GetEntries()
    limitNames = ['down2','down1','cent','up1','up2','obs']
    for iL in xrange(nL):
      t.GetEntry(iL)
      val = t.limit
      val /= xsec
      setattr(l,limitNames[iL],val)
    limits[(mMed,mChi)] = l
    fin.Close()
  return limits

def makePlot2D(filepath,foutname,medcfg,chicfg,offshell=True):
  xsecs = fcncXsecs # FIXME
  limits = parseLimitFiles2D(filepath,xsecs)
  gs = {}
  for g in ['exp','expup','expdown','obs','obsup','obsdown']:
    gs[g] = TGraph2D()

  iP=0
  for p in limits:
    mMed = p[0]; mChi = p[1]
    l = limits[p]
    gs['exp'].SetPoint(iP,mMed,mChi,l.cent)
    gs['expup'].SetPoint(iP,mMed,mChi,l.up1)
    gs['expdown'].SetPoint(iP,mMed,mChi,l.down1)
    gs['obs'].SetPoint(iP,mMed,mChi,l.obs)
    gs['obsup'].SetPoint(iP,mMed,mChi,l.obs/(1-XSECUNCERT))
    gs['obsdown'].SetPoint(iP,mMed,mChi,l.obs/(1+XSECUNCERT))
    iP += 1

  hs = {}
  for h in ['exp','expup','expdown','obs','obsup','obsdown']:
    hs[h] = TH2D(h,h,medcfg[0],medcfg[1],medcfg[2],chicfg[0],chicfg[1],chicfg[2])
    # hs[h].SetStats(0); hs[h].SetTitle('')
    for iX in xrange(0,medcfg[0]):
      for iY in xrange(0,chicfg[0]):
        x = medcfg[1] + (medcfg[2]-medcfg[1])*iX/medcfg[0]
        y = chicfg[1] + (chicfg[2]-chicfg[1])*iY/chicfg[0]
        if not(offshell) and 2*y>x:
          continue
        hs[h].SetBinContent(iX+1,iY+1,gs[h].Interpolate(x,y))
        # if h=='obs':
        #   print iX+1,iY+1,x,y,gs[h].Interpolate(x,y)

  hs['obsclone'] = hs['obs'].Clone() # clone it so we can draw with different settings
  for h in ['exp','expup','expdown','obsclone','obsup','obsdown']:
    hs[h].SetContour(2)
    hs[h].SetContourLevel(1,1)
    for iX in xrange(1,medcfg[0]+1):
      for iY in xrange(1,chicfg[0]+1):
        if hs[h].GetBinContent(iX,iY)<=0:
          hs[h].SetBinContent(iX,iY,100)

  canvas = ROOT.TCanvas("canvas", "canvas", 1000, 800)
  canvas.SetLogz()

  frame = canvas.DrawFrame(300,10,2100,500,"")

  frame.GetYaxis().CenterTitle();
  frame.GetYaxis().SetTitle("m_{DM} [GeV]");
  frame.GetXaxis().SetTitle("M_{MED} [GeV]");
  frame.GetXaxis().SetTitleOffset(1.15);
  frame.GetYaxis().SetTitleOffset(1.15);

  root.gStyle.SetLabelSize(0.035,"X");
  root.gStyle.SetLabelSize(0.035,"Y");
  root.gStyle.SetLabelSize(0.035,"Z");

  frame.Draw()

  ##Color palette
  ncontours = 999;
  #root.TColor.InitializeColors();
  stops = [ 0.0000, 0.1250, 0.2500, 0.3750, 0.5000, 0.6250, 0.7500, 0.8750, 1.0000]
  red   = [ 243./255., 243./255., 240./255., 240./255., 241./255., 239./255., 186./255., 151./255., 129./255.]
  green = [   0./255.,  46./255.,  99./255., 149./255., 194./255., 220./255., 183./255., 166./255., 147./255.]
  blue  = [   6./255.,   8./255.,  36./255.,  91./255., 169./255., 235./255., 246./255., 240./255., 233./255.]

  stopsArray = array('d',stops)
  redArray   = array('d',red)
  greenArray = array('d',green)
  blueArray  = array('d',blue)

  root.TColor.CreateGradientColorTable(9, stopsArray, redArray, greenArray, blueArray, ncontours);
  root.gStyle.SetNumberContours(ncontours);

  hs['obs'].SetMinimum(0.01)
  hs['obs'].SetMaximum(10.)

  hs['obs'].Draw("COLZ SAME")

  hs['obsclone'].SetLineStyle(1)
  hs['obsclone'].SetLineWidth(3)
  hs['obsclone'].SetLineColor(2)
  hs['obsclone'].Draw('CONT3 SAME')

  hs['exp'].SetLineStyle(1)
  hs['exp'].SetLineWidth(2)
  hs['exp'].SetLineColor(1)
  hs['exp'].Draw('CONT3 SAME')

  root.gPad.SetRightMargin(0.15);
  root.gPad.SetTopMargin(0.05);
  root.gPad.SetBottomMargin(0.15);
  root.gPad.RedrawAxis();
  root.gPad.Modified(); 
  root.gPad.Update();

  canvas.SaveAs(foutname+'.root')
  canvas.SaveAs(foutname+'.pdf')
  canvas.SaveAs(foutname+'.png')

plotsdir = plotConfig.plotDir

# makePlot2D('../datacards/scan/higgsCombinefcnc_*.Asymptotic.mH120.root',plotsdir+'fcnc2d',(10,300.,2100.),(10,10.,500.),True)
makePlot2D('../datacards/scan/higgsCombinefcnc_*.Asymptotic.mH120.root',plotsdir+'fcnc2d',(100,300.,2100.),(100,10.,500.),True)
