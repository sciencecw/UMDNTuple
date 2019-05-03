import FWCore.ParameterSet.Config as cms

import FWCore.ParameterSet.VarParsing as VarParsing
import re

process = cms.Process("UMDNTuple")

# setup 'analysis'  options
opt = VarParsing.VarParsing ('analysis')

opt.register('isMC', -1, VarParsing.VarParsing.multiplicity.singleton, VarParsing.VarParsing.varType.int, 'Flag indicating if the input samples are from MC (1) or from the detector (0).')
opt.register('nEvents', 1000, VarParsing.VarParsing.multiplicity.singleton, VarParsing.VarParsing.varType.int, 'Number of events to analyze')
opt.register('disableEventWeights', 0, VarParsing.VarParsing.multiplicity.singleton, VarParsing.VarParsing.varType.bool, 'Set to 1 to disable event weights')

#input files. Can be changed on the command line with the option inputFiles=...
opt.inputFiles = [
    #'file:/data/users/jkunkle/Samples/aQGC_WWW_SingleLepton_LO/Job_0000/MakeMINIAOD/aQGC_WWW_SingleLepton_LO_MINIAOD.root',
    #'file:/data/users/jkunkle/Samples/WGamma/02FE572F-88DA-E611-8CAB-001E67792884.root',
    #'file:/data/users/jkunkle/Samples/WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/MINIAOD/08F5FD50-23BC-E611-A4C2-00259073E3DA.root',
    #'file:/afs/cern.ch/work/y/yofeng/public/WGamma/SignalMiniAOD/FEAAD8B5-E7FC-E611-81C1-008CFA197B74.root'
    #'root://cms-xrd-global.cern.ch//store/data/Run2016B/SingleMuon/MINIAOD/07Aug17_ver1-v1/70000/F8E02A2B-0E7F-E711-BC53-0CC47A4D761A.root', #rereco legacy16 @ Aug17
    #'/store/mc/RunIISummer16MiniAODv2/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext2-v1/90000/FE8A7852-66E4-E611-B5D0-002590E7E01A.root', # DY MC 2016
    #'/store/mc/RunIIFall17MiniAODv2/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/40000/B4C84D02-5242-E811-AA60-008CFA197A60.root', # DY MC 2017
    #'/store/mc/RunIIFall17MiniAODv2/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/40000/04F71189-4742-E811-AA48-008CFAC9157C.root',
    #'file:/afs/cern.ch/user/k/kawong/UMDNTuple/CMSSW_9_4_9_cand2/src/UMDNTuple/UMDNTuple/04F71189-4742-E811-AA48-008CFAC9157C.root',
    #'file:/eos/cms/store/user/kawong/40BCA89D-2C38-E811-9682-008CFAC93CF8.root',
    #'/store/mc/RunIIFall17MiniAODv2/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/MINIAODSIM/PU2017RECOSIMstep_12Apr2018_94X_mc2017_realistic_v14-v1/910000/ECC11159-F647-E811-A157-001E67792510.root', # DY MC 2017 Madgraph RecoSIM step

	#'/store/mc/RunIIAutumn18MiniAOD/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/102X_upgrade2018_realistic_v15-v1/90000/F46D8BF5-1BDE-464A-A523-D14E2C06D6C6.root', # DY 2018
	'file:/eos/cms/store/user/kawong/F46D8BF5-1BDE-464A-A523-D14E2C06D6C6.root', #DY 2018 local on lxplus eos
    #'file:/afs/cern.ch/work/y/yofeng/public/WGamma/SingleElectronMiniAOD/00622F98-20EB-E611-A0A4-28924A33AFF6.root'
    #'file:/afs/cern.ch/work/y/yofeng/public/WGamma/SingleElectronMiniAOD/FA3923C7-878E-E711-A8BE-0CC47A7C3420.root '
    #'file:/afs/cern.ch/work/y/yofeng/public/WGamma/SignalMiniAOD/FEAAD8B5-E7FC-E611-81C1-008CFA197B74.root'
    #'file:/afs/cern.ch/work/y/yofeng/public/WGamma/QCDMiniAOD/FCF48CF4-C5B1-E611-9D65-0CC47A4D766C.root'
    #'file:/afs/cern.ch/work/y/yofeng/public/WGamma/SingleElectronMiniAOD/00622F98-20EB-E611-A0A4-28924A33AFF6.root'
    #'root://cms-xrd-global.cern.ch//store/data/Run2016G/SingleElectron/MINIAOD/23Sep2016-v1/100000/004A7893-A990-E611-B29F-002590E7DE36.root'
    #'root://cms-xrd-global.cern.ch//store/data/Run2016G/SingleElectron/MINIAOD/03Feb2017-v1/50000/004A75AB-B2EA-E611-B000-24BE05CEFDF1.root',
]


