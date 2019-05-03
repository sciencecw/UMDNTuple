
import os
import getpass
USER=getpass.getuser()
import socket
HOST=socket.gethostname()
from argparse import ArgumentParser

p = ArgumentParser()

p.add_argument('--version', dest='version', required=True, help='version' )
p.add_argument('--outputPath', dest='outputPath', default='/store/user/%s/WGamma' %USER, help='output path on storage site, default=/store/user/%s/WGamma' %USER )
p.add_argument('--site', dest='site', default='T3_US_UMD', help='destination site, default=T3_US_UMD' )

options = p.parse_args()




data_samples = [ 
#2018
	'/SingleMuon/Run2018A-17Sep2018-v2/MINIAOD',
	'/SingleMuon/Run2018B-17Sep2018-v1/MINIAOD',
	'/SingleMuon/Run2018C-17Sep2018-v1/MINIAOD',
	#'/SingleMuon/Run2018D-PromptReco-v2/MINIAOD ',
	'/EGamma/Run2018C-17Sep2018-v1/MINIAOD',
	'/EGamma/Run2018B-17Sep2018-v1/MINIAOD',
	'/EGamma/Run2018A-17Sep2018-v2/MINIAOD',
	#'/EGamma/Run2018D-PromptReco-v2/MINIAOD',
]

