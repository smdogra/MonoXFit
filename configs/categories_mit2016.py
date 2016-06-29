# Configuration for a simple monojet topology. Use this as a template for your own Run-2 mono-X analysis
# First provide ouput file name in out_file_name field 
out_file_name = 'mono-x.root'

# can define any thing useful here which may be common to several categories, eg binning in MET 
#bins = range(200,1200,200)
bins = [250,300,350,400,500,1000]
#bins = [250,300,350,400,500,600,1000]
# will expect samples with sample_sys_Up/Down but will skip if not found 
#systematics=["Met","FP","btag","mistag","wjethf","zjethf","gjethf"]
systematics=["Met","FP","btag","mistag"]
# Define each of the categories in a dictionary of the following form .. 
#	'name' : the category name 
#	'in_file_name' : input ntuple file for this category 
#	'cutstring': add simple cutrstring, applicable to ALL regions in this category (eg mvamet > 200)
#	'varstring': the main variable to be fit in this category (eg mvamet), must be named as the branch in the ntuples
#	'weightname': name of the weight variable 
#	'bins': binning given as a python list
#	'additionalvars': list additional variables to be histogrammed by the first stage, give as a list of lists, each list element 
#			  as ['variablename',nbins,min,max]
#	'pdfmodel': integer --> N/A  redudant for now unless we move back to parameteric fitting estimates
# 	'samples' : define tree->region/process map given as a dictionary with each entry as follows 
#		TreeName : ['region','process',isMC,isSignal] --> Note isSignal means DM/Higgs etc for signal region but Z-jets/W-jets for the di/single-muon regions !!!

#  OPTIONAL --> 'extra_cuts': additional cuts maybe specific to this control region (eg ptphoton cuts) if this key is missing, the code will not complain   
 