#defaults
#opt.nEvents = 1000
opt.disableEventWeights = 0
opt.parseArguments()

process.source = cms.Source("PoolSource",
                            fileNames =  cms.untracked.vstring(opt.inputFiles))

# try to determine if its data or MC based on the name
# otherwise request the user to provide isMC=
print "isMC: ", opt.isMC
if opt.isMC < 0 and len(process.source.fileNames) > 0:
  if re.match(r'.*/(MINI)?AODSIM/.*', process.source.fileNames[0]):
    print "MC dataset detected."
    opt.isMC = 1
  elif re.match(r'.*/(MINI)?AOD/.*', process.source.fileNames[0]):
    print "Real data dataset detected."
    opt.isMC = 0

if opt.isMC < 0:
  raise Exception("Failed to detect data type. Data type need to be specify with the isMC cmsRun command line option")

process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(opt.nEvents))
#process.source.skipEvents = cms.untracked.uint32(1000)
process.source.duplicateCheckMode = cms.untracked.string('noDuplicateCheck') 

process.TFileService = cms.Service("TFileService",
                                   fileName = cms.string('ntuple.root' )
)


#-----------------------------------------------------
# Configure message logger
#-----------------------------------------------------
process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 1000
#process.MessageLogger.suppressWarning = cms.untracked.vstring('ecalLaserCorrFilter','manystripclus53X','toomanystripclus53X')
process.options = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )
#process.options.allowUnscheduled = cms.untracked.bool(True)
#-----------------------------------------------------

# Load the standard set of configuration modules
# may not need this for MiniAOD v2
process.load('Configuration.StandardSequences.Services_cff')
process.load('Configuration.StandardSequences.GeometryDB_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')

#-----------------------------------
# Load additional MET Filters
# https://twiki.cern.ch/twiki/bin/viewauth/CMS/MissingETOptionalFiltersRun2#How_to_run_the_Bad_Charged_Hadro

process.load('RecoMET.METFilters.BadPFMuonFilter_cfi')
process.BadPFMuonFilter.muons = cms.InputTag("slimmedMuons")
process.BadPFMuonFilter.PFCandidates = cms.InputTag("packedPFCandidates")
process.BadPFMuonFilter.taggingMode = cms.bool( True )

process.load('RecoMET.METFilters.BadChargedCandidateFilter_cfi')
process.BadChargedCandidateFilter.muons = cms.InputTag("slimmedMuons")
process.BadChargedCandidateFilter.PFCandidates = cms.InputTag("packedPFCandidates")
process.BadChargedCandidateFilter.taggingMode = cms.bool( True )




#------------------------------------
#Condition DB tag
from Configuration.AlCa.GlobalTag_condDBv2 import GlobalTag
dataGlobalTag = '102X_dataRun2_Sep2018ABC_v2'	## 2018ABC
#dataGlobalTag = '102X_dataRun2_Prompt_v13' 		## 2018D
mcGlobalTag = '102X_upgrade2018_realistic_v18'

if opt.isMC == 1:
  process.GlobalTag = GlobalTag(process.GlobalTag, mcGlobalTag, '')
else:
  process.GlobalTag = GlobalTag(process.GlobalTag, dataGlobalTag, '')


#------------------------------------
# load Egamma id
from RecoEgamma.EgammaTools.EgammaPostRecoTools import setupEgammaPostRecoSeq
setupEgammaPostRecoSeq(process,
					   #applyEnergyCorrections=False,
                       #applyVIDOnCorrectedEgamma=False,
                       #isMiniAOD=True,
                       #runVID=True,
                       era='2018-Prompt')  # 2018 prompt?
#a sequence egammaPostRecoSeq has now been created and should be added to your path, eg process.p=cms.Path(process.egammaPostRecoSeq)

#--------------------------------------------

