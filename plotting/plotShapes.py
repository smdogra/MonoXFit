#!/usr/bin/env python

import ROOT as root

fTemplates = root.TFile('combined_model.root')

counter=0

def mycanvas():
  global counter
  counter += 1
  return root.TCanvas('c%i'%(counter),'c%i'%(counter),600,600)


def getDivided(dirname,central,uncert,linecolor):
  fTemplates.cd(dirname)
  centralHist = fTemplates.Get(dirname+central)
#  print central+'_'+uncert+'_Up'
#  fTemplates.ls()
  upHist = fTemplates.Get(dirname+central+'_'+uncert+'_Up')
  downHist = fTemplates.Get(dirname+central+'_'+uncert+'_Down')
#  print centralHist,upHist
  upDivided = upHist.Clone(); upDivided.Divide(centralHist)
  downDivided = downHist.Clone(); downDivided.Divide(centralHist)
  maxval = 1+2*(max(upDivided.GetMaximum(),downDivided.GetMaximum())-1)
  minval = 1-1.2*(1-min(upDivided.GetMinimum(),downDivided.GetMinimum()))
  #maxval = 1.4*max(upDivided.GetMaximum(),downDivided.GetMaximum())
  #minval = 0.8*min(upDivided.GetMinimum(),downDivided.GetMinimum())
  for hist in [upDivided,downDivided]:
    hist.SetLineColor(linecolor)
    hist.SetStats(0)
    hist.SetMaximum(maxval)
    hist.SetMinimum(minval)
    hist.SetLineWidth(2)
  return upDivided,downDivided

def getBinDivided(dirname,central,uncert,linecolor):
  centralHist = fTemplates.Get(dirname+central)
  upDivided = centralHist.Clone()
  downDivided = centralHist.Clone()
  for iB in xrange(centralHist.GetNbinsX()):
    upHist = fTemplates.Get(dirname+central+'_'+uncert+'_bin%i_Up'%(iB))
    downHist = fTemplates.Get(dirname+central+'_'+uncert+'_bin%i_Down'%(iB))
    upDivided.SetBinContent(iB+1,upHist.GetBinContent(iB+1))
    downDivided.SetBinContent(iB+1,downHist.GetBinContent(iB+1))
  upDivided.Divide(centralHist)
  downDivided.Divide(centralHist)
  maxval = 1+2*(max(upDivided.GetMaximum(),downDivided.GetMaximum())-1)
  minval = 1-1.2*(1-min(upDivided.GetMinimum(),downDivided.GetMinimum()))
  for hist in [upDivided,downDivided]:
    hist.SetLineColor(linecolor)
    hist.SetStats(0)
    hist.SetMaximum(maxval)
    hist.SetMinimum(minval)
    hist.SetLineWidth(2)
  return upDivided,downDivided

phocanvas = mycanvas()
dirname = 'Z_constraints_category_monotop/'
central = 'photon_weights_monotop'
leg = root.TLegend(0.7,0.7,0.9,0.9)
upren,downren = getDivided(dirname,central,'renscale',1)
upren.SetTitle('Shape variations (Z#rightarrow#nu#nu/#gamma)')
upren.Draw('hist'); downren.Draw('hist same')
leg.AddEntry(upren,'renscale','L')

upfac,downfac = getDivided(dirname,central,'facscale',2)
upfac.Draw('hist same'); downfac.Draw('hist same')
leg.AddEntry(upfac,'facscale','L')

uppdf,downpdf = getDivided(dirname,central,'pdf',3)
uppdf.Draw('hist same'); downpdf.Draw('hist same')
leg.AddEntry(uppdf,'PDF','L')

upbtag,downbtag = getDivided(dirname,central,'btag',6)
upbtag.Draw('hist same'); downbtag.Draw('hist same')
leg.AddEntry(upbtag,'b-tag','L')

upmistag,downmistag = getDivided(dirname,central,'mistag',7)
upmistag.Draw('hist same'); downmistag.Draw('hist same')
leg.AddEntry(upmistag,'b-mistag','L')

upewk,downewk = getBinDivided(dirname,central,'ewk_monotop',4)
upewk.Draw('hist same'); downewk.Draw('hist same')
leg.AddEntry(upewk,'EWK','L')

ones = upewk.Clone(); ones.Divide(upewk);
ones.SetLineStyle(2)
ones.SetLineColor(1)
ones.Draw('hist same')

