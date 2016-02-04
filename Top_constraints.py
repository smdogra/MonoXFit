import ROOT
from counting_experiment import *
# Define how a control region(s) transfer is made by defining cmodel provide, the calling pattern must be unchanged!
# First define simple string which will be used for the datacard 
model = "ttbar"
convertHistograms = []

### helper functions ###

def makeTop(cid,_fOut,newName,targetmc,controlmc,targetmcup=None,targetmcdown=None,controlmcup=None,controlmcdown=None):
  TopScales = targetmc.Clone(); TopScales.SetName(newName+"_weights_%s"%cid)
  TopScales.Divide(controlmc)
  _fOut.WriteTObject(TopScales)

  if not(targetmcup==None):
    TopScalesUp = targetmcup.Clone(); TopScalesUp.SetName(newName+"_weights_%s_btag_Up"%cid)
    TopScalesUp.Divide(controlmcup)
    _fOut.WriteTObject(TopScalesUp)

    TopScalesDown = targetmcdown.Clone(); TopScalesDown.SetName(newName+"_weights_%s_btag_Down"%cid)
    TopScalesDown.Divide(controlmcdown)
    _fOut.WriteTObject(TopScalesDown)

    return TopScales,TopScalesUp,TopScalesDown
  
  return TopScales


def addTopErrors(TopScales,targetmc,newName,crName,_fOut,CRs,nCR,cid):

  '''
  CRs[nCR].add_nuisance("pdf_CT10",0.006)
  if crName.find('electron')>=0:
   CRs[nCR].add_nuisance("CMS_eff_e",0.01) 
  else:
   CRs[nCR].add_nuisance("CMS_eff_m",0.01) 
  '''

  CRs[nCR].add_nuisance_shape("btag",_fOut)

  bins = range(targetmc.GetNbinsX())

  for b in bins:
    err = TopScales.GetBinError(b+1)
    if not TopScales.GetBinContent(b+1)>0: continue 
    else: relerr = err/TopScales.GetBinContent(b+1)
    if relerr<0.001: continue
    byb_u = TopScales.Clone(); byb_u.SetName("%s_weights_%s_%s_stat_error_%sCR_bin%d_Up"%(newName,cid,cid,crName,b))
    byb_u.SetBinContent(b+1,TopScales.GetBinContent(b+1)+err)
    byb_d = TopScales.Clone(); byb_d.SetName("%s_weights_%s_%s_stat_error_%sCR_bin%d_Down"%(newName,cid,cid,crName,b))
    byb_d.SetBinContent(b+1,TopScales.GetBinContent(b+1)-err)
    _fOut.WriteTObject(byb_u)
    _fOut.WriteTObject(byb_d)
    print "Adding an error -- ", byb_u.GetName(),err
    CRs[nCR].add_nuisance_shape("%s_stat_error_%sCR_bin%d"%(cid,crName,b),_fOut)

