#!/usr/bin/env python

from os import system,environ
from sys import exit,stdout
from re import sub
from glob import glob

filestoprocess = glob('/afs/cern.ch/user/s/snarayan/work/skims/monotop_limits_v1/MonoTop_*801.root')
#filestoprocess = glob('/afs/cern.ch/user/s/snarayan/eos/cms/store/user/snarayan/monotop80/private/monotop-nr-v3-500-10_med-500_dm-10.root')
print 'processing %i files'%len(filestoprocess)
if len(filestoprocess)==0:
  print 'no files found'
  exit(1)

scramdir=environ['CMSSW_BASE']
nPerJob=10
queue = '2nw4cores' 
#queue = '1nh'

nF=len(filestoprocess)
nJ = nF/nPerJob+1
for iJ in xrange(nJ):
  cfgpath = '%s/cfg/fit_%i.cfg'%(environ['PANDA_LIMITDIR'],iJ)
  with open(cfgpath,'w') as cfgfile:
    for iF in xrange(iJ*nPerJob,min((iJ+1)*nPerJob,nF)):
      f = filestoprocess[iF].split('/')[-1]
      if ('nr' in f) or ('801' in f):
        mV = f.split('_')[1]
        mChi = f.split('_')[2]
        cfgfile.write('--mMed %4s --mChi %3s --isFCNC\n'%(mV,mChi))
        '''
        mV = f.split('-')[3]
        mChi = sub('_med','',f.split('-')[4])
        cfgfile.write('--mMed %4s --mChi %3s --isFCNC\n'%(mV,mChi))
        '''
      else:
        mChi = '100'
        mPhi = sub('.root','',f.split('-')[1])
        cfgfile.write('--mMed %4s --mChi %3s --isRes\n'%(mPhi,mChi))
  logpath = '/afs/cern.ch/work/s/%s/logs/fits_%i'%(environ['USER'],iJ)
  cmd = 'bsub -o %s.out -e %s.err -q %s run_limit_lxplus.sh %s'%(logpath,logpath,queue,cfgpath)
  print cmd
  system(cmd)