leg.SetFillStyle(0)
leg.SetBorderSize(0)
leg.Draw()

phocanvas.SaveAs('~/public_html/figs/monotop/fits_smoothed/variations/phoshapes.png')
phocanvas.SaveAs('~/public_html/figs/monotop/fits_smoothed/variations/phoshapes.pdf')


###
zmmcanvas = mycanvas()
dirname = 'Z_constraints_category_monotop/'
central = 'zmm_weights_monotop'
leg = root.TLegend(0.7,0.7,0.9,0.9)

upbtag,downbtag = getDivided(dirname,central,'btag',6)
upbtag.SetTitle('Shape variations (Z#rightarrow#nu#nu/Z#rightarrow#mu#mu)')
upbtag.Draw('hist'); downbtag.Draw('hist same')
leg.AddEntry(upbtag,'b-tag','L')

upmistag,downmistag = getDivided(dirname,central,'mistag',7)
upmistag.Draw('hist same'); downmistag.Draw('hist same')
leg.AddEntry(upmistag,'b-mistag','L')

ones.Draw('hist same')

leg.SetFillStyle(0)
leg.SetBorderSize(0)
leg.Draw()

zmmcanvas.SaveAs('~/public_html/figs/monotop/fits_smoothed/variations/zmmshapes.png')
zmmcanvas.SaveAs('~/public_html/figs/monotop/fits_smoothed/variations/zmmshapes.pdf')

###
zeecanvas = mycanvas()
dirname = 'Z_constraints_category_monotop/'
central = 'zee_weights_monotop'
leg = root.TLegend(0.7,0.7,0.9,0.9)

upbtag,downbtag = getDivided(dirname,central,'btag',6)
upbtag.SetTitle('Shape variations (Z#rightarrow#nu#nu/Z#rightarrowee)')
upbtag.Draw('hist'); downbtag.Draw('hist same')
leg.AddEntry(upbtag,'b-tag','L')

upmistag,downmistag = getDivided(dirname,central,'mistag',7)
upmistag.Draw('hist same'); downmistag.Draw('hist same')
leg.AddEntry(upmistag,'b-mistag','L')

ones.Draw('hist same')

leg.SetFillStyle(0)
leg.SetBorderSize(0)
leg.Draw()

zeecanvas.SaveAs('~/public_html/figs/monotop/fits_smoothed/variations/zeeshapes.png')
zeecanvas.SaveAs('~/public_html/figs/monotop/fits_smoothed/variations/zeeshapes.pdf')

###

topencanvas = mycanvas()
dirname = 'Top_constraints_category_monotop/'
central = 'topen_weights_monotop'
leg = root.TLegend(0.7,0.85,0.9,0.9)
upbtag,downbtag = getDivided(dirname,central,'btag',6)
upbtag.SetTitle('Shape variations (t#bar{t}#rightarrowb(l)#nu/t#bar{t}#rightarrowbe#nu)')
upbtag.Draw('hist'); downbtag.Draw('hist same')
leg.AddEntry(upbtag,'btag','L')

ones.Draw('hist same')

leg.SetFillStyle(0)
leg.SetBorderSize(0)
leg.Draw()

topencanvas.SaveAs('~/public_html/figs/monotop/fits_smoothed/variations/topenshapes.png')
topencanvas.SaveAs('~/public_html/figs/monotop/fits_smoothed/variations/topenshapes.pdf')

###

topmncanvas = mycanvas()
dirname = 'Top_constraints_category_monotop/'
central = 'topmn_weights_monotop'
leg = root.TLegend(0.7,0.85,0.9,0.9)
upbtag,downbtag = getDivided(dirname,central,'btag',6)
upbtag.SetTitle('Shape variations (t#bar{t}#rightarrowb(l)#nu/t#bar{t}#rightarrowb#mu#nu)')
upbtag.Draw('hist'); downbtag.Draw('hist same')
leg.AddEntry(upbtag,'btag','L')

ones.Draw('hist same')

leg.SetFillStyle(0)
leg.SetBorderSize(0)
leg.Draw()

topmncanvas.SaveAs('~/public_html/figs/monotop/fits_smoothed/variations/topmnshapes.png')
topmncanvas.SaveAs('~/public_html/figs/monotop/fits_smoothed/variations/topmnshapes.pdf')