mc_samples = [
    # list of MC sample
    # The first arugment is the DAS path for the dataset
    # The second argument controls if the EventWeights are saved (removing them saves disk space)
	('/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM',True),
	('/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM',False),
	('/GJets_HT-100To200_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-4cores5k_102X_upgrade2018_realistic_v15-v1/MINIAODSIM',False),
	('/GJets_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM',False),
	('/GJets_HT-400To600_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM',False),
	('/GJets_HT-40To100_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM',False),
	('/GJets_HT-600ToInf_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15_ext1-v2/MINIAODSIM',False),
	('/TTGJets_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM',True),
	('/TTJets_DiLept_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM',False),
	('/TTJets_SingleLeptFromT_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM',False),
	('/TTJets_SingleLeptFromTbar_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM',False),
	('/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15_ext1-v2/MINIAODSIM',True),
	('/TTJets_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM',False),
	('/WGToLNuG_01J_5f_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15_ext1-v1/MINIAODSIM',True),
	('/WGToLNuG_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM',False),
	('/WJetsToLNu_HT-100To200_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM',False),
	('/WJetsToLNu_HT-1200To2500_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM',False),
	('/WJetsToLNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM',False),
	('/WJetsToLNu_HT-2500ToInf_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM',False),
	('/WJetsToLNu_HT-400To600_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM',False),
	('/WJetsToLNu_HT-600To800_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM',False),
	('/WJetsToLNu_HT-800To1200_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM',False),
	('/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM',False),
	('/WWG_TuneCP5_13TeV-amcatnlo-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15_ext1-v2/MINIAODSIM',True),
	('/WWTo2L2Nu_NNPDF31_TuneCP5_13TeV-powheg-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM',False),
	('/WWW_4F_TuneCP5_13TeV-amcatnlo-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15_ext1-v2/MINIAODSIM',True),
	('/ZGToLLG_01J_5f_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15_ext1-v2/MINIAODSIM',True),
    #('/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14_ext1-v1/MINIAODSIM', True),
    # Diphoton missing
	#('/DiPhotonJets_MGG-80toInf_13TeV_amcatnloFXFX_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', True),


     ###   2017 signal samples
     #('/MadGraphChargedResonance_WGToLNuG_M1000_width0p01/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',True ),
     #('/MadGraphChargedResonance_WGToLNuG_M1200_width0p01/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',True ),
     #('/MadGraphChargedResonance_WGToLNuG_M1400_width0p01/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',True ),
     #('/MadGraphChargedResonance_WGToLNuG_M1400_width5/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',True ),
     #('/MadGraphChargedResonance_WGToLNuG_M1800_width5/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',True ),
     #('/MadGraphChargedResonance_WGToLNuG_M2000_width0p01/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',True ),
     #('/MadGraphChargedResonance_WGToLNuG_M2000_width5/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',True ),
     #('/MadGraphChargedResonance_WGToLNuG_M200_width0p01/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',True ),
     #('/MadGraphChargedResonance_WGToLNuG_M2200_width0p01/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',True ),
     #('/MadGraphChargedResonance_WGToLNuG_M2200_width5/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',True ),
     #('/MadGraphChargedResonance_WGToLNuG_M250_width5/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',True ),
     #('/MadGraphChargedResonance_WGToLNuG_M2600_width0p01/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',True ),
     #('/MadGraphChargedResonance_WGToLNuG_M2800_width0p01/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',True ),
     #('/MadGraphChargedResonance_WGToLNuG_M300_width5/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',True ),
     #('/MadGraphChargedResonance_WGToLNuG_M3500_width5/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',True ),
     #('/MadGraphChargedResonance_WGToLNuG_M350_width0p01/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',True ),
     #('/MadGraphChargedResonance_WGToLNuG_M350_width5/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',True ),
     #('/MadGraphChargedResonance_WGToLNuG_M4000_width5/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',True ),
     #('/MadGraphChargedResonance_WGToLNuG_M400_width5/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',True ),
     #('/MadGraphChargedResonance_WGToLNuG_M450_width5/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',True ),
     #('/MadGraphChargedResonance_WGToLNuG_M500_width5/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',True ),
     #('/MadGraphChargedResonance_WGToLNuG_M700_width0p01/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',True ),
     #('/MadGraphChargedResonance_WGToLNuG_M800_width0p01/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',True ),
     #('/MadGraphChargedResonance_WGToLNuG_M800_width5/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',True ),
     #('/MadGraphChargedResonance_WGToLNuG_M900_width0p01/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',True ),
     #('/MadGraphChargedResonance_WGToLNuG_M900_width5/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',True ),

     ### 2017 signal pythia
     #('/PythiaChargedResonance_WGToLNuG_M1000_width5/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',False),
     #('/PythiaChargedResonance_WGToLNuG_M1200_width5/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',False),
     #('/PythiaChargedResonance_WGToLNuG_M1400_width0p01/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',False),
     #('/PythiaChargedResonance_WGToLNuG_M1800_width0p01/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',False),
     #('/PythiaChargedResonance_WGToLNuG_M1800_width5/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',False),
     #('/PythiaChargedResonance_WGToLNuG_M2000_width0p01/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',False),
     #('/PythiaChargedResonance_WGToLNuG_M200_width0p01/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',False),
     #('/PythiaChargedResonance_WGToLNuG_M2200_width5/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',False),
     #('/PythiaChargedResonance_WGToLNuG_M2400_width0p01/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',False),
     #('/PythiaChargedResonance_WGToLNuG_M250_width0p01/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',False),
     #('/PythiaChargedResonance_WGToLNuG_M2600_width0p01/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',False),
     #('/PythiaChargedResonance_WGToLNuG_M300_width0p01/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',False),
     #('/PythiaChargedResonance_WGToLNuG_M300_width5/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',False),
     #('/PythiaChargedResonance_WGToLNuG_M3500_width0p01/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',False),
     #('/PythiaChargedResonance_WGToLNuG_M3500_width5/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',False),
     #('/PythiaChargedResonance_WGToLNuG_M350_width0p01/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',False),
     #('/PythiaChargedResonance_WGToLNuG_M4000_width5/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',False),
     #('/PythiaChargedResonance_WGToLNuG_M450_width0p01/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',False),
     #('/PythiaChargedResonance_WGToLNuG_M450_width5/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',False),
     #('/PythiaChargedResonance_WGToLNuG_M500_width0p01/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',False),
     #('/PythiaChargedResonance_WGToLNuG_M500_width5/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',False),
     #('/PythiaChargedResonance_WGToLNuG_M600_width5/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',False),
     #('/PythiaChargedResonance_WGToLNuG_M800_width0p01/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',False),
]

json_path = 'https://cms-service-dqm.web.cern.ch/cms-service-dqm/CAF/certification/Collisions18/13TeV/PromptReco/Cert_314472-324420_13TeV_PromptReco_Collisions18_JSON.txt'

config_dir = 'crab_configs'

if not os.path.isdir( config_dir ) :
    os.mkdir(config_dir ) 

