# Configuration for a simple monojet topology. Use this as a template for your own Run-2 mono-X analysis
# First provide ouput file name in out_file_name field 
out_file_name = 'mono-x.root'

# can define any thing useful here which may be common to several categories, eg binning in MET 
#bins = range(200,1200,200)
bins = [160, 200, 250,300,350,400,500,2500]
#bins = [250,280,310,350,400,500,600,1000]
#bins = [250,300,350,400,500,1000]
#bins = [250,300,350,400,500,600,1000]
# will expect samples with sample_sys_Up/Down but will skip if not found 
#systematics=["Met","FP","btag","mistag","wjethf","zjethf","gjethf"]
#systematics=["Met","FP","btag","mistag",'sjbtag','sjmistag']
systematics=["btag","mistag"] #Sunil
# Define each of the categories in a dictionary of the following form .. 
#    'name' : the category name 
#    'in_file_name' : input ntuple file for this category 
#    'cutstring': add simple cutrstring, applicable to ALL regions in this category (eg mvamet > 200)
#    'varstring': the main variable to be fit in this category (eg mvamet), must be named as the branch in the ntuples
#    'weightname': name of the weight variable 
#    'bins': binning given as a python list
#    'additionalvars': list additional variables to be histogrammed by the first stage, give as a list of lists, each list element 
#              as ['variablename',nbins,min,max]
#    'pdfmodel': integer --> N/A  redudant for now unless we move back to parameteric fitting estimates
#     'samples' : define tree->region/process map given as a dictionary with each entry as follows 
#        TreeName : ['region','process',isMC,isSignal] --> Note isSignal means DM/Higgs etc for signal region but Z-jets/W-jets for the di/single-muon regions !!!

#  OPTIONAL --> 'extra_cuts': additional cuts maybe specific to this control region (eg ptphoton cuts) if this key is missing, the code will not complain   
 
#in_file_name = '/data/t3home000/snarayan/store/panda/v_8026_0_5_slim/fitting/fittingForest_stdm.root'
in_file_name = './files/fittingForest.root' # add fittingForest_bjet2.root+fittingForest_bjet1.root+fittingForest_bjet0.root
#in_file_name = '/uscms/homes/s/sdogra/work/CMSSW_8_0_26_patch1/src/PandaAnalysis/MonoX/fitting/fittingForest/fittingForest_bjet2.root'


