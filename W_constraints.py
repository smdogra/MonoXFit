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
  targetmcUp = _fin.Get("signal_wjets_btagUp")
  targetmcDown = _fin.Get("signal_wjets_btagDown")
  controlmcUp = _fin.Get("singlemuonw_wjets_btagUp"); controlmcUp_e = _fin.Get("singleelectronw_wjets_btagUp")
  controlmcDown = _fin.Get("singlemuonw_wjets_btagDown"); controlmcDown_e = _fin.Get("singleelectronw_wjets_btagDown")

  # Create the transfer factors and save them (not here you can also create systematic variations of these 
  # transfer factors (named with extention _sysname_Up/Down
  WScales = targetmc.Clone(); WScales.SetName("wmnWCR_weights_%s"%cid)
  WScales.Divide(controlmc)
  _fOut.WriteTObject(WScales)  # always write out to the directory 

  WScalesUp = targetmcUp.Clone(); WScalesUp.SetName("wmnWCR_weights_%s_btagW_Up"%cid)
  WScalesUp.Divide(controlmcUp)
  _fOut.WriteTObject(WScalesUp)  # always write out to the directory 

  WScalesDown = targetmcDown.Clone(); WScalesDown.SetName("wmnWCR_weights_%s_btagW_Down"%cid)
  WScalesDown.Divide(controlmcDown)
  _fOut.WriteTObject(WScalesDown)  # always write out to the directory 


  WScales_e = targetmc.Clone(); WScales_e.SetName("wenWCR_weights_%s"%cid)
  WScales_e.Divide(controlmc_e)
  _fOut.WriteTObject(WScales_e)  # always write out to the directory 

  WScalesUp_e = targetmcUp.Clone(); WScalesUp_e.SetName("wenWCR_weights_%s_btagW_Up"%cid)
  WScalesUp_e.Divide(controlmcUp_e)
  _fOut.WriteTObject(WScalesUp_e)  # always write out to the directory 

  WScalesDown_e = targetmcDown.Clone(); WScalesDown_e.SetName("wenWCR_weights_%s_btagW_Down"%cid)
  WScalesDown_e.Divide(controlmcDown_e)
  _fOut.WriteTObject(WScalesDown_e)  # always write out to the directory 


  controlmcTop = _fin.Get("singlemuontop_wjets")
  controlmcTop_e = _fin.Get("singleelectrontop_wjets")
  controlmcTopUp = _fin.Get("singlemuontop_wjets_btagUp"); controlmcTopUp_e = _fin.Get("singleelectrontop_wjets_btagUp")
  controlmcTopDown = _fin.Get("singlemuontop_wjets_btagDown"); controlmcTopDown_e = _fin.Get("singleelectrontop_wjets_btagDown")

  TopScales = targetmc.Clone(); TopScales.SetName("wmnTopCR_weights_%s"%cid)
  TopScales.Divide(controlmcTop)
  _fOut.WriteTObject(TopScales)

  TopScalesUp = targetmcUp.Clone(); TopScalesUp.SetName("wmnTopCR_weights_%s_btagW_Up"%cid)
  TopScalesUp.Divide(controlmcTopUp)
  _fOut.WriteTObject(TopScalesUp)

  TopScalesDown = targetmcDown.Clone(); TopScalesDown.SetName("wmnTopCR_weights_%s_btagW_Down"%cid)
  TopScalesDown.Divide(controlmcTopDown)
  _fOut.WriteTObject(TopScalesDown)


  TopScales_e = targetmc.Clone(); TopScales_e.SetName("wenTopCR_weights_%s"%cid)
  TopScales_e.Divide(controlmcTop_e)
  _fOut.WriteTObject(TopScales_e)

  TopScalesUp_e = targetmcUp.Clone(); TopScalesUp_e.SetName("wenTopCR_weights_%s_btagW_Up"%cid)
  TopScalesUp_e.Divide(controlmcTopUp_e)
  _fOut.WriteTObject(TopScalesUp_e)

  TopScalesDown_e = targetmcDown.Clone(); TopScalesDown_e.SetName("wenTopCR_weights_%s_btagW_Down"%cid)
  TopScalesDown_e.Divide(controlmcTopDown_e)
  _fOut.WriteTObject(TopScalesDown_e)


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
   Channel("singlemuonwModelW",_wspace,out_ws,cid+'_'+model,WScales),
   Channel("singleelectronwModelW",_wspace,out_ws,cid+'_'+model,WScales_e),
   Channel("singlemuontopModelW",_wspace,out_ws,cid+'_'+model,TopScales),
   Channel("singleelectrontopModelW",_wspace,out_ws,cid+'_'+model,TopScales_e)
  ]


  # ############################ USER DEFINED ###########################################################
  # Add systematics in the following, for normalisations use name, relative size (0.01 --> 1%)
  # for shapes use add_nuisance_shape with (name,_fOut)
  # note, the code will LOOK for something called NOMINAL_name_Up and NOMINAL_name_Down, where NOMINAL=WScales.GetName()
  # these must be created and writted to the same dirctory as the nominal (fDir)

  #CRs[0].add_nuisance("SingleMuonEff",0.01)
  #CRs[1].add_nuisance("SingleElEff",0.02)

  CRs[0].add_nuisance_shape("btagW",_fOut)
  CRs[1].add_nuisance_shape("btagW",_fOut)
  CRs[2].add_nuisance_shape("btagW",_fOut)
  CRs[3].add_nuisance_shape("btagW",_fOut)

  # Statistical uncertainties too!, one per bin 
  for b in range(targetmc.GetNbinsX()):
    err = WScales.GetBinError(b+1)
    if not WScales.GetBinContent(b+1)>0: continue 
    relerr = err/WScales.GetBinContent(b+1)
    if relerr<0.001: continue
    byb_u = WScales.Clone(); byb_u.SetName("wmnWCR_weights_%s_%s_stat_error_%s_bin%d_Up"%(cid,cid,"singlemuonwModelWCR",b))
    byb_u.SetBinContent(b+1,WScales.GetBinContent(b+1)+err)
    byb_d = WScales.Clone(); byb_d.SetName("wmnWCR_weights_%s_%s_stat_error_%s_bin%d_Down"%(cid,cid,"singlemuonwModelWCR",b))
    byb_d.SetBinContent(b+1,WScales.GetBinContent(b+1)-err)
    _fOut.WriteTObject(byb_u)
    _fOut.WriteTObject(byb_d)
    print "Adding an error -- ", byb_u.GetName(),err
    CRs[0].add_nuisance_shape("%s_stat_error_%s_bin%d"%(cid,"singlemuonwModelWCR",b),_fOut)

  # Statistical uncertainties too!, one per bin 
  for b in range(targetmc.GetNbinsX()):
    err_e = WScales_e.GetBinError(b+1)
    if not WScales_e.GetBinContent(b+1)>0: continue 
    relerr_e = err_e/WScales_e.GetBinContent(b+1)
    if relerr_e<0.001: continue
    byb_u_e = WScales_e.Clone(); byb_u_e.SetName("wenWCR_weights_%s_%s_stat_error_%s_bin%d_Up"%(cid,cid,"singleelectronwModelWCR",b))
    byb_u_e.SetBinContent(b+1,WScales_e.GetBinContent(b+1)+err_e)
    byb_d_e = WScales_e.Clone(); byb_d_e.SetName("wenWCR_weights_%s_%s_stat_error_%s_bin%d_Down"%(cid,cid,"singleelectronwModelWCR",b))
    byb_d_e.SetBinContent(b+1,WScales_e.GetBinContent(b+1)-err_e)
    _fOut.WriteTObject(byb_u_e)
    _fOut.WriteTObject(byb_d_e)
    print "Adding an error -- ", byb_u_e.GetName(),err_e
    CRs[1].add_nuisance_shape("%s_stat_error_%s_bin%d"%(cid,"singleelectronwModelWCR",b),_fOut)

  # Statistical uncertainties too!, one per bin 
  for b in range(targetmc.GetNbinsX()):
    err = TopScales.GetBinError(b+1)
    if not TopScales.GetBinContent(b+1)>0: continue 
    relerr = err/TopScales.GetBinContent(b+1)
    if relerr<0.001: continue
    byb_u = TopScales.Clone(); byb_u.SetName("wmnTopCR_weights_%s_%s_stat_error_%s_bin%d_Up"%(cid,cid,"singlemuontopModelWCR",b))
    byb_u.SetBinContent(b+1,TopScales.GetBinContent(b+1)+err)
    byb_d = TopScales.Clone(); byb_d.SetName("wmnTopCR_weights_%s_%s_stat_error_%s_bin%d_Down"%(cid,cid,"singlemuontopModelWCR",b))
    byb_d.SetBinContent(b+1,TopScales.GetBinContent(b+1)-err)
    _fOut.WriteTObject(byb_u)
    _fOut.WriteTObject(byb_d)
    print "Adding an error -- ", byb_u.GetName(),err
    CRs[2].add_nuisance_shape("%s_stat_error_%s_bin%d"%(cid,"singlemuontopModelWCR",b),_fOut)

  # Statistical uncertainties too!, one per bin 
  for b in range(targetmc.GetNbinsX()):
    err = TopScales_e.GetBinError(b+1)
    if not TopScales_e.GetBinContent(b+1)>0: continue 
    relerr = err/TopScales_e.GetBinContent(b+1)
    if relerr<0.001: continue
    byb_u = TopScales_e.Clone(); byb_u.SetName("wenTopCR_weights_%s_%s_stat_error_%s_bin%d_Up"%(cid,cid,"singleelectrontopModelWCR",b))
    byb_u.SetBinContent(b+1,TopScales_e.GetBinContent(b+1)+err)
    byb_d = TopScales_e.Clone(); byb_d.SetName("wenTopCR_weights_%s_%s_stat_error_%s_bin%d_Down"%(cid,cid,"singleelectrontopModelWCR",b))
    byb_d.SetBinContent(b+1,TopScales_e.GetBinContent(b+1)-err)
    _fOut.WriteTObject(byb_u)
    _fOut.WriteTObject(byb_d)
    print "Adding an error -- ", byb_u.GetName(),err
    CRs[3].add_nuisance_shape("%s_stat_error_%s_bin%d"%(cid,"singleelectrontopModelWCR",b),_fOut)

  #######################################################################################################

  cat = Category(model,cid,nam,_fin,_fOut,_wspace,out_ws,_bins,metname,targetmc.GetName(),CRs,diag)
  #cat.setDependant("zjets","wjetssignal")  # Can use this to state that the "BASE" of this is already dependant on another process
  # EG if the W->lv in signal is dependant on the Z->vv and then the W->mv is depenant on W->lv, then 
  # give the arguments model,channel name from the config which defines the Z->vv => W->lv map! 
  # Return of course
  return cat