monotop_category = {
	    'name':"monotop"
	   #,'in_file_name':"/afs/cern.ch/user/p/pharris/pharris/public/bacon/prod/CMSSW_7_4_12_patch1/src/MonoX/../BaconAnalyzer/MJSelection/skim/monojet-combo-electron.root"  # Without recoil corrections
	   #,'in_file_name':"/afs/cern.ch/user/p/pharris/pharris/public/bacon/prod/CMSSW_7_4_12_patch1/src/MonoX/monojet-combo-electron.root_recoil"
       #,'in_file_name':"files/monotop-boosted-combo-weight.root"
#       ,'in_file_name':"files/monotop-boosted-combo-mar9.root"
       ,'in_file_name':"files/limitForest.root"
	   ,"cutstring":"met>250 && met<1000"
	   ,"varstring":["met",250,1000]
	   ,"weightname":"weight"
	   ,"bins":bins[:]
	   #,"bins":[200.0 , 210.0 , 220.0 , 230.0 , 240.0 , 250.0 , 260.0 , 270.0 , 280.0 , 290.0 , 300.0 , 310.0 , 320.0 , 330.0,340,360,380,420,510,1000]
  	   #,"additionalvars":[['jet1pt',25,150,1000]]
	   ,"additionalvars":[]
           ,"pdfmodel":0
	   #,"extra_cuts":[["singleelectron","rmet>40"],["photon","ptpho>200"]]
	   #,"extra_cuts":[["singleelectron","rmet>40"]]
	   ,"samples":
	   	{  
		  # Signal Region
		   "signal_Zvv"  	           :['signal','zjets',1,0]
      ,"signal_Zll"	             :['signal','zll',1,0]
 		  ,"signal_Wlv"  	           :['signal','wjets',1,0]
		  ,"signal_Diboson"  	       :['signal','dibosons',1,0]
		  ,"signal_TTbar"   	       :['signal','ttbar',1,0]
		  ,"signal_ST"               :['signal','stop',1,0]
		  ,"signal_QCD"		   	       :['signal','qcd',1,0]
		  ,"signal_Data"	           :['signal','data',0,0]

		  # some signals 
		  ,"signal_res_mMed1900"		   :['signal','Mres1900_Mchi100',1,1]
      ,"signal_fcnc_mMed1100"		   :['signal','Mchi1100',1,1]

		  # Di muon-Control
      ,"dimuon_Zll"	             :['dimuon','zll',1,0]
 		  ,"dimuon_Wlv"  	           :['dimuon','wjets',1,0]
		  ,"dimuon_Diboson"  	       :['dimuon','dibosons',1,0]
		  ,"dimuon_TTbar"   	       :['dimuon','ttbar',1,0]
		  ,"dimuon_ST"               :['dimuon','stop',1,0]
		  ,"dimuon_QCD"		   	       :['dimuon','qcd',1,0]
		  ,"dimuon_Data"	           :['dimuon','data',0,0]

		  # Single muon (top) control
      ,"singlemuontop_Zll"	             :['singlemuontop','zll',1,0]
 		  ,"singlemuontop_Wlv"  	           :['singlemuontop','wjets',1,0]
		  ,"singlemuontop_Diboson"  	       :['singlemuontop','dibosons',1,0]
		  ,"singlemuontop_TTbar"    	       :['singlemuontop','ttbar',1,0]
		  ,"singlemuontop_ST"                :['singlemuontop','stop',1,0]
		  ,"singlemuontop_QCD"		   	       :['singlemuontop','qcd',1,0]
		  ,"singlemuontop_Data"	             :['singlemuontop','data',0,0]

      # Single muon (w) control
      ,"singlemuonw_Zll"	             :['singlemuonw','zll',1,0]
 		  ,"singlemuonw_Wlv"  	           :['singlemuonw','wjets',1,0]
		  ,"singlemuonw_Diboson"  	       :['singlemuonw','dibosons',1,0]
		  ,"singlemuonw_TTbar"    	       :['singlemuonw','ttbar',1,0]
		  ,"singlemuonw_ST"                :['singlemuonw','stop',1,0]
		  ,"singlemuonw_QCD"		   	       :['singlemuonw','qcd',1,0]
		  ,"singlemuonw_Data"	             :['singlemuonw','data',0,0]

		  # Di electron-Control
      ,"dielectron_Zll"	             :['dielectron','zll',1,0]
 		  ,"dielectron_Wlv"  	           :['dielectron','wjets',1,0]
		  ,"dielectron_Diboson"  	       :['dielectron','dibosons',1,0]
		  ,"dielectron_TTbar"   	       :['dielectron','ttbar',1,0]
		  ,"dielectron_ST"               :['dielectron','stop',1,0]
		  ,"dielectron_QCD"		   	       :['dielectron','qcd',1,0]
		  ,"dielectron_Data"	           :['dielectron','data',0,0]

		  # Single electron (top) control
      ,"singleelectrontop_Zll"	             :['singleelectrontop','zll',1,0]
 		  ,"singleelectrontop_Wlv"  	           :['singleelectrontop','wjets',1,0]
		  ,"singleelectrontop_Diboson"  	       :['singleelectrontop','dibosons',1,0]
		  ,"singleelectrontop_TTbar"    	       :['singleelectrontop','ttbar',1,0]
		  ,"singleelectrontop_ST"                :['singleelectrontop','stop',1,0]
		  ,"singleelectrontop_QCD"		   	       :['singleelectrontop','qcd',1,0]
		  ,"singleelectrontop_Data"	             :['singleelectrontop','data',0,0]

      # Single electron (w) control
      ,"singleelectronw_Zll"	             :['singleelectronw','zll',1,0]
 		  ,"singleelectronw_Wlv"  	           :['singleelectronw','wjets',1,0]
		  ,"singleelectronw_Diboson"  	       :['singleelectronw','dibosons',1,0]
		  ,"singleelectronw_TTbar"    	       :['singleelectronw','ttbar',1,0]
		  ,"singleelectronw_ST"                :['singleelectronw','stop',1,0]
		  ,"singleelectronw_QCD"		   	       :['singleelectronw','qcd',1,0]
		  ,"singleelectronw_Data"	             :['singleelectronw','data',0,0]

		  # Photon control region
		  ,"photon_Data"	       :['photon','data',0,0]
		  ,"photon_GJets"        :['photon','gjets',1,1]
      ,"photon_QCD"     	   :['photon','qcd',1,0]


}
categories = [monotop_category]
