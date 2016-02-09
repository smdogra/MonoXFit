#!/usr/bin/env python

import ROOT as root

fIn = root.TFile.Open('../mono-x.root')
fdir = fIn.Get('category_monotop')
signals = [
           ('Mchi900' ,'M_{V}=900 GeV',2),
           ('Mchi500' ,'M_{V}=500 GeV',1),
           ('Mchi300' ,'M_{V}=300 GeV',0),
           ('Mres1300_Mchi100' ,'M_{S}=1.3 TeV, M_{#chi}=100 GeV',2),
           ('Mres1100_Mchi100' ,'M_{S}=1.1 TeV, M_{#chi}=100 GeV',1),
           ('Mres900_Mchi100' ,'M_{S}=0.9 TeV, M_{#chi}=100 GeV',0),
           ]

signals.reverse()

c = root.TCanvas('c','c',800,900)
c.SetTopMargin(0.01)
c.SetLeftMargin(0.12)
c.SetRightMargin(0.01)
leg = root.TLegend(.55,.7,.98,.98)
leg.SetFillStyle(0)
leg.SetBorderSize(0)
binwidths = [50,50,50,100,100,400]
colors = [root.kRed, root.kBlue, root.kBlack]
drawn=False
for sig in signals:
  k = sig[0]
  label = sig[1]
  num = sig[2]
  hsig = fdir.Get('signal_'+k)
  hsig.SetLineColor(colors[num])
  hsig.SetLineWidth(2)
  for iB in xrange(hsig.GetNbinsX()):
    val = hsig.GetBinContent(iB+1)
    hsig.SetBinContent(iB+1,val/binwidths[iB])
  if label.find('chi')>=0:
    hsig.SetLineStyle(2)
  if not drawn:
    drawn=True
    hsig.SetStats(0)
    hsig.SetTitle('')
    hsig.GetXaxis().SetTitle('MET [GeV]')
    hsig.GetYaxis().SetTitle('Events/GeV')
    hsig.Draw('hist')
  else:
    hsig.Draw('hist same')
  leg.AddEntry(hsig,label,'l')

leg.Draw()
c.SaveAs('~/www/figs/monotop/fits/signals.png')
c.SaveAs('~/www/figs/monotop/fits/signals.pdf')
c.SaveAs('~/www/figs/monotop/fits/signals.C')