#--------------------------------------------
# define the triggers that we want to save
trigger_map = cms.untracked.vstring( 
    # Muon triggers
    '0:HLT_Mu8', 
    '1:HLT_Mu17',
    '2:HLT_Mu19',
    '3:HLT_Mu20',
    '4:HLT_Mu27',
    '5:HLT_Mu50',
    '6:HLT_Mu55',
    '7:HLT_Mu8_TrkIsoVVL', 
    '8:HLT_IsoMu20', 
    '9:HLT_IsoMu24', # intended trigger
    '10:HLT_IsoMu27', # intended trigger
    '11:HLT_IsoMu30', 
    '12:HLT_IsoMu24_eta2p1', 
    '13:HLT_IsoMu27_LooseChargedIsoPFTau20_SingleL1',
    '14:HLT_IsoMu27_MediumChargedIsoPFTau20_SingleL1',
    '15:HLT_IsoMu27_TightChargedIsoPFTau20_SingleL1',
    # Electron triggers
    '20:HLT_Ele20_WPLoose_Gsf',
    '21:HLT_Ele20_WPTight_Gsf',
    '22:HLT_Ele20_eta2p1_WPLoose_Gsf',
    '23:HLT_Ele28_eta2p1_WPTight_Gsf_HT150',
    '24:HLT_Ele27_WPTight_Gsf',  
    '25:HLT_Ele30_eta2p1_WPTight_Gsf_CentralPFJet35_EleCleaned',
    '26:HLT_Ele32_WPTight_Gsf', # intended trigger
    '27:HLT_Ele32_WPTight_Gsf_L1DoubleEG',
    '28:HLT_Ele35_WPTight_Gsf', # intended trigger
    '29:HLT_Ele35_WPTight_Gsf_L1EGMT',
    '30:HLT_Ele38_WPTight_Gsf',
    '31:HLT_Ele40_WPTight_Gsf',
    '32:HLT_Ele135_CaloIdVT_GsfTrkIdT',
    '33:HLT_Ele145_CaloIdVT_GsfTrkIdT',
    '34:HLT_Ele200_CaloIdVT_GsfTrkIdT',
    '35:HLT_Ele250_CaloIdVT_GsfTrkIdT',
    '36:HLT_Ele300_CaloIdVT_GsfTrkIdT',
    # Photon triggers
    '40:HLT_Photon25',
    '41:HLT_Photon33',
    '42:HLT_Photon50', 
    '43:HLT_Photon75', 
    '44:HLT_Photon90', 
    '45:HLT_Photon120', 
    '46:HLT_Photon150', 
    '47:HLT_Photon175', 
    '48:HLT_Photon200',  ## intended trigger
    '49:HLT_Photon300_noHE',
    '50:HLT_Photon50_R9Id90_HE10_IsoM',
    '51:HLT_Photon75_R9Id90_HE10_IsoM',
    '52:HLT_Photon90_R9Id90_HE10_IsoM',
    '53:HLT_Photon120_R9Id90_HE10_IsoM',
    '54:HLT_Photon165_R9Id90_HE10_IsoM',
    '55:HLT_Photon20_HoverELoose',
    '56:HLT_Photon30_HoverELoose',
    '57:HLT_Photon40_HoverELoose',
    '58:HLT_Photon50_HoverELoose',
    '59:HLT_Photon60_HoverELoose',
    '60:HLT_Photon120_R9Id90_HE10_IsoM',
    '61:HLT_Photon165_R9Id90_HE10_IsoM',
    '62:HLT_Photon50_R9Id90_HE10_IsoM',
    '63:HLT_Photon75_R9Id90_HE10_IsoM',
    '64:HLT_Photon90_R9Id90_HE10_IsoM',
    '65:HLT_Photon60_R9Id90_CaloIdL_IsoL_DisplacedIdL',
    '66:HLT_Photon60_R9Id90_CaloIdL_IsoL',
    '67:HLT_Photon60_R9Id90_CaloIdL_IsoL_DisplacedIdL_PFHT350MinPFJet15',
    '68:HLT_Photon50_R9Id90_HE10_IsoM_EBOnly_PFJetsMJJ300DEta3_PFMET50',
    '69:HLT_Photon75_R9Id90_HE10_IsoM_EBOnly_PFJetsMJJ300DEta3',
    '70:HLT_Photon75_R9Id90_HE10_IsoM_EBOnly_PFJetsMJJ600DEta3',
    #DiMuon triggers
    '80:HLT_Mu18_Mu9',
    '81:HLT_Mu18_Mu9_DZ',
    '82:HLT_Mu18_Mu9_SameSign',
    '83:HLT_Mu18_Mu9_SameSign_DZ',
    '84:HLT_Mu20_Mu10',
    '85:HLT_Mu20_Mu10_DZ',
    '86:HLT_Mu20_Mu10_SameSign',
    '87:HLT_Mu20_Mu10_SameSign_DZ',
    '88:HLT_Mu23_Mu12',
    '89:HLT_Mu23_Mu12_DZ',
    '90:HLT_Mu23_Mu12_SameSign',
    '91:HLT_Mu23_Mu12_SameSign_DZ',
    '92:HLT_Mu37_TkMu27',
    '93:HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL',
    '94:HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ', 
    '95:HLT_Mu20_TkMu0_Phi',
    '96:HLT_Mu25_TkMu0_Onia',
    '97:HLT_Mu25_TkMu0_Phi',
    '98:HLT_Mu30_TkMu0_Onia',
    '99:HLT_DoubleIsoMu20_eta2p1',
    '100:HLT_DoubleIsoMu24_eta2p1',
    '101:HLT_DoubleL2Mu50',
    #DiElectron triggers
    '110:HLT_DoubleEle33_CaloIdL_MW',
    '111:HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ', 
    '112:HLT_Ele16_Ele12_Ele8_CaloIdL_TrackIdL',
    '113:HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL', 
    '114:HLT_DoubleEle24_eta2p1_WPTight_Gsf',
    '115:HLT_DoubleEle25_CaloIdL_MW',
    '116:HLT_DoubleEle27_CaloIdL_MW',
    '117:HLT_Ele27_Ele37_CaloIdL_MW',
    # muon + egamma triggers
    '120:HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL', 
    '121:HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ',
    '122:HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL',
    '123:HLT_Mu24_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ',
    '124:HLT_Mu17_Photon30_IsoCaloId',
    '125:HLT_Mu27_Ele37_CaloIdL_MW',
    '125:HLT_Mu37_Ele27_CaloIdL_MW',
    #DiPhoton triggers
    '130:HLT_DoublePhoton33_CaloIdL',
    '131:HLT_DoublePhoton70', 
    '132:HLT_DoublePhoton85',
    )

