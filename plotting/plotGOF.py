#!/usr/bin/env python

import ROOT as root
from tdrStyle import *
from array import array 

setTDRStyle()

fIn = root.TFile.Open('~/scratch5/root/gof4/toys.root')
limits = fIn.Get('limit')
realVal = 2*2.644
#realVal = 14.75
#realVal = 5.34
maxVal = 25 # just histogram binning
nbins=500

c = root.TCanvas()
c.SetLeftMargin(0.15)
leg = root.TLegend(.55,.7,.9,.9)
leg.SetFillStyle(0)
leg.SetBorderSize(0)

htoys = root.TH1F('htoys','htoys',nbins,0,maxVal)
limits.Draw('2*deltaNLL>>htoys','quantileExpected==-1','')
htoys.SetLineColor(root.kBlack)
realBin = htoys.FindBin(realVal)
pval = htoys.Integral(realBin,nbins+1)/htoys.Integral(0,nbins+1)
print 'p-val:',pval

hshaded = htoys.Clone('hshaded')
hshaded.SetFillColor(root.kRed)
hshaded.SetFillStyle(3004)
for iB in xrange(realBin,nbins+1):
  hshaded.SetBinContent(iB,0)

htoys.SetMaximum(1.5*htoys.GetMaximum())
htoys.GetXaxis().SetTitle('2 ln #lambda')
htoys.GetYaxis().SetTitle('Toys')
htoys.GetYaxis().SetTitleOffset(1.5)
htoys.Draw('hist')
hshaded.Draw('hist same')

leg.AddEntry(htoys,"Toy distribution","l")
leg.AddEntry(hshaded,"Area below real data","F")

latex2 = root.TLatex()
latex2.SetNDC()
latex2.SetTextSize(0.5*c.GetTopMargin())
latex2.SetTextFont(42)
latex2.SetTextAlign(31) # align right
latex2.DrawLatex(0.9, 0.94,"2.26 fb^{-1} (13 TeV)")
latex2.SetTextSize(0.6*c.GetTopMargin())
latex2.SetTextFont(62)
latex2.SetTextAlign(11) # align right
latex2.DrawLatex(0.19, 0.85, "CMS")
latex2.SetTextSize(0.5*c.GetTopMargin())
latex2.SetTextFont(52)
latex2.SetTextAlign(11)
latex2.DrawLatex(0.28, 0.85, "Preliminary")          
latex2.SetTextFont(42)
latex2.DrawLatex(0.19, 0.8, "p-value: %.3f"%pval)
#latex2.DrawLatex(0.19, 0.8, "Z#rightarrowee scale floated")


leg.Draw()
baseName = '~/public_html/figs/monotop/fits_wcr/gof4'
c.SaveAs(baseName+'.png')
c.SaveAs(baseName+'.pdf')
c.SaveAs(baseName+'.C')



