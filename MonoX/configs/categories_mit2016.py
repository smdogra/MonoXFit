# Configuration for a simple monojet topology. Use this as a template for your own Run-2 mono-X analysis
# First provide ouput file name in out_file_name field 
out_file_name = 'mono-x.root'

# can define any thing useful here which may be common to several categories, eg binning in MET 
#bins = range(200,1200,200)
bins = [250,280,310,350,400,450,600,1000]
#bins = [250,280,310,350,400,500,600,1000]
#bins = [250,300,350,400,500,1000]
#bins = [250,300,350,400,500,600,1000]
# will expect samples with sample_sys_Up/Down but will skip if not found 
#systematics=["Met","FP","btag","mistag","wjethf","zjethf","gjethf"]
#systematics=["Met","FP","btag","mistag",'sjbtag','sjmistag']
systematics=["btag","mistag",'sjbtag','sjmistag']
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
        ,'in_file_name':"/local/snarayan/monotop_80_13fb/limits/limitForest.root"
#	   ,"cutstring":"met>250 && met<1000"
#	   ,"varstring":["met",250,1000]
     ,"cutstring":"met>250"
     ,"varstring":["min(999.9999,met)",250,1000]
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
		   "Zvv_signal"  	           :['signal','zjets',1,0]
      ,"Zll_signal"	             :['signal','zll',1,0]
 		  ,"Wlv_signal"  	           :['signal','wjets',1,0]
		  ,"Diboson_signal"  	       :['signal','dibosons',1,0]
		  ,"ttbar_signal"   	       :['signal','ttbar',1,0]
		  ,"ST_signal"               :['signal','stop',1,0]
		  ,"QCD_signal"		   	       :['signal','qcd',1,0]
		  ,"Data_signal"	           :['signal','data',0,0]

		  # some signals 
#		  ,"res_mMed1900_signal"		   :['signal','Mres1900_Mchi100',1,1]
#      ,"fcnc_mMed1100_signal"		   :['signal','Mchi1100',1,1]

		  # Di muon-Control
      ,"Zll_dimuon"	             :['dimuon','zll',1,0]
 		  #,"Wlv_dimuon"  	           :['dimuon','wjets',1,0]
		  ,"Diboson_dimuon"  	       :['dimuon','dibosons',1,0]
		  ,"ttbar_dimuon"   	       :['dimuon','ttbar',1,0]
		  ,"ST_dimuon"               :['dimuon','stop',1,0]
		  ,"QCD_dimuon"		   	       :['dimuon','qcd',1,0]
		  ,"Data_dimuon"	           :['dimuon','data',0,0]

		  # Single muon (top) control
      ,"Zll_singlemuontop"	             :['singlemuontop','zll',1,0]
 		  ,"Wlv_singlemuontop"  	           :['singlemuontop','wjets',1,0]
		  ,"Diboson_singlemuontop"  	       :['singlemuontop','dibosons',1,0]
		  ,"ttbar_singlemuontop"    	       :['singlemuontop','ttbar',1,0]
		  ,"ST_singlemuontop"                :['singlemuontop','stop',1,0]
		  ,"QCD_singlemuontop"		   	       :['singlemuontop','qcd',1,0]
		  ,"Data_singlemuontop"	             :['singlemuontop','data',0,0]

      # Single muon (w) control
      ,"Zll_singlemuonw"	             :['singlemuonw','zll',1,0]
 		  ,"Wlv_singlemuonw"  	           :['singlemuonw','wjets',1,0]
		  ,"Diboson_singlemuonw"  	       :['singlemuonw','dibosons',1,0]
		  ,"ttbar_singlemuonw"    	       :['singlemuonw','ttbar',1,0]
		  ,"ST_singlemuonw"                :['singlemuonw','stop',1,0]
		  ,"QCD_singlemuonw"		   	       :['singlemuonw','qcd',1,0]
		  ,"Data_singlemuonw"	             :['singlemuonw','data',0,0]

		  # Di electron-Control
      ,"Zll_dielectron"	             :['dielectron','zll',1,0]
 		  #,"Wlv_dielectron"  	           :['dielectron','wjets',1,0]
		  ,"Diboson_dielectron"  	       :['dielectron','dibosons',1,0]
		  ,"ttbar_dielectron"   	       :['dielectron','ttbar',1,0]
		  ,"ST_dielectron"               :['dielectron','stop',1,0]
		  ,"QCD_dielectron"		   	       :['dielectron','qcd',1,0]
		  ,"Data_dielectron"	           :['dielectron','data',0,0]

		  # Single electron (top) control
      ,"Zll_singleelectrontop"	             :['singleelectrontop','zll',1,0]
 		  ,"Wlv_singleelectrontop"  	           :['singleelectrontop','wjets',1,0]
		  ,"Diboson_singleelectrontop"  	       :['singleelectrontop','dibosons',1,0]
		  ,"ttbar_singleelectrontop"    	       :['singleelectrontop','ttbar',1,0]
		  ,"ST_singleelectrontop"                :['singleelectrontop','stop',1,0]
		  ,"QCD_singleelectrontop"		   	       :['singleelectrontop','qcd',1,0]
		  ,"Data_singleelectrontop"	             :['singleelectrontop','data',0,0]

      # Single electron (w) control
      ,"Zll_singleelectronw"	             :['singleelectronw','zll',1,0]
 		  ,"Wlv_singleelectronw"  	           :['singleelectronw','wjets',1,0]
		  ,"Diboson_singleelectronw"  	       :['singleelectronw','dibosons',1,0]
		  ,"ttbar_singleelectronw"    	       :['singleelectronw','ttbar',1,0]
		  ,"ST_singleelectronw"                :['singleelectronw','stop',1,0]
		  ,"QCD_singleelectronw"		   	       :['singleelectronw','qcd',1,0]
		  ,"Data_singleelectronw"	             :['singleelectronw','data',0,0]

		  # Photon control region
		  ,"Data_photon"	       :['photon','data',0,0]
		  ,"Pho_photon"          :['photon','gjets',1,1]
      ,"QCD_photon"     	   :['photon','qcd',1,0]

    }
}

# old/76x model:
'''
for m in range(300,1700,200):
  signame = 'monotop_fcnc_mMed%i'%(m)
  monotop_category['samples'][signame+'_signal'] = ['signal',signame+'_v0',1,1]
for m in range(900,2300,200):
  signame = 'monotop_res_mMed%i'%(m)
  monotop_category['samples'][signame+'_signal'] = ['signal',signame+'_v0',1,1]
for m in [1100,2100]:
  signame = 'monotop-nr-%i'%(m)
  oldname = 'monotop_fcnc_mMed%i'%(m)
  monotop_category['samples'][signame+'_signal'] = ['signal',oldname+'_v0',1,1]
'''

# new v3 model
for m in [50]+range(100,2300,200):
  signame = 'monotop-nr-v3-%i-10_med-%i_dm-10'%(m,m)
  monotop_category['samples'][signame+'_signal'] = ['signal',signame,1,1]
for m in range(900,3500,200):
  signame = 'monotop_med-%i_dm-100'%(m)
  monotop_category['samples'][signame+'_signal'] = ['signal',signame,1,1]

categories = [monotop_category]
