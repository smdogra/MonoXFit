from ROOT import TCanvas, TGraph, TGraphAsymmErrors, TLegend, TLatex
from array import array
from sys import argv
from tdrStyle import *
setTDRStyle()

def parseLine(l):
  if 'Observed' in l:
    return 'Observed',float(l.split('<')[1])
  return float(l.split()[1].strip(':%')),float(l.split('<')[1])

def makePlot(finname,foutname,plottitle='',masstitle=''):
  points = {}
  cls = [2.5, 16, 50, 84, 97.5,'Observed']
  xaxis = []
  for cl in cls:
    points[cl] = []
  for l in open(finname):
    try:
      if l.strip()[0]=='#':
        continue
      if 'MASS' in l:
        xaxis.append(float(l.split()[1]))
      else:
        cl,val = parseLine(l)
        points[cl].append(val)
    except:
      pass
  
  N = len(xaxis)
  up1Sigma=[]; up2Sigma=[]
  down1Sigma=[]; down2Sigma=[]
  for iM in xrange(N):
    up1Sigma.append(points[84][iM]-points[50][iM])
    up2Sigma.append(points[97.5][iM]-points[50][iM])
    down1Sigma.append(-points[16][iM]+points[50][iM])
    down2Sigma.append(-points[2.5][iM]+points[50][iM])
  
  up1Sigma = array('f',up1Sigma)
  up2Sigma = array('f',up2Sigma)
  down1Sigma = array('f',down1Sigma)
  down2Sigma = array('f',down2Sigma)
  cent = array('f',points[50])
  obs = array('f',points['Observed'])
  xarray = array('f',xaxis)
 
  #print up2Sigma
  #print cent
  #print down2Sigma
  zeros = array('f',[0 for i in xrange(N)])
  graphCent = TGraph(N,xarray,cent)
  graphObs = TGraph(N,xarray,obs)
  graph1Sigma = TGraphAsymmErrors(N,xarray,cent,zeros,zeros,down1Sigma,up1Sigma)
  graph2Sigma = TGraphAsymmErrors(N,xarray,cent,zeros,zeros,down2Sigma,up2Sigma)
  c = TCanvas('c','c',700,600)
  c.SetLeftMargin(.15)
  graph2Sigma.GetXaxis().SetTitle(masstitle+'Mass [GeV]')
  graph2Sigma.GetYaxis().SetTitle('Upper limit [pb]')
  graph2Sigma.GetYaxis().SetTitleOffset(1.5)
  graph2Sigma.SetLineColor(5)
  graph1Sigma.SetLineColor(3)
  graph2Sigma.SetFillColor(5)
  graph1Sigma.SetFillColor(3)
  graph2Sigma.SetMinimum(0)
  graph2Sigma.SetMaximum(1.5*max(points[97.5]))
  graphCent.SetLineStyle(2)
  graphObs.SetLineColor(1)
  graphObs.SetLineWidth(2)
  graph1Sigma.SetLineStyle(0)
  graph2Sigma.SetLineStyle(0)
 
  leg = TLegend(0.7,0.7,0.9,0.9)
  leg.AddEntry(graphCent,'Expected','L')
  leg.AddEntry(graphObs,'Observed','L')
  leg.AddEntry(graph1Sigma,'1 #sigma','F')
  leg.AddEntry(graph2Sigma,'2 #sigma','F')
  leg.SetFillStyle(0)
  leg.SetBorderSize(0)

  graph2Sigma.Draw('A3')
  graph1Sigma.Draw('3 same')
  graphCent.Draw('same L')
  graphObs.Draw('same L')
  leg.Draw()
  label = TLatex()
  label.SetNDC()
  label.SetTextFont(62)
  label.SetTextAlign(11)
  label.DrawLatex(0.19,0.85,"CMS")
  label.SetTextFont(52)
  label.DrawLatex(0.28,0.85,"Preliminary")
  label.SetTextFont(42)
  label.DrawLatex(0.19,0.75,plottitle)
  label.SetTextSize(0.5*c.GetTopMargin())
  label.SetTextFont(42)
  label.SetTextAlign(31) # align right
  label.DrawLatex(0.9, 0.94,"2.26 fb^{-1} (13 TeV)")
  c.SaveAs(foutname+'.pdf')
  c.SaveAs(foutname+'.png')

makePlot('../datacards/fcnc_obs_limits.txt','~/public_html/figs/monotop/fits_wcr/fcnc_obs_limits','#splitline{Flavor-changing}{neutral current}','DM ')
makePlot('../datacards/resonant_obs_limits.txt','~/public_html/figs/monotop/fits_wcr/resonant_obs_limits','Resonant production','Mediator ')
