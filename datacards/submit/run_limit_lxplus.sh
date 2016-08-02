#!/bin/bash
cfgName=$1
WD=${PWD}
pwd

executable=scanbatch.py

scramdir=/afs/cern.ch/user/s/snarayan/work/private/CMSSW_7_4_7/
cd ${scramdir}/src/
eval `scramv1 runtime -sh`
cd $WD

monox=${scramdir}/src/MonoX/
source ${monox}/datacards/submit/setup.sh
cp ${monox}/combined_model.root .
cp ${monox}/datacards/combined_tmpl.txt .
cp ${monox}/datacards/combined_batch.txt .
cp ${monox}/datacards/${executable} .

sed -i 's?\.\./combined_model.root?combined_model.root?g' combined_tmpl.txt

echo ##############################
ls
echo ##############################

cat $cfgName | xargs -n 5 -P 4 python ${executable} combined_batch.txt
#cat $cfgName | xargs -n 5 -P 4 python ${executable} combined_tmpl.txt

echo ##############################

cp higgs*root ${PANDA_LIMITDIR}/results/

rm -f *root *txt *py *cfg

exit 0
