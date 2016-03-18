#!/usr/bin/env python

from os import system
from re import sub

def run(modelClass,modelsList,runObserved=True):
  s=''
  logfile = '%s_%slimits.txt'%(modelClass,'obs_' if runObserved else '')
#  s += 'rm -f %s\n'%(logfile)
  runOption = '' if runObserved else ' --run=expected'
  for l in modelsList:
    print l
    mass = sub('[A-z]*','',l.split('_')[0])
    s += 'echo "MASS %s" \n'%(mass)
    s += "sed 's/XXXX/%s/g' combined_tmpl.txt > combined_run.txt \n"%(l)
    s += "combine -M Asymptotic combined_run.txt %s > tmp.txt\n"%(runOption)
    s += 'grep "<" tmp.txt \n'
  with open('run.sh','w') as runFile:
    runFile.write(s)
  system('sh run.sh > '+logfile)
    

run('fcnc',['Mchi300','Mchi500','Mchi700','Mchi900','Mchi1100','Mchi1300','Mchi1500'],True)
run('resonant',['Mres%i_Mchi100'%(x) for x in [900,1100,1300,1500,1700,1900,2100]],True)
