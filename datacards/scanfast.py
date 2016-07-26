#!/usr/bin/env python

from os import system
from re import sub
from sys import argv
from argparse import ArgumentParser

parser = ArgumentParser(description='perform 2d scan')
parser.add_argument('template',metavar='template',type=str)
parser.add_argument('--mMed',type=int,default=None)
parser.add_argument('--mChi',type=int,default=None)
parser.add_argument('--isRes',dest='isRes',action='store_true')
parser.add_argument('--isFCNC',dest='isRes',action='store_false')
parser.set_defaults(isRes=False)
args = parser.parse_args()

class Model():
  def __init__(self,mMed,mChi,isRes):
    self.mMed=mMed
    self.mChi=mChi
    self.isRes=isRes
    if isRes:
      self.name = 'monotop_med-%i_dm-%i'%(mMed,mChi)
    else:
      self.name = 'monotop-nr-v3-%i-%i_med-%i_dm-%i'%(mMed,mChi,mMed,mChi)

def run(model,runObserved=True):
  label = 'res_' if model.isRes else 'fcnc_'
  label += '%i_%i'%(model.mMed,model.mChi)
  runOption = '' if runObserved else '--run=blind'
  cmd = "sed 's?XXXX?%s?g' %s > combined_%s.txt"%(model.name,args.template,label)
  system(cmd)
  system("sed -i 's?combined_model\.root?../combined_model.root?g' combined_%s.txt"%(label))
  # system("sed 's/XXXX/%s/g %s > combined_%s.txt'"%(model.name,args.template,label))
  system("combine -M Asymptotic combined_%s.txt -n %s"%(label,label))
  # system("combine -M Asymptotic combined_%s.txt -n %s -m %i"%(label,model.mMed*1000+mChi))

model = Model(args.mMed,args.mChi,args.isRes)
run(model,True)

# def run(modelClass,modelsList,runObserved=True):
#   s=''
#   logfile = '%sv3_%slimits.txt'%(modelClass,'obs_' if runObserved else '')
#   runOption = '' if runObserved else ' --run=blind'
#   for l in modelsList:
#     print l
#     mass = sub('[A-z]*','',l.split('_')[0])
#     if 'nr' in l:
#       mass = l.split('-')[3]
#     else:
#       mass = sub('_dm','',l.split('-')[1])
#     print mass
#     s += 'echo "MASS %s" \n'%(mass)
#     s += "sed 's/XXXX/%s/g' combined_tmpl.txt > combined_run.txt \n"%(l)
#     s += "combine -M Asymptotic combined_run.txt %s > tmp.txt\n"%(runOption)
#     s += 'grep "<" tmp.txt \n'
#   with open('run.sh','w') as runFile:
#     runFile.write(s)
#   system('sh run.sh > '+logfile)
    

# run('fcnc',['monotop-nr-v3-%i-10_med-%i_dm-10'%(m,m) for m in range(300,2300,200)],True)
# run('resonant',['monotop_med-%i_dm-100'%(m) for m in range(900,3100,200)],True)