filter_map = cms.untracked.vstring( 
    '1:Flag_HBHENoiseFilter',
    '2:Flag_HBHENoiseIsoFilter',
    '3:Flag_CSCTightHaloFilter',
    '4:Flag_CSCTightHaloTrkMuUnvetoFilter',
    '5:Flag_CSCTightHalo2015Filter',
    '6:Flag_globalTightHalo2016Filter',
    '7:Flag_globalSuperTightHalo2016Filter',
    '8:Flag_HcalStripHaloFilter',
    '9:Flag_hcalLaserEventFilter',
    '10:Flag_EcalDeadCellTriggerPrimitiveFilter',
    '11:Flag_EcalDeadCellBoundaryEnergyFilter',
    '12:Flag_goodVertices',
    '13:Flag_eeBadScFilter',
    '14:Flag_ecalLaserCorrFilter',
    '15:Flag_trkPOGFilters',
    '16:Flag_chargedHadronTrackResolutionFilter',
    '17:Flag_muonBadTrackFilter',
    '18:Flag_trkPOG_manystripclus53X',
    '19:Flag_trkPOG_toomanystripclus53X',
    '20:Flag_trkPOG_logErrorTooManyClusters',
    # these are added 'manually' because they are not availbe in the miniAOD
    '100:Flag_BadChargedCandidateFilter',
    '101:Flag_BadPFMuonFilter',
)

#process.prefiringweight = cms.EDProducer("L1ECALPrefiringWeightProducer",
#                                 ThePhotons = cms.InputTag("slimmedPhotons"),
#	                         TheJets = cms.InputTag("slimmedJets"),
#                                 L1Maps = cms.string("src/L1Prefiring/EventWeightProducer/data/L1PrefiringMaps_new.root"), # update this line with the location of this file
#                                 #L1Maps = cms.string("L1PrefiringMaps_new.root"), # update this line with the location of this file
#                                 DataEra = cms.string("2017BtoF"), #Use 2016BtoH for 2016
#                                 #DataEra = cms.string("2016BtoH"),
#                                 UseJetEMPt = cms.bool(False), #can be set to true to use jet prefiring maps parametrized vs pt(em) instead of pt
#	                         PrefiringRateSystematicUncty = cms.double(0.2) #Minimum relative prefiring uncty per object
#                                 )

