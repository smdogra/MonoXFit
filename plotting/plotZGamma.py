#!/usr/bin/env python

import ROOT as root
from tdrStyle import *
from array import array 

setTDRStyle()

fFile = root.TFile.Open('../mono-x.root')
fIn = fFile.Get('category_monotop')

c = root.TCanvas()
leg = root.TLegend(.55,.7,.9,.9)
leg.SetFillStyle(0)
leg.SetBorderSize(0)

hZll = fIn.Get('dimuon_zll')
hZllData = fIn.Get('dimuon_data')
hPhoton = fIn.Get('photon_gjets')
hPhotonData = fIn.Get('photon_data')

hMC = hZll.Clone('hMCRatio'); hMC.Divide(hPhoton);
hMCErr = hMC.Clone('hMCRatioErr')
hData = hZllData.Clone('hDataRatio'); hData.Divide(hPhotonData)

hMCErr.SetLineColor(0)
hMCErr.SetFillColor(root.kBlack)
hMCErr.SetFillStyle(3004)
hMC.SetLineColor(root.kBlue)
hData.SetLineColor(root.kBlack)

hData.SetMaximum(2*hData.GetMaximum())
hData.Draw('elp')
hMCErr.Draw('e2 same')
hMC.Draw('hist same')

leg.AddEntry(hData,"Z#rightarrowll/#gamma [Data]","elp")
leg.AddEntry(hMC,"Z#rightarrowll/#gamma [MC]","l")
leg.AddEntry(hMCErr,"stat. uncert.","f")

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

leg.Draw()
baseName = '~/public_html/figs/monotop/fits_wcr/zgamma_ratio'
print c
c.SaveAs(baseName+'.png')
c.SaveAs(baseName+'.pdf')
c.SaveAs(baseName+'.C')



