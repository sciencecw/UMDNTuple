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
    'file:/afs/cern.ch/work/y/yofeng/public/WGamma/SignalMiniAOD/FEAAD8B5-E7FC-E611-81C1-008CFA197B74.root'
    #'file:/afs/cern.ch/work/y/yofeng/public/WGamma/SingleElectronMiniAOD/00622F98-20EB-E611-A0A4-28924A33AFF6.root'
    #'file:/afs/cern.ch/work/y/yofeng/public/WGamma/SingleElectronMiniAOD/FA3923C7-878E-E711-A8BE-0CC47A7C3420.root '
    #'root://cms-xrd-global.cern.ch//store/data/Run2016G/SingleElectron/MINIAOD/03Feb2017-v1/50000/004A75AB-B2EA-E611-B000-24BE05CEFDF1.root',
]


#defaults
opt.nEvents = 1000
opt.disableEventWeights = 0

opt.parseArguments()

process.source = cms.Source("PoolSource",
                            fileNames =  cms.untracked.vstring(opt.inputFiles))

# try to determine if its data or MC based on the name
# otherwise request the user to provide isMC=
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
#dataGlobalTag = '80X_dataRun2_2016SeptRepro_v7'
dataGlobalTag = '94X_dataRun2_v10'
#mcGlobalTag = '80X_mcRun2_asymptotic_2016_miniAODv2_v3'
#mcGlobalTag = '80X_mcRun2_asymptotic_2016_TrancheIV_v6'
#mcGlobalTag= '80X_mcRun2_asymptotic_2016_TrancheIV_v8'
mcGlobalTag = '94X_mcRun2_asymptotic_v3'

if opt.isMC == 1:
  process.GlobalTag = GlobalTag(process.GlobalTag, mcGlobalTag, '')
else:
  process.GlobalTag = GlobalTag(process.GlobalTag, dataGlobalTag, '')


#------------------------------------
# load Egamma id
from RecoEgamma.EgammaTools.EgammaPostRecoTools import setupEgammaPostRecoSeq
setupEgammaPostRecoSeq(process, applyEnergyCorrections=False,
                       applyVIDOnCorrectedEgamma=False,
                       isMiniAOD=True,
                       runVID=True,
                       era='2016-Legacy')  #era is new to select between 2016 / 2017,  it defaults to 2017
#a sequence egammaPostRecoSeq has now been created and should be added to your path, eg process.p=cms.Path(process.egammaPostRecoSeq)

#--------------------------------------------