def cmodel(cid,nam,_f,_fOut, out_ws, diag):
  # Some setup
  _fin = _f.Get("category_%s"%cid)
  _wspace = _fin.Get("wspace_%s"%cid)


  # ############################ USER DEFINED ###########################################################
  # First define the nominal transfer factors (histograms of signal/control, usually MC 
  # note there are many tools available inside include/diagonalize.h for you to make 
  # special datasets/histograms representing these and systematic effects 
  # but for now this is just kept simple 
  processName = "TTbar" # Give a name of the process being modelled
  metname = "met"    # Observable variable name 

  targetmc     = _fin.Get("signal_ttbar")      # define monimal (MC) of which process this config will model
  controlmc    = _fin.Get("singlemuontop_ttbar")
  controlmc_e  = _fin.Get("singleelectrontop_ttbar")
  targetmcUp = _fin.Get("signal_ttbar_btagUp")
  targetmcDown = _fin.Get("signal_ttbar_btagDown")
  controlmcUp = _fin.Get("singlemuontop_ttbar_btagUp"); controlmcUp_e = _fin.Get("singleelectrontop_ttbar_btagUp")
  controlmcDown = _fin.Get("singlemuontop_ttbar_btagDown"); controlmcDown_e = _fin.Get("singleelectrontop_ttbar_btagDown")
  
  genVpt = "genVpt"

  # Create the transfer factors and save them (not here you can also create systematic variations of these 
  # transfer factors (named with extention _sysname_Up/Down

  #diag.generateWeightedDataset("signal_ttbar_weighted",hOne,"weight",genVpt,_wspace,"signal_ttbar")
  #diag.generateWeightedDataset("signal_ttbar_weighted_btagUp",hOne,"weight",genVpt,_wspace,"signal_ttbar_btagUp")
  #diag.generateWeightedDataset("signal_ttbar_weighted_btagDown",hOne,"weight",genVpt,_wspace,"signal_ttbar_btagDown")


  TopScales,TopScalesUp,TopScalesDown = makeTop(cid,_fOut,"topmnTopCR",targetmc,controlmc,targetmcUp,targetmcDown,controlmcUp,controlmcDown)
  TopScales_e,TopScalesUp_e,TopScalesDown_e = makeTop(cid,_fOut,"topenTopCR",targetmc,controlmc_e,targetmcUp_e,targetmcDown_e,controlmcUp_e,controlmcDown_e)

  controlmcW = _fin.Get('singlemuonw_ttbar')
  controlmcW_e = _fin.Get('singleelectronw_ttbar')
  controlmcWUp = _fin.Get("singlemuonw_ttbar_btagUp"); controlmcWUp_e = _fin.Get("singleelectronw_ttbar_btagUp")
  controlmcWDown = _fin.Get("singlemuonw_ttbar_btagDown"); controlmcWDown_e = _fin.Get("singleelectronw_ttbar_btagDown")

  WScales,WScalesUp,WScalesDown = makeTop(cid,_fOut,"topmnWCR",targetmc,controlmcW,targetmcWUp,targetmcWDown,controlmcWUp,controlmcWDown)
  WScales_e,WScalesUp_e,WScalesDown_e = makeTop(cid,_fOut,"topenWCR",targetmc,controlmcW_e,targetmcWUp_e,targetmcWDown_e,controlmcWUp_e,controlmcWDown_e)

  '''
  TopScales,TopScalesUp,TopScalesDown = makeTop(_fin,cid,metname,genVpt,hOne,_wspace,_fOut,diag,"topmn","singlemuontop",targetmc,targetmcUp,targetmcDown)
  TopScalese,TopScaleseUp,TopScaleseDown = makeTop(_fin,cid,metname,genVpt,hOne,_wspace,_fOut,diag,"topen","singleelectrontop",targetmc,targetmcUp,targetmcDown)
  WScales,WScalesUp,WScalesDown = makeTop(_fin,cid,metname,genVpt,hOne,_wspace,_fOut,diag,"topmnw","singlemuonw",targetmc,targetmcUp,targetmcDown)
  WScalese,WScaleseUp,WScaleseDown = makeTop(_fin,cid,metname,genVpt,hOne,_wspace,_fOut,diag,"topenw","singleelectronw",targetmc,targetmcUp,targetmcDown)
  '''

  #######################################################################################################

  _bins = []  # take bins from some histogram, can choose anything but this is easy 
  for b in range(targetmc.GetNbinsX()+1):
    _bins.append(targetmc.GetBinLowEdge(b+1))

  # Here is the important bit which "Builds" the control region, make a list of control regions which 
  # are constraining this process, each "Channel" is created with ...
  # 	(name,_wspace,out_ws,cid+'_'+model,TRANSFERFACTORS) 
  # the second and third arguments can be left unchanged, the others instead must be set
  # TRANSFERFACTORS are what is created above, eg TopScales

  CRs = [
   Channel("singlemuontopModelTop",_wspace,out_ws,cid+'_'+model,TopScales)
   ,Channel("singleelectrontopModelTop",_wspace,out_ws,cid+'_'+model,TopScales_e)
   ,Channel("singlemuonwModelTop",_wspace,out_ws,cid+'_'+model,WScales)
   ,Channel("singleelectronwModelTop",_wspace,out_ws,cid+'_'+model,WScales_e)
  ]


  # ############################ USER DEFINED ###########################################################
  # Add systematics in the following, for normalisations use name, relative size (0.01 --> 1%)
  # for shapes use add_nuisance_shape with (name,_fOut)
  # note, the code will LOOK for something called NOMINAL_name_Up and NOMINAL_name_Down, where NOMINAL=TopScales.GetName()
  # these must be created and writted to the same dirctory as the nominal (fDir)
  
  addTopErrors(TopScales,  targetmc,"topmnTopCR","singlemuontopModelTop",    _fOut,CRs,0,cid)
  addTopErrors(TopScales_e,targetmc,"topenTopCR","singleelectrontopModelTop",_fOut,CRs,1,cid)
  addTopErrors(WScales,    targetmc,"topmnWCR",  "singlemuonwModelTop",      _fOut,CRs,2,cid)
  addTopErrors(WScales_e,  targetmc,"topenWCR",  "singleelectronwModelTop",  _fOut,CRs,3,cid)

  #######################################################################################################

  cat = Category(model,cid,nam,_fin,_fOut,_wspace,out_ws,_bins,metname,targetmc.GetName(),CRs,diag)
  #cat.setDependant("zjets","wjetsdependant")  # Can use this to state that the "BASE" of this is already dependant on another process
  # EG if the W->lv in signal is dependant on the Z->vv and then the W->mv is depenant on W->lv, then 
  # give the arguments model,channel name from the config which defines the Z->vv => W->lv map! 
  # Return of course
  return cat