submit_commands = []

for path in data_samples : 

    base_name = path.split('/')[1]+'_'+path.split('/')[2]

    fname = '%s/%s.py'%(config_dir, base_name)

    ofile = open(fname, 'w' )

    file_entries = []

    file_entries.append( 'from CRABClient.UserUtilities import config' )
    file_entries.append( 'config = config()' )
    file_entries.append( '' )
    file_entries.append( 'config.General.requestName = "production_%s_%s"' %( options.version, base_name ) )
    file_entries.append( 'config.General.workArea = "crab_projects" ' )
    file_entries.append( 'config.General.transferOutputs = True' )
    file_entries.append( 'config.General.transferLogs = False' )
    file_entries.append( '' )
    file_entries.append( 'config.JobType.pluginName = "Analysis"' )
    file_entries.append( 'config.JobType.psetName = "src/UMDNTuple/UMDNTuple/run_production_cfg.py"')
    file_entries.append( 'config.JobType.pyCfgParams = ["isMC=0"]' )
    file_entries.append( '' )
    file_entries.append( 'config.Data.inputDataset = "%s"' %path )
    file_entries.append( 'config.Data.splitting = "LumiBased"' )
    file_entries.append( 'config.Data.unitsPerJob = 30' )
    file_entries.append( 'config.Data.outLFNDirBase = "%s"' %options.outputPath)
    file_entries.append( 'config.Data.publication = False' )
    file_entries.append( 'config.Data.outputDatasetTag = "UMDNTuple_%s"' %options.version )
    file_entries.append( 'config.Data.lumiMask = "%s"' %json_path)
    file_entries.append( '' )
    file_entries.append( 'config.Site.storageSite = "%s"' %options.site )

    for line in file_entries : 
        ofile.write( line + '\n' )

    ofile.close()

    submit_commands.append( 'crab submit --config %s' %( fname ) )

                       



for path, useEventWeights in mc_samples: 

    base_name = path.split('/')[1]

    fname = '%s/%s.py'%(config_dir, base_name)

    ofile = open(fname, 'w' )

    file_entries = []

    file_entries.append('from CRABClient.UserUtilities import config')
    file_entries.append('config = config()')
    file_entries.append('config.General.workArea = "crab_projects"')
    file_entries.append('config.General.transferOutputs = True')
    file_entries.append('config.General.transferLogs = False')
    file_entries.append('config.JobType.pluginName = "Analysis"')
    file_entries.append('config.JobType.psetName = "src/UMDNTuple/UMDNTuple/run_production_cfg.py"')
    file_entries.append('config.Data.outLFNDirBase = "%s"' %options.outputPath)
    file_entries.append('config.Data.publication = False')
    file_entries.append('config.Site.storageSite = "%s"' %options.site)
    file_entries.append('config.Data.outputDatasetTag= "UMDNTuple_%s"' %options.version)
    file_entries.append('config.JobType.pyCfgParams = ["isMC=1","disableEventWeights=%d"]' %(not useEventWeights))
    file_entries.append('config.General.requestName = "production_%s_%s"' %(options.version, base_name))
    file_entries.append('config.Data.inputDataset = "%s"' %path)
    file_entries.append('config.Data.splitting = "Automatic"')
    file_entries.append('config.Data.unitsPerJob = 200')

    for line in file_entries : 
        ofile.write( line + '\n' )

    ofile.close()

    submit_commands.append( 'crab submit --config %s' %( fname ) )

if HOST.count('umd.edu') :
    submit_file = open('submit_crab.csh', 'w' )
    
    submit_file.write( '#!/bin/tcsh\n' )
    #submit_file.write( 'cmsenv\n' )
    #submit_file.write( 'source /cvmfs/cms.cern.ch/crab3/crab.csh\n' )
else : # assume we use bash everywhere else
    submit_file = open('submit_crab.sh', 'w' )
    
    submit_file.write( '#!/bin/bash\n' )
    #submit_file.write( 'cmsenv\n' )
    #submit_file.write( 'source /cvmfs/cms.cern.ch/crab3/crab.sh\n' )


for cmd in submit_commands :
    submit_file.write(cmd + '\n' )


submit_file.close()

                       
