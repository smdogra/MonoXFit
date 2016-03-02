import ROOT
from counting_experiment import *
# Define how a control region(s) transfer is made by defining cmodel provide, the calling pattern must be unchanged!
# First define simple string which will be used for the datacard 
model = "wjets"
def cmodel(cid,nam,_f,_fOut, out_ws, diag):
  
  # Some setup
  _fin    = _f.Get("category_%s"%cid)
  _wspace = _fin.Get("wspace_%s"%cid)


  # ############################ USER DEFINED ###########################################################
  # First define the nominal transfer factors (histograms of signal/control, usually MC 
  # note there are many tools available inside include/diagonalize.h for you to make 
  # special datasets/histograms representing these and systematic effects 
  # but for now this is just kept simple 
  processName  = "WJets" # Give a name of the process being modelled
  metname      = "met"    # Observable variable name 
  targetmc     = _fin.Get("signal_wjets")      # define monimal (MC) of which process this config will model
  controlmc    = _fin.Get("singlemuonw_wjets")  # defines in / out acceptance
  controlmc_e  = _fin.Get("singleelectronw_wjets")  # defines in / out acceptance

  # btag systs
  targetmcbtagUp = _fin.Get("signal_wjets_btagUp")
  targetmcbtagDown = _fin.Get("signal_wjets_btagDown")
  controlmcbtagUp = _fin.Get("singlemuonw_wjets_btagUp"); controlmcbtagUp_e = _fin.Get("singleelectronw_wjets_btagUp")
  controlmcbtagDown = _fin.Get("singlemuonw_wjets_btagDown"); controlmcbtagDown_e = _fin.Get("singleelectronw_wjets_btagDown")

  # mistag systs
  targetmcmistagUp = _fin.Get("signal_wjets_mistagUp")
  targetmcmistagDown = _fin.Get("signal_wjets_mistagDown")
  controlmcmistagUp = _fin.Get("singlemuonw_wjets_mistagUp"); controlmcmistagUp_e = _fin.Get("singleelectronw_wjets_mistagUp")
  controlmcmistagDown = _fin.Get("singlemuonw_wjets_mistagDown"); controlmcmistagDown_e = _fin.Get("singleelectronw_wjets_mistagDown")

  '''
  # wjethf systs
  targetmcwjethfUp = _fin.Get("signal_wjets_wjethfUp")
  targetmcwjethfDown = _fin.Get("signal_wjets_wjethfDown")
  controlmcwjethfUp = _fin.Get("singlemuonw_wjets_wjethfUp"); controlmcwjethfUp_e = _fin.Get("singleelectronw_wjets_wjethfUp")
  controlmcwjethfDown = _fin.Get("singlemuonw_wjets_wjethfDown"); controlmcwjethfDown_e = _fin.Get("singleelectronw_wjets_wjethfDown")
  '''

  # Create the transfer factors and save them (not here you can also create systematic variations of these 
  # transfer factors (named with extention _sysname_Up/Down
  
  WScales = targetmc.Clone(); WScales.SetName("wmn_weights_%s"%cid)
  WScales.Divide(controlmc);  _fOut.WriteTObject(WScales)  # always write out to the directory 

  WScales_e = targetmc.Clone(); WScales_e.SetName("wen_weights_%s"%cid)
  WScales_e.Divide(controlmc_e);  _fOut.WriteTObject(WScales_e)  # always write out to the directory 

  ### BTAG ###  
  WScalesbtagUp = targetmcbtagUp.Clone(); WScalesbtagUp.SetName("wmn_weights_%s_btag_Up"%cid)
  WScalesbtagUp.Divide(controlmcbtagUp);  _fOut.WriteTObject(WScalesbtagUp)  # always write out to the directory 

  WScalesbtagDown = targetmcbtagDown.Clone(); WScalesbtagDown.SetName("wmn_weights_%s_btag_Down"%cid)
  WScalesbtagDown.Divide(controlmcbtagDown);  _fOut.WriteTObject(WScalesbtagDown)

  WScalesbtagUp_e = targetmcbtagUp.Clone(); WScalesbtagUp_e.SetName("wen_weights_%s_btag_Up"%cid)
  WScalesbtagUp_e.Divide(controlmcbtagUp_e);  _fOut.WriteTObject(WScalesbtagUp_e)  # always write out to the directory 

  WScalesbtagDown_e = targetmcbtagDown.Clone(); WScalesbtagDown_e.SetName("wen_weights_%s_btag_Down"%cid)
  WScalesbtagDown_e.Divide(controlmcbtagDown_e);  _fOut.WriteTObject(WScalesbtagDown_e)  # always write out to the directory 

  ### MISTAG ###  
  WScalesmistagUp = targetmcmistagUp.Clone(); WScalesmistagUp.SetName("wmn_weights_%s_mistag_Up"%cid)
  WScalesmistagUp.Divide(controlmcmistagUp);  _fOut.WriteTObject(WScalesmistagUp)  # always write out to the directory 

  WScalesmistagDown = targetmcmistagDown.Clone(); WScalesmistagDown.SetName("wmn_weights_%s_mistag_Down"%cid)
  WScalesmistagDown.Divide(controlmcmistagDown);  _fOut.WriteTObject(WScalesmistagDown)

  WScalesmistagUp_e = targetmcmistagUp.Clone(); WScalesmistagUp_e.SetName("wen_weights_%s_mistag_Up"%cid)
  WScalesmistagUp_e.Divide(controlmcmistagUp_e);  _fOut.WriteTObject(WScalesmistagUp_e)  # always write out to the directory 

  WScalesmistagDown_e = targetmcmistagDown.Clone(); WScalesmistagDown_e.SetName("wen_weights_%s_mistag_Down"%cid)
  WScalesmistagDown_e.Divide(controlmcmistagDown_e);  _fOut.WriteTObject(WScalesmistagDown_e)  # always write out to the directory 

  '''
  ### HF ###  
  WScaleswjethfUp = targetmcwjethfUp.Clone(); WScaleswjethfUp.SetName("wmn_weights_%s_wjethf_Up"%cid)
  WScaleswjethfUp.Divide(controlmcwjethfUp);  _fOut.WriteTObject(WScaleswjethfUp)  # always write out to the directory 

  WScaleswjethfDown = targetmcwjethfDown.Clone(); WScaleswjethfDown.SetName("wmn_weights_%s_wjethf_Down"%cid)
  WScaleswjethfDown.Divide(controlmcwjethfDown);  _fOut.WriteTObject(WScaleswjethfDown)

  WScaleswjethfUp_e = targetmcwjethfUp.Clone(); WScaleswjethfUp_e.SetName("wen_weights_%s_wjethf_Up"%cid)
  WScaleswjethfUp_e.Divide(controlmcwjethfUp_e);  _fOut.WriteTObject(WScaleswjethfUp_e)  # always write out to the directory 

  WScaleswjethfDown_e = targetmcwjethfDown.Clone(); WScaleswjethfDown_e.SetName("wen_weights_%s_wjethf_Down"%cid)
  WScaleswjethfDown_e.Divide(controlmcwjethfDown_e);  _fOut.WriteTObject(WScaleswjethfDown_e)  # always write out to the directory 
  '''

  #######################################################################################################

  _bins = []  # take bins from some histogram, can choose anything but this is easy 
  for b in range(targetmc.GetNbinsX()+1):
    _bins.append(targetmc.GetBinLowEdge(b+1))

  # Here is the important bit which "Builds" the control region, make a list of control regions which 
  # are constraining this process, each "Channel" is created with ...
  # 	(name,_wspace,out_ws,cid+'_'+model,TRANSFERFACTORS) 
  # the second and third arguments can be left unchanged, the others instead must be set
  # TRANSFERFACTORS are what is created above, eg WScales

  CRs = [
   Channel("singlemuonwModel",_wspace,out_ws,cid+'_'+model,WScales),
   Channel("singleelectronwModel",_wspace,out_ws,cid+'_'+model,WScales_e),
  ]


  # ############################ USER DEFINED ###########################################################
  # Add systematics in the following, for normalisations use name, relative size (0.01 --> 1%)
  # for shapes use add_nuisance_shape with (name,_fOut)
  # note, the code will LOOK for something called NOMINAL_name_Up and NOMINAL_name_Down, where NOMINAL=WScales.GetName()
  # these must be created and writted to the same dirctory as the nominal (fDir)

  #CRs[0].add_nuisance("SingleMuonEff",0.01)
  #CRs[1].add_nuisance("SingleElEff",0.02)

  for cr in [0,1]:
    CRs[cr].add_nuisance("SFSubJetBMistag",0.07)
    CRs[cr].add_nuisance("SFSubJetBtag",0.07)

  # for cr in [0,1]:
  #   for uncert in ['btag','mistag']:
  #     CRs[cr].add_nuisance_shape(uncert,_fOut)
  
  # Statistical uncertainties too!, one per bin 
  for b in range(targetmc.GetNbinsX()):
    err = WScales.GetBinError(b+1)
    if not WScales.GetBinContent(b+1)>0: continue 
    relerr = err/WScales.GetBinContent(b+1)
    if relerr<0.001: continue
    byb_u = WScales.Clone(); byb_u.SetName("wmn_weights_%s_%s_stat_error_%s_bin%d_Up"%(cid,cid,"singlemuonwModel",b))
    byb_u.SetBinContent(b+1,WScales.GetBinContent(b+1)+err)
    byb_d = WScales.Clone(); byb_d.SetName("wmn_weights_%s_%s_stat_error_%s_bin%d_Down"%(cid,cid,"singlemuonwModel",b))
    byb_d.SetBinContent(b+1,WScales.GetBinContent(b+1)-err)
    _fOut.WriteTObject(byb_u)
    _fOut.WriteTObject(byb_d)
    print "Adding an error -- ", byb_u.GetName(),err
    CRs[0].add_nuisance_shape("%s_stat_error_%s_bin%d"%(cid,"singlemuonwModel",b),_fOut)

  # Statistical uncertainties too!, one per bin 
  for b in range(targetmc.GetNbinsX()):
    err_e = WScales_e.GetBinError(b+1)
    if not WScales_e.GetBinContent(b+1)>0: continue 
    relerr_e = err_e/WScales_e.GetBinContent(b+1)
    if relerr_e<0.001: continue
    byb_u_e = WScales_e.Clone(); byb_u_e.SetName("wen_weights_%s_%s_stat_error_%s_bin%d_Up"%(cid,cid,"singleelectronwModel",b))
    byb_u_e.SetBinContent(b+1,WScales_e.GetBinContent(b+1)+err_e)
    byb_d_e = WScales_e.Clone(); byb_d_e.SetName("wen_weights_%s_%s_stat_error_%s_bin%d_Down"%(cid,cid,"singleelectronwModel",b))
    byb_d_e.SetBinContent(b+1,WScales_e.GetBinContent(b+1)-err_e)
    _fOut.WriteTObject(byb_u_e)
    _fOut.WriteTObject(byb_d_e)
    print "Adding an error -- ", byb_u_e.GetName(),err_e
    CRs[1].add_nuisance_shape("%s_stat_error_%s_bin%d"%(cid,"singleelectronwModel",b),_fOut)

  #######################################################################################################

  cat = Category(model,cid,nam,_fin,_fOut,_wspace,out_ws,_bins,metname,targetmc.GetName(),CRs,diag)
  #cat.setDependant("zjets","wjetssignal")  # Can use this to state that the "BASE" of this is already dependant on another process
  # EG if the W->lv in signal is dependant on the Z->vv and then the W->mv is depenant on W->lv, then 
  # give the arguments model,channel name from the config which defines the Z->vv => W->lv map! 
  # Return of course
  return cat

