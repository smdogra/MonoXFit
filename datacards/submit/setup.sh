#!/bin/bash

#here
export PANDA=${CMSSW_BASE}/src/MitPanda/

#location of nero output (from bambu or miniaod)
histDir=monotop80/v1.8
export PANDA_HISTDIR=${EOS}/$histDir
export PANDA_HISTDIR_CERNBOX=${CERNBOX}/$histDir
export PANDA_HISTDIR_CERNBOXB=${CERNBOXB}/$histDir

#location of private-produced samples
export PANDA_PRODDIR=${HOME}/cms/hist/monotop_private

#location of flat trees
export PANDA_FLATDIR=${HOME}/work/skims/monotop_80_v9/
#export PANDA_FLATDIR=${HOME}/work/skims/monotop_trigger/
export PANDA_PRODFLATDIR=${ROOT}/monotop_prod/
export PANDA_LIMITDIR=${HOME}/work/skims/monotop_limits_v1/