#--------------------------------------------
# define the triggers that we want to save
trigger_map = cms.untracked.vstring( 
    # Muon triggers
    '0:HLT_Mu8',
    '1:HLT_Mu17',
    '2:HLT_Mu20',
    '3:HLT_Mu24',
    '4:HLT_Mu27',
    '5:HLT_Mu34',
    '6:HLT_Mu50',
    '7:HLT_Mu55',
    '8:HLT_Mu300',
    '9:HLT_Mu350',
    '10:HLT_Mu24_eta2p1',
    '11:HLT_Mu45_eta2p1',
    '12:HLT_Mu50_eta2p1',
    '13:HLT_Mu8_TrkIsoVVL',
    '14:HLT_Mu17_TrkIsoVVL',
    '15:HLT_Mu24_TrkIsoVVL',
    '16:HLT_Mu34_TrkIsoVVL',
    '17:HLT_TkMu20',
    '18:HLT_TkMu27',
    '19:HLT_TkMu24_eta2p1',
    '20:HLT_IsoMu18',
    '21:HLT_IsoMu20',
    '22:HLT_IsoMu22',
    '23:HLT_IsoMu24',
    '24:HLT_IsoMu27',
    '25:HLT_IsoMu17_eta2p1',
    '26:HLT_IsoMu20_eta2p1',
    '27:HLT_IsoMu24_eta2p1',
    '28:HLT_IsoTkMu18',
    '29:HLT_IsoTkMu20',
    '30:HLT_IsoTkMu22',
    '31:HLT_IsoTkMu24',
    '32:HLT_IsoTkMu27',
    '33:HLT_IsoTkMu20_eta2p1',
    '34:HLT_IsoTkMu24_eta2p1',
    '35:HLT_Mu16_eta2p1_CaloMET30',
    '36:HLT_IsoMu16_eta2p1_CaloMET30',
    # Electron triggers
    '50:HLT_Ele22_eta2p1_WPLoose_Gsf',
    '51:HLT_Ele22_eta2p1_WPTight_Gsf',
    '52:HLT_Ele23_WPLoose_Gsf',
    '53:HLT_Ele24_eta2p1_WPLoose_Gsf',
    '54:HLT_Ele25_WPTight_Gsf',
    '55:HLT_Ele25_eta2p1_WPLoose_Gsf',
    '56:HLT_Ele25_eta2p1_WPTight_Gsf',
    '57:HLT_Ele27_WPLoose_Gsf',
    '58:HLT_Ele27_WPTight_Gsf',
    '59:HLT_Ele27_eta2p1_WPLoose_Gsf',
    '60:HLT_Ele27_eta2p1_WPTight_Gsf',
    '61:HLT_Ele32_eta2p1_WPLoose_Gsf',
    '62:HLT_Ele32_eta2p1_WPTight_Gsf',
    '63:HLT_Ele35_WPLoose_Gsf',
    '64:HLT_Ele45_WPLoose_Gsf',
    '65:HLT_Ele105_CaloIdVT_GsfTrkIdT',
    '66:HLT_Ele115_CaloIdVT_GsfTrkIdT',
    '67:HLT_Ele12_CaloIdL_TrackIdL_IsoVL',
    '68:HLT_Ele17_CaloIdL_GsfTrkIdVL',
    '69:HLT_Ele17_CaloIdL_TrackIdL_IsoVL',
    '70:HLT_Ele23_CaloIdL_TrackIdL_IsoVL',
    # Photon triggers
    '100:HLT_Photon250_NoHE',
    '101:HLT_Photon300_NoHE',
    '102:HLT_Photon22',
    '103:HLT_Photon30',
    '104:HLT_Photon36',
    '105:HLT_Photon50',
    '106:HLT_Photon75',
    '107:HLT_Photon90',
    '108:HLT_Photon120',
    '109:HLT_Photon175',
    '110:HLT_Photon500',
    '111:HLT_Photon600',
    '112:HLT_Photon165_HE10',
    '113:HLT_Photon22_R9Id90_HE10_IsoM',
    '114:HLT_Photon30_R9Id90_HE10_IsoM',
    '115:HLT_Photon36_R9Id90_HE10_IsoM',
    '116:HLT_Photon50_R9Id90_HE10_IsoM',
    '117:HLT_Photon75_R9Id90_HE10_IsoM',
    '118:HLT_Photon90_R9Id90_HE10_IsoM',
    '119:HLT_Photon120_R9Id90_HE10_IsoM',
    '120:HLT_Photon165_R9Id90_HE10_IsoM',
    '121:HLT_Photon22_R9Id90_HE10_Iso40_EBOnly',
    '122:HLT_Photon36_R9Id90_HE10_Iso40_EBOnly',
    '123:HLT_Photon50_R9Id90_HE10_Iso40_EBOnly',
    '124:HLT_Photon75_R9Id90_HE10_Iso40_EBOnly',
    '125:HLT_Photon90_R9Id90_HE10_Iso40_EBOnly',
    '126:HLT_Photon120_R9Id90_HE10_Iso40_EBOnly',
    #DiMuon triggers
    '150:HLT_Mu17_Mu8',
    '151:HLT_Mu17_Mu8_DZ',
    '152:HLT_Mu17_Mu8_SameSign_DZ',
    '153:HLT_Mu20_Mu10',
    '154:HLT_Mu20_Mu10_DZ',
    '155:HLT_Mu20_Mu10_SameSign_DZ',
    '156:HLT_Mu17_TkMu8_DZ',
    '157:HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL',
    '158:HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ',
    '159:HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL',
    '160:HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ',
    '161:HLT_Mu27_TkMu8',
    '162:HLT_Mu30_TkMu11',
    '163:HLT_Mu40_TkMu11',
    '164:HLT_DoubleIsoMu17_eta2p1',
    '165:HLT_DoubleIsoMu17_eta2p1_noDzCut',
    #DiElectron triggers
    '200:HLT_DoubleEle24_22_eta2p1_WPLoose_Gsf',
    '201:HLT_DoubleEle25_CaloIdL_GsfTrkIdVL',
    '202:HLT_DoubleEle33_CaloIdL',
    '203:HLT_DoubleEle33_CaloIdL_MW',
    '204:HLT_DoubleEle33_CaloIdL_GsfTrkIdVL_MW',
    '205:HLT_DoubleEle33_CaloIdL_GsfTrkIdVL',
    '206:HLT_DoubleEle37_Ele27_CaloIdL_GsfTrkIdVL',
    '207:HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ',
    '208:HLT_Ele17_Ele12_CaloIdL_TrackIdL_IsoVL_DZ',
    '209:HLT_Ele16_Ele12_Ele8_CaloIdL_TrackIdL',
    '210:HLT_Ele17_Ele12_CaloIdL_TrackIdL_IsoVL',
    '211:HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL',
    # muon + egamma triggers
    '212:HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL',
    '213:HLT_Mu8_TrkIsoVVL_Ele17_CaloIdL_TrackIdL_IsoVL',
    '214:HLT_Mu23_TrkIsoVVL_Ele8_CaloIdL_TrackIdL_IsoVL',
    '215:HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL',
    '216:HLT_Mu17_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL',
    '217:HLT_Mu30_Ele30_CaloIdL_GsfTrkIdVL',
    '218:HLT_Mu37_Ele27_CaloIdL_GsfTrkIdVL',
    '219:HLT_Mu27_Ele37_CaloIdL_GsfTrkIdVL',
    '220:HLT_Mu17_Photon30_CaloIdL_L1ISO',
    #DiPhoton triggers
    '250:HLT_DoublePhoton40',
    '251:HLT_DoublePhoton50',
    '252:HLT_DoublePhoton60',
    '253:HLT_DoublePhoton85',
    '254:HLT_Photon26_R9Id85_OR_CaloId24b40e_Iso50T80L_Photon16_AND_HE10_R9Id65_Eta2_Mass60',
    '255:HLT_Photon36_R9Id85_OR_CaloId24b40e_Iso50T80L_Photon22_AND_HE10_R9Id65_Eta2_Mass15',
    '256:HLT_Diphoton30_18_R9Id_OR_IsoCaloId_AND_HE_R9Id_Mass90',
    '257:HLT_Diphoton30_18_R9Id_OR_IsoCaloId_AND_HE_R9Id_DoublePixelSeedMatch_Mass70',
    '258:HLT_Diphoton30PV_18PV_R9Id_AND_IsoCaloId_AND_HE_R9Id_DoublePixelVeto_Mass55',
    '259:HLT_Diphoton30_18_Solid_R9Id_AND_IsoCaloId_AND_HE_R9Id_Mass55',
    '260:HLT_Diphoton30_18_R9Id_OR_IsoCaloId_AND_HE_R9Id_Mass95',
    '261:HLT_Diphoton30EB_18EB_R9Id_OR_IsoCaloId_AND_HE_R9Id_DoublePixelVeto_Mass55',
    '262:HLT_Photon42_R9Id85_OR_CaloId24b40e_Iso50T80L_Photon25_AND_HE10_R9Id65_Eta2_Mass15',
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


process.UMDNTuple = cms.EDAnalyzer("UMDNTuple",
    electronTag = cms.untracked.InputTag('slimmedElectrons'),
        elecIdVeryLooseStr = cms.untracked.string("cutBasedElectronID-Summer16-80X-V1-veto"),
        elecIdLooseStr     = cms.untracked.string("cutBasedElectronID-Summer16-80X-V1-loose"),
        elecIdMediumStr    = cms.untracked.string("cutBasedElectronID-Summer16-80X-V1-medium"),
        elecIdTightStr     = cms.untracked.string("cutBasedElectronID-Summer16-80X-V1-tight"),
        #elecIdHLTStr       = cms.untracked.string("cutBasedElectronHLTPreselection-Summer16-V1"),
        elecIdHEEPStr      = cms.untracked.string("heepElectronID-HEEPV70"),
        # electron energy scale and smearings
        elecEneCalibStr    = cms.untracked.string('ecalTrkEnergyPostCorr'),
    muonTag     = cms.untracked.InputTag('slimmedMuons'),
    photonTag   = cms.untracked.InputTag('slimmedPhotons'),
        phoChIsoStr    = cms.untracked.string("phoChargedIsolation"),
        phoNeuIsoStr   = cms.untracked.string("phoNeutralHadronIsolation"),
        phoPhoIsoStr   = cms.untracked.string("phoPhotonIsolation"),
        phoIdLooseStr  = cms.untracked.string("cutBasedPhotonID-Spring16-V2p2-loose"),
        phoIdMediumStr = cms.untracked.string("cutBasedPhotonID-Spring16-V2p2-medium"),
        phoIdTightStr  = cms.untracked.string("cutBasedPhotonID-Spring16-V2p2-tight"),
        # photon energy scale and smearings
        phoEneCalibStr = cms.untracked.string("ecalEnergyPostCorr"),
    jetTag     = cms.untracked.InputTag('slimmedJets'),
    fatjetTag     = cms.untracked.InputTag('slimmedJetsAK8'),
    metTag     = cms.untracked.InputTag('slimmedMETs'),
    triggerTag  = cms.untracked.InputTag('TriggerResults', '', 'HLT'),
    triggerObjTag = cms.untracked.InputTag('selectedPatTrigger'),
    triggerMap = trigger_map,
    metFilterTag  = cms.untracked.InputTag('TriggerResults', '', 'PAT'),
    BadChargedCandidateFilter = cms.untracked.InputTag('BadChargedCandidateFilter'),
    BadPFMuonFilter = cms.untracked.InputTag('BadPFMuonFilter'),
    metFilterMap = filter_map,

    beamSpotTag = cms.untracked.InputTag('offlineBeamSpot'),
    conversionsTag = cms.untracked.InputTag('reducedEgamma', 'reducedConversions' ),
    #conversionsTag = cms.untracked.InputTag('allConversions' ),
    verticesTag  = cms.untracked.InputTag('offlineSlimmedPrimaryVertices'),
    rhoTag  = cms.untracked.InputTag('fixedGridRhoFastjetAll'),
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

process.p += process.UMDNTuple

