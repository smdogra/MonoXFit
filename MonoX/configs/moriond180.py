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
in_file_name = './files/fittingForest_bjet2.root'


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
        # Signal Region
        "TTbar_DiLep_bjet2"             :['signal', 'TTbar_dilep',1,0]
        }
    }


categories = [monotop_category]