process.UMDNTuple = cms.EDAnalyzer("UMDNTuple",
    electronTag = cms.untracked.InputTag('slimmedElectrons'),
        elecIdVeryLooseStr = cms.untracked.string("cutBasedElectronID-Fall17-94X-V1-veto"),
        elecIdLooseStr     = cms.untracked.string("cutBasedElectronID-Fall17-94X-V1-loose"),
        elecIdMediumStr    = cms.untracked.string("cutBasedElectronID-Fall17-94X-V1-medium"),
        elecIdTightStr     = cms.untracked.string("cutBasedElectronID-Fall17-94X-V1-tight"),
        #elecIdHLTStr       = cms.untracked.string("cutBasedElectronHLTPreselection-Summer16-V1"),
        elecIdHEEPStr      = cms.untracked.string("heepElectronID-HEEPV70"),
        # electron energy scale and smearings
        elecEneCalibStr    = cms.untracked.string('ecalTrkEnergyPostCorr'),
    muonTag     = cms.untracked.InputTag('slimmedMuons'),
    photonTag   = cms.untracked.InputTag('slimmedPhotons'),
        phoChIsoStr    = cms.untracked.string("phoChargedIsolation"),
        phoNeuIsoStr   = cms.untracked.string("phoNeutralHadronIsolation"),
        phoPhoIsoStr   = cms.untracked.string("phoPhotonIsolation"),
        phoIdLooseStr  = cms.untracked.string("cutBasedPhotonID-Fall17-94X-V1-loose"),
        phoIdMediumStr = cms.untracked.string("cutBasedPhotonID-Fall17-94X-V1-medium"),
        phoIdTightStr  = cms.untracked.string("cutBasedPhotonID-Fall17-94X-V1-tight"),
        # photon energy scale and smearings
        phoEneCalibStr = cms.untracked.string("ecalEnergyPostCorr"),
    jetTag     = cms.untracked.InputTag('slimmedJets'),
    fatjetTag     = cms.untracked.InputTag('slimmedJetsAK8'),
    metTag     = cms.untracked.InputTag('slimmedMETs'),
    triggerTag  = cms.untracked.InputTag('TriggerResults', '', 'HLT'),
    triggerObjTag = cms.untracked.InputTag('slimmedPatTrigger'),
    triggerMap = trigger_map,
    metFilterTag  = cms.untracked.InputTag('TriggerResults', '', 'RECO'),
    BadChargedCandidateFilter = cms.untracked.InputTag('BadChargedCandidateFilter'),
    BadPFMuonFilter = cms.untracked.InputTag('BadPFMuonFilter'),
    metFilterMap = filter_map,

    beamSpotTag = cms.untracked.InputTag('offlineBeamSpot'),
    conversionsTag = cms.untracked.InputTag('reducedEgamma', 'reducedConversions' ),
    #conversionsTag = cms.untracked.InputTag('allConversions' ),
    verticesTag  = cms.untracked.InputTag('offlineSlimmedPrimaryVertices'),
    rhoTag  = cms.untracked.InputTag('fixedGridRhoFastjetAll'),
	
	doPref = cms.untracked.bool(False),  #no prefiring weights for 2018
    prefTag = cms.untracked.InputTag('prefiringweight:NonPrefiringProb'),
    prefupTag = cms.untracked.InputTag('prefiringweight:NonPrefiringProbUp'),
    prefdownTag = cms.untracked.InputTag('prefiringweight:NonPrefiringProbDown'),
    puTag   = cms.untracked.InputTag('slimmedAddPileupInfo'),
    lheEventTag  = cms.untracked.InputTag('externalLHEProducer'),
    lheRunTag  = cms.untracked.InputTag('externalLHEProducer'),
    generatorTag = cms.untracked.InputTag('generator'),
    genParticleTag = cms.untracked.InputTag('prunedGenParticles'),

    electronDetailLevel = cms.untracked.int32( 1 ),
    photonDetailLevel = cms.untracked.int32( 1 ),
    muonDetailLevel = cms.untracked.int32( 1 ),
    jetDetailLevel = cms.untracked.int32( 1 ),
    isMC = cms.untracked.int32( opt.isMC ),
    disableEventWeights = cms.untracked.bool( opt.disableEventWeights ),
    prefix_el   = cms.untracked.string("el"),
    prefix_mu   = cms.untracked.string("mu"),
    prefix_ph   = cms.untracked.string("ph"),
    prefix_jet  = cms.untracked.string("jet"),
    prefix_fjet = cms.untracked.string("fjet"),
    prefix_trig = cms.untracked.string("passTrig"),
    prefix_gen  = cms.untracked.string("gen"),
    prefix_met  = cms.untracked.string("met"),
                                   
    electronMinPt = cms.untracked.double( 10 ),
    muonMinPt = cms.untracked.double( 10 ),
    photonMinPt = cms.untracked.double( 20 ),
    jetMinPt = cms.untracked.double( 30 ),
    fjetMinPt = cms.untracked.double( 200 ),
    genMinPt = cms.untracked.double( 5 ),


)


process.p = cms.Path()

#process.p += process.selectedElectrons
process.p += process.egammaPostRecoSeq
# run additional MET filters
process.p += process.BadPFMuonFilter
process.p += process.BadChargedCandidateFilter
#if opt.isMC: process.p += process.prefiringweight

process.p += process.UMDNTuple