monotop_category = {
    'name':"monotop"
    ,'in_file_name':in_file_name
    ,"cutstring":"mTw>160 && mTw<1500"
    ,"varstring":["min(999.9999,mTw)",160,2500]
    ,"weightname":"weight"
    ,"bins":bins[:]
    #,"bins":[200.0 , 210.0 , 220.0 , 230.0 , 240.0 , 250.0 , 260.0 , 270.0 , 280.0 , 290.0 , 300.0 , 310.0 , 320.0 , 330.0,340,360,380,420,510,1000]
    #,"additionalvars":[['jet1pt',25,150,1000]]
    #,"additionalvars":[['fj1Tau32',25,0,1],['top_ecf_bdt',25,-1,1]]
    ,"additionalvars":[]
    ,"pdfmodel":0
    ,"samples":
        {  
        # Signal Region bjet=1
        "TTbar_DiLep_bjet1"             :['signal', 'TTbar_dilep',1,0],
        "WJets100_bjet1"                   :['signal', 'WJets',      1,0],
        "WJets200_bjet1"                   :['signal', 'WJets',      1,0],
        "WJets400_bjet1"                   :['signal', 'WJets',      1,0],
        "WJets600_bjet1"                   :['signal', 'WJets',      1,0],
        "WJets800_bjet1"                   :['signal', 'WJets',      1,0],
        "WJets1200_bjet1"                  :['signal', 'WJets',      1,0],
        "WJets2500_bjet1"                  :['signal', 'WJets',      1,0],

        "DYJetsToLL_M50_HT70to100_bjet1"         :['signal', 'DYJetsToLL', 1,0],
        "DYJetsToLL_M50_HT100to200_bjet1"        :['signal', 'DYJetsToLL', 1,0],
        "DYJetsToLL_M50_HT200to400_bjet1"        :['signal', 'DYJetsToLL', 1,0],
        "DYJetsToLL_M50_HT400to600_bjet1"        :['signal', 'DYJetsToLL', 1,0],
        "DYJetsToLL_M50_HT600to800_bjet1"        :['signal', 'DYJetsToLL', 1,0],
        "DYJetsToLL_M50_HT800to1200_bjet1"       :['signal', 'DYJetsToLL', 1,0],
        "DYJetsToLL_M50_HT1200to2500_bjet1"      :['signal', 'DYJetsToLL', 1,0],
        "DYJetsToLL_M50_HT2500toInf_bjet1"       :['signal', 'DYJetsToLL', 1,0],

        "QCD_HT100to200_bjet1"       :['signal', 'QCD', 1,0],
        "QCD_HT200to300_bjet1"       :['signal', 'QCD', 1,0],
        "QCD_HT300to500_bjet1"       :['signal', 'QCD', 1,0],
        "QCD_HT500to700_bjet1"       :['signal', 'QCD', 1,0],
        "QCD_HT700to1000_bjet1"       :['signal', 'QCD', 1,0],
        "QCD_HT1000to1500_bjet1"       :['signal', 'QCD', 1,0],
        "QCD_HT1500to2000_bjet1"       :['signal', 'QCD', 1,0],
        "QCD_HT2000toInf_bjet1"       :['signal', 'QCD', 1,0],

        "TBar_tch_bjet1"       :['signal', 'TBar_tch', 1,0],
        "TBar_tWch_bjet1"       :['signal', 'TBar_tWch', 1,0],

        "TTJets_SingleLeptonFromT_bjet1"       :['signal', 'TTJets_SingleLeptonFromT', 1,0],
        "TTJets_SingleLeptonFromTbar_bjet1"       :['signal', 'TTJets_SingleLeptonFromTbar', 1,0],
        "TTWToLNu_bjet1"                         :['signal', 'TTWToLNu', 1,0],
        "TTZToLLNuNu_bjet1"                         :['signal', 'TTWToLNu', 1,0],
        "TToLeptons_sch_bjet1"                       :['signal', 'TToLeptons_sch', 1,0],
        "T_tWch_bjet1"                       :['signal', 'T_tWch', 1,0],
        "T_tch_bjet1"                       :['signal', 'T_tch', 1,0],

        "WWTo2L2Nu_bjet1"                        :['signal', 'WWTo2L2Nu', 1,0],
        "WWToLNuQQ_bjet1"                       :['signal', 'WWToLNuQQ', 1,0],
        "WZTo1L3Nu_bjet1"                       :['signal', 'WZTo1L3Nu', 1,0],
        "ZZTo2L2Nu_bjet1"                        :['signal', 'ZZTo2L2Nu', 1,0],
        "ZZTo2L2Q_bjet1"                         :['signal', 'ZZTo2L2Q', 1,0],
 
        "ELec2016B_bjet1"                        :['signal', 'Data', 0,0],
        "ELec2016C_bjet1"                        :['signal', 'Data', 0,0],
        "Elec2016D_bjet1"                        :['signal', 'Data', 0,0],
        "Elec2016E_bjet1"                        :['signal', 'Data', 0,0],
        "Elec2016F_bjet1"                        :['signal', 'Data', 0,0],
        "Elec2016G_bjet1"                        :['signal', 'Data', 0,0],
        "Elec2016H2_bjet1"                       :['signal', 'Data', 0,0],
        "Elec2016H3_bjet1"                       :['signal', 'Data', 0,0],

        "Muon2016B_bjet1"                        :['signal', 'Data', 0,0],
        "Muon2016C_bjet1"                        :['signal', 'Data', 0,0],
        "Muon2016D_bjet1"                        :['signal', 'Data', 0,0],
        "Muon2016E_bjet1"                        :['signal', 'Data', 0,0],
        "Muon2016F_bjet1"                        :['signal', 'Data', 0,0],
        "Muon2016G_bjet1"                        :['signal', 'Data', 0,0],
        "Muon2016H2_bjet1"                       :['signal', 'Data', 0,0],
        "Muon2016H3_bjet1"                       :['signal', 'Data', 0,0],
        'Mphi_300_Mchi_200_gSM_0p25_gDM_1p0_bjet1;1'    :['signal','Mphi_300_Mchi_200_gSM_0p25_gDM_1p0',1,1],
        'Mphi_1000_Mchi_200_gSM_0p25_gDM_1p0_bjet1'     :['signal','Mphi_1000_Mchi_200_gSM_0p25_gDM_1p0',1,1],
        'Mphi_2500_Mchi_200_gSM_0p25_gDM_1p0_bjet1'     :['signal','Mphi_2500_Mchi_200_gSM_0p25_gDM_1p0',1,1],

        # Control Region bjet2
        "TTbar_DiLep_bjet2"             :['bjet2', 'TTbar_dilep',1,0],
        "WJets100_bjet2"                   :['bjet2', 'WJets',      1,0],
        "WJets200_bjet2"                   :['bjet2', 'WJets',      1,0],
        "WJets400_bjet2"                   :['bjet2', 'WJets',      1,0],
        "WJets600_bjet2"                   :['bjet2', 'WJets',      1,0],
        "WJets800_bjet2"                   :['bjet2', 'WJets',      1,0],
        "WJets1200_bjet2"                  :['bjet2', 'WJets',      1,0],
        "WJets2500_bjet2"                  :['bjet2', 'WJets',      1,0],

        "DYJetsToLL_M50_HT70to100_bjet2"         :['bjet2', 'DYJetsToLL', 1,0],
        "DYJetsToLL_M50_HT100to200_bjet2"        :['bjet2', 'DYJetsToLL', 1,0],
        "DYJetsToLL_M50_HT200to400_bjet2"        :['bjet2', 'DYJetsToLL', 1,0],
        "DYJetsToLL_M50_HT400to600_bjet2"        :['bjet2', 'DYJetsToLL', 1,0],
        "DYJetsToLL_M50_HT600to800_bjet2"        :['bjet2', 'DYJetsToLL', 1,0],
        "DYJetsToLL_M50_HT800to1200_bjet2"       :['bjet2', 'DYJetsToLL', 1,0],
        "DYJetsToLL_M50_HT1200to2500_bjet2"      :['bjet2', 'DYJetsToLL', 1,0],
        "DYJetsToLL_M50_HT2500toInf_bjet2"       :['bjet2', 'DYJetsToLL', 1,0],

        "QCD_HT100to200_bjet2"       :['bjet2', 'QCD', 1,0],
        "QCD_HT200to300_bjet2"       :['bjet2', 'QCD', 1,0],
        "QCD_HT300to500_bjet2"       :['bjet2', 'QCD', 1,0],
        "QCD_HT500to700_bjet2"       :['bjet2', 'QCD', 1,0],
        "QCD_HT700to1000_bjet2"       :['bjet2', 'QCD', 1,0],
        "QCD_HT1000to1500_bjet2"       :['bjet2', 'QCD', 1,0],
        "QCD_HT1500to2000_bjet2"       :['bjet2', 'QCD', 1,0],
        "QCD_HT2000toInf_bjet2"       :['bjet2', 'QCD', 1,0],

        "TBar_tch_bjet2"       :['bjet2', 'TBar_tch', 1,0],
        "TBar_tWch_bjet2"       :['bjet2', 'TBar_tWch', 1,0],

        "TTJets_SingleLeptonFromT_bjet2"       :['bjet2', 'TTJets_SingleLeptonFromT', 1,0],
        "TTJets_SingleLeptonFromTbar_bjet2"       :['bjet2', 'TTJets_SingleLeptonFromTbar', 1,0],
        "TTWToLNu_bjet2"                         :['bjet2', 'TTWToLNu', 1,0],
        "TTZToLLNuNu_bjet2"                         :['bjet2', 'TTWToLNu', 1,0],
        "TToLeptons_sch_bjet2"                       :['bjet2', 'TToLeptons_sch', 1,0],
        "T_tWch_bjet2"                       :['bjet2', 'T_tWch', 1,0],
        "T_tch_bjet2"                       :['bjet2', 'T_tch', 1,0],

        "WWTo2L2Nu_bjet2"                        :['bjet2', 'WWTo2L2Nu', 1,0],
        "WWToLNuQQ_bjet2"                       :['bjet2', 'WWToLNuQQ', 1,0],
        "WZTo1L3Nu_bjet2"                       :['bjet2', 'WZTo1L3Nu', 1,0],
        "ZZTo2L2Nu_bjet2"                        :['bjet2', 'ZZTo2L2Nu', 1,0],
        "ZZTo2L2Q_bjet2"                         :['bjet2', 'ZZTo2L2Q', 1,0],
 
        "ELec2016B_bjet2"                        :['bjet2', 'Data', 0,0],
        "ELec2016C_bjet2"                        :['bjet2', 'Data', 0,0],
        "Elec2016D_bjet2"                        :['bjet2', 'Data', 0,0],
        "Elec2016E_bjet2"                        :['bjet2', 'Data', 0,0],
        "Elec2016F_bjet2"                        :['bjet2', 'Data', 0,0],
        "Elec2016G_bjet2"                        :['bjet2', 'Data', 0,0],
        "Elec2016H2_bjet2"                       :['bjet2', 'Data', 0,0],
        "Elec2016H3_bjet2"                       :['bjet2', 'Data', 0,0],

        "Muon2016B_bjet2"                        :['bjet2', 'Data', 0,0],
        "Muon2016C_bjet2"                        :['bjet2', 'Data', 0,0],
        "Muon2016D_bjet2"                        :['bjet2', 'Data', 0,0],
        "Muon2016E_bjet2"                        :['bjet2', 'Data', 0,0],
        "Muon2016F_bjet2"                        :['bjet2', 'Data', 0,0],
        "Muon2016G_bjet2"                        :['bjet2', 'Data', 0,0],
        "Muon2016H2_bjet2"                       :['bjet2', 'Data', 0,0],
        "Muon2016H3_bjet2"                       :['bjet2', 'Data', 0,0],


        # Control Region bjet0
        "TTbar_DiLep_bjet0"             :['bjet0', 'TTbar_dilep',1,0],
        "WJets100_bjet0"                   :['bjet0', 'WJets',      1,0],
        "WJets200_bjet0"                   :['bjet0', 'WJets',      1,0],
        "WJets400_bjet0"                   :['bjet0', 'WJets',      1,0],
        "WJets600_bjet0"                   :['bjet0', 'WJets',      1,0],
        "WJets800_bjet0"                   :['bjet0', 'WJets',      1,0],
        "WJets1200_bjet0"                  :['bjet0', 'WJets',      1,0],
        "WJets2500_bjet0"                  :['bjet0', 'WJets',      1,0],

        "DYJetsToLL_M50_HT70to100_bjet0"         :['bjet0', 'DYJetsToLL', 1,0],
        "DYJetsToLL_M50_HT100to200_bjet0"        :['bjet0', 'DYJetsToLL', 1,0],
        "DYJetsToLL_M50_HT200to400_bjet0"        :['bjet0', 'DYJetsToLL', 1,0],
        "DYJetsToLL_M50_HT400to600_bjet0"        :['bjet0', 'DYJetsToLL', 1,0],
        "DYJetsToLL_M50_HT600to800_bjet0"        :['bjet0', 'DYJetsToLL', 1,0],
        "DYJetsToLL_M50_HT800to1200_bjet0"       :['bjet0', 'DYJetsToLL', 1,0],
        "DYJetsToLL_M50_HT1200to2500_bjet0"      :['bjet0', 'DYJetsToLL', 1,0],
        "DYJetsToLL_M50_HT2500toInf_bjet0"       :['bjet0', 'DYJetsToLL', 1,0],

        "QCD_HT100to200_bjet0"       :['bjet0', 'QCD', 1,0],
        "QCD_HT200to300_bjet0"       :['bjet0', 'QCD', 1,0],
        "QCD_HT300to500_bjet0"       :['bjet0', 'QCD', 1,0],
        "QCD_HT500to700_bjet0"       :['bjet0', 'QCD', 1,0],
        "QCD_HT700to1000_bjet0"       :['bjet0', 'QCD', 1,0],
        "QCD_HT1000to1500_bjet0"       :['bjet0', 'QCD', 1,0],
        "QCD_HT1500to2000_bjet0"       :['bjet0', 'QCD', 1,0],
        "QCD_HT2000toInf_bjet0"       :['bjet0', 'QCD', 1,0],

        "TBar_tch_bjet0"       :['bjet0', 'TBar_tch', 1,0],
        "TBar_tWch_bjet0"       :['bjet0', 'TBar_tWch', 1,0],

        "TTJets_SingleLeptonFromT_bjet0"       :['bjet0', 'TTJets_SingleLeptonFromT', 1,0],
        "TTJets_SingleLeptonFromTbar_bjet0"       :['bjet0', 'TTJets_SingleLeptonFromTbar', 1,0],
        "TTWToLNu_bjet0"                         :['bjet0', 'TTWToLNu', 1,0],
        "TTZToLLNuNu_bjet0"                         :['bjet0', 'TTWToLNu', 1,0],
        "TToLeptons_sch_bjet0"                       :['bjet0', 'TToLeptons_sch', 1,0],
        "T_tWch_bjet0"                       :['bjet0', 'T_tWch', 1,0],
        "T_tch_bjet0"                       :['bjet0', 'T_tch', 1,0],

        "WWTo2L2Nu_bjet0"                        :['bjet0', 'WWTo2L2Nu', 1,0],
        "WWToLNuQQ_bjet0"                       :['bjet0', 'WWToLNuQQ', 1,0],
        "WZTo1L3Nu_bjet0"                       :['bjet0', 'WZTo1L3Nu', 1,0],
        "ZZTo2L2Nu_bjet0"                        :['bjet0', 'ZZTo2L2Nu', 1,0],
        "ZZTo2L2Q_bjet0"                         :['bjet0', 'ZZTo2L2Q', 1,0],
 
        "ELec2016B_bjet0"                        :['bjet0', 'Data', 0,0],
        "ELec2016C_bjet0"                        :['bjet0', 'Data', 0,0],
        "Elec2016D_bjet0"                        :['bjet0', 'Data', 0,0],
        "Elec2016E_bjet0"                        :['bjet0', 'Data', 0,0],
        "Elec2016F_bjet0"                        :['bjet0', 'Data', 0,0],
        "Elec2016G_bjet0"                        :['bjet0', 'Data', 0,0],
        "Elec2016H2_bjet0"                       :['bjet0', 'Data', 0,0],
        "Elec2016H3_bjet0"                       :['bjet0', 'Data', 0,0],

        "Muon2016B_bjet0"                        :['bjet0', 'Data', 0,0],
        "Muon2016C_bjet0"                        :['bjet0', 'Data', 0,0],
        "Muon2016D_bjet0"                        :['bjet0', 'Data', 0,0],
        "Muon2016E_bjet0"                        :['bjet0', 'Data', 0,0],
        "Muon2016F_bjet0"                        :['bjet0', 'Data', 0,0],
        "Muon2016G_bjet0"                        :['bjet0', 'Data', 0,0],
        "Muon2016H2_bjet0"                       :['bjet0', 'Data', 0,0],
        "Muon2016H3_bjet0"                       :['bjet0', 'Data', 0,0],

        }
    }


categories = [monotop_category]