#!/usr/bin/env python

import ROOT as root
from array import array
from re import sub

class Syst(object):
  def __init__(self,updownname):
    ll = updownname.split('_')
    N = len(ll)
    self.nominal = ''
    for l in ll[:N-1]:
      self.nominal += l+'_'
    self.nominal = self.nominal[:-1]
    systname = sub('Down','',sub('Up','',ll[N-1]))
    self.up = self.nominal+'_'+systname+'Up'
    self.down = self.nominal+'_'+systname+'Down'

def contains(s1,s2):
  if type(s2)==type(""):
    return s1.find(s2)>=0
  else:
    for s in s2:
      if s1.find(s)>=0:
        return True
    return False


def symmetrize(nominal,up,down,invert=False):
  nbins = nominal.GetNbinsX()
  for iB in xrange(1,nbins+1):
    shift = (up.GetBinContent(iB)-down.GetBinContent(iB))*0.5
    #print iB,shift,up.GetBinContent(iB), down.GetBinContent(iB)
    nominalVal = nominal.GetBinContent(iB)
    if invert and False:
      # for something like W CR, to keep things anticorrelated
      up.SetBinContent(iB,nominalVal-shift)
      down.SetBinContent(iB,nominalVal+shift)
    else:
      up.SetBinContent(iB,nominalVal+shift)
      down.SetBinContent(iB,nominalVal-shift)

def smooth(var,nominal,N=1):
  hist = var.Clone(); hist.SetName('tmp')
  hist.Divide(nominal)
  nbins = hist.GetNbinsX()
  vals = array('f',[0 for i in xrange(nbins)])
  for iB in xrange(1,nbins+1):
    if iB<=N or nbins-iB<N:
      continue
    tmpsum=0.
    for jB in xrange(iB-N,iB+N+1):
      tmpsum += hist.GetBinContent(jB)
    tmpsum /= (2*N+1)
    vals[iB-1] = tmpsum
  for iB in xrange(1,nbins+1):
    if iB<=N or nbins-iB<N:
      continue
    var.SetBinContent(iB,vals[iB-1]*nominal.GetBinContent(iB))

baseIn = root.TFile.Open('mono-x.root','UPDATE')
fIn = baseIn.Get('category_monotop')
#fOut = root.TFile.Open('smoothed.root','RECREATE')
#systNames = ['zjets_zjethf','gjets_gjethf','wjets_wjethf']
systNames = ['zjethf','gjethf','wjethf']
shapes = {}

keys = fIn.GetListOfKeys()
nKeys = keys.GetEntries()
for iK in xrange(nKeys):
  key = keys.At(iK).GetName()
  if contains(key,systNames):
    newSyst = Syst(key)
    if newSyst.up not in shapes:
      shapes[newSyst.up] = newSyst

for name,syst in shapes.iteritems():
  print name
  nominal = fIn.Get(syst.nominal)
  up = fIn.Get(syst.up)
  down = fIn.Get(syst.down)
  for i in xrange(1):
    smooth(up,nominal)
    smooth(down,nominal)
  symmetrize(nominal,up,down,contains(syst.nominal,['singlemuonw','singleelectronw']))
  fIn.WriteTObject(nominal)
  fIn.WriteTObject(up)
  fIn.WriteTObject(down)
#  fOut.WriteTObject(nominal)
#  fOut.WriteTObject(up)
#  fOut.WriteTObject(down)
