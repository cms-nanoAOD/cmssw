import FWCore.ParameterSet.Config as cms
from PhysicsTools.NanoAOD.common_cff import *
from PhysicsTools.JetMCAlgos.TauGenJets_cfi import tauGenJets
from PhysicsTools.JetMCAlgos.TauGenJetsDecayModeSelectorAllHadrons_cfi import tauGenJetsSelectorAllHadrons 

##################### Updated tau collection with MVA-based tau-Ids rerun #######
# Used only in some eras
from RecoTauTag.Configuration.loadRecoTauTagMVAsFromPrepDB_cfi import *
from RecoTauTag.RecoTau.PATTauDiscriminationByMVAIsolationRun2_cff import *

### MVAIso 2017v2
## DBoldDM
# Raw
patTauDiscriminationByIsolationMVArun2v1DBoldDMwLTraw = patDiscriminationByIsolationMVArun2v1raw.clone(
   PATTauProducer = cms.InputTag('slimmedTaus'),
   Prediscriminants = noPrediscriminants,
   loadMVAfromDB = cms.bool(True),
   mvaName = cms.string("RecoTauTag_tauIdMVAIsoDBoldDMwLT2017v2"), # name of the training you want to use
   mvaOpt = cms.string("DBoldDMwLTwGJ"), # option you want to use for your training (i.e., which variables are used to compute the BDT score)
   requireDecayMode = cms.bool(True),
   verbosity = cms.int32(0)
)
# VVLoose WP
patTauDiscriminationByVVLooseIsolationMVArun2v1DBoldDMwLT = patDiscriminationByIsolationMVArun2v1VLoose.clone(
   PATTauProducer = cms.InputTag('slimmedTaus'),
   Prediscriminants = noPrediscriminants,
   toMultiplex = cms.InputTag('patTauDiscriminationByIsolationMVArun2v1DBoldDMwLTraw'),
   key = cms.InputTag('patTauDiscriminationByIsolationMVArun2v1DBoldDMwLTraw','category'),
   loadMVAfromDB = cms.bool(True),
   mvaOutput_normalization = cms.string("RecoTauTag_tauIdMVAIsoDBoldDMwLT2017v2_mvaOutput_normalization"), # normalization fo the training you want to use
   mapping = cms.VPSet(
      cms.PSet(
         category = cms.uint32(0),
         cut = cms.string("RecoTauTag_tauIdMVAIsoDBoldDMwLT2017v2_WPEff95"), # this is the name of the working point you want to use
         variable = cms.string("pt"),
      )
   )
)
# VLoose WP
patTauDiscriminationByVLooseIsolationMVArun2v1DBoldDMwLT = patTauDiscriminationByVVLooseIsolationMVArun2v1DBoldDMwLT.clone()
patTauDiscriminationByVLooseIsolationMVArun2v1DBoldDMwLT.mapping[0].cut = cms.string("RecoTauTag_tauIdMVAIsoDBoldDMwLT2017v2_WPEff90")
# Loose WP
patTauDiscriminationByLooseIsolationMVArun2v1DBoldDMwLT = patTauDiscriminationByVVLooseIsolationMVArun2v1DBoldDMwLT.clone()
patTauDiscriminationByLooseIsolationMVArun2v1DBoldDMwLT.mapping[0].cut = cms.string("RecoTauTag_tauIdMVAIsoDBoldDMwLT2017v2_WPEff80")
# Medium WP
patTauDiscriminationByMediumIsolationMVArun2v1DBoldDMwLT = patTauDiscriminationByVVLooseIsolationMVArun2v1DBoldDMwLT.clone()
patTauDiscriminationByMediumIsolationMVArun2v1DBoldDMwLT.mapping[0].cut = cms.string("RecoTauTag_tauIdMVAIsoDBoldDMwLT2017v2_WPEff70")
# Tight WP
patTauDiscriminationByTightIsolationMVArun2v1DBoldDMwLT = patTauDiscriminationByVVLooseIsolationMVArun2v1DBoldDMwLT.clone()
patTauDiscriminationByTightIsolationMVArun2v1DBoldDMwLT.mapping[0].cut = cms.string("RecoTauTag_tauIdMVAIsoDBoldDMwLT2017v2_WPEff60")
# VTight WP
patTauDiscriminationByVTightIsolationMVArun2v1DBoldDMwLT = patTauDiscriminationByVVLooseIsolationMVArun2v1DBoldDMwLT.clone()
patTauDiscriminationByVTightIsolationMVArun2v1DBoldDMwLT.mapping[0].cut = cms.string("RecoTauTag_tauIdMVAIsoDBoldDMwLT2017v2_WPEff50")
# VVTights WP
patTauDiscriminationByVVTightIsolationMVArun2v1DBoldDMwLT = patTauDiscriminationByVVLooseIsolationMVArun2v1DBoldDMwLT.clone()
patTauDiscriminationByVVTightIsolationMVArun2v1DBoldDMwLT.mapping[0].cut = cms.string("RecoTauTag_tauIdMVAIsoDBoldDMwLT2017v2_WPEff40")
# MVAIso DBoldDM Seqeunce
patTauDiscriminationByIsolationMVArun2v1DBoldDMwLTSeq = cms.Sequence(
    patTauDiscriminationByIsolationMVArun2v1DBoldDMwLTraw
    + patTauDiscriminationByVVLooseIsolationMVArun2v1DBoldDMwLT
    + patTauDiscriminationByVLooseIsolationMVArun2v1DBoldDMwLT
    + patTauDiscriminationByLooseIsolationMVArun2v1DBoldDMwLT
    + patTauDiscriminationByMediumIsolationMVArun2v1DBoldDMwLT
    + patTauDiscriminationByTightIsolationMVArun2v1DBoldDMwLT
    + patTauDiscriminationByVTightIsolationMVArun2v1DBoldDMwLT
    + patTauDiscriminationByVVTightIsolationMVArun2v1DBoldDMwLT
)
## DBnewDM
# Raw
patTauDiscriminationByIsolationMVArun2v1DBnewDMwLTraw = patDiscriminationByIsolationMVArun2v1raw.clone(
   PATTauProducer = cms.InputTag('slimmedTaus'),
   Prediscriminants = noPrediscriminants,
   loadMVAfromDB = cms.bool(True),
   mvaName = cms.string("RecoTauTag_tauIdMVAIsoDBnewDMwLT2017v2"), # name of the training you want to use
   mvaOpt = cms.string("DBnewDMwLTwGJ"), # option you want to use for your training (i.e., which variables are used to compute the BDT score)
   requireDecayMode = cms.bool(True),
   verbosity = cms.int32(0)
)
# VVLoose WP
patTauDiscriminationByVVLooseIsolationMVArun2v1DBnewDMwLT = patDiscriminationByIsolationMVArun2v1VLoose.clone(
   PATTauProducer = cms.InputTag('slimmedTaus'),
   Prediscriminants = noPrediscriminants,
   toMultiplex = cms.InputTag('patTauDiscriminationByIsolationMVArun2v1DBnewDMwLTraw'),
   key = cms.InputTag('patTauDiscriminationByIsolationMVArun2v1DBnewDMwLTraw','category'),
   loadMVAfromDB = cms.bool(True),
   mvaOutput_normalization = cms.string("RecoTauTag_tauIdMVAIsoDBnewDMwLT2017v2_mvaOutput_normalization"), # normalization fo the training you want to use
   mapping = cms.VPSet(
      cms.PSet(
         category = cms.uint32(0),
         cut = cms.string("RecoTauTag_tauIdMVAIsoDBnewDMwLT2017v2_WPEff95"), # this is the name of the working point you want to use
         variable = cms.string("pt"),
      )
   )
)
# VLoose WP
patTauDiscriminationByVLooseIsolationMVArun2v1DBnewDMwLT = patTauDiscriminationByVVLooseIsolationMVArun2v1DBnewDMwLT.clone()
patTauDiscriminationByVLooseIsolationMVArun2v1DBnewDMwLT.mapping[0].cut = cms.string("RecoTauTag_tauIdMVAIsoDBnewDMwLT2017v2_WPEff90")
# Loose WP
patTauDiscriminationByLooseIsolationMVArun2v1DBnewDMwLT = patTauDiscriminationByVVLooseIsolationMVArun2v1DBnewDMwLT.clone()
patTauDiscriminationByLooseIsolationMVArun2v1DBnewDMwLT.mapping[0].cut = cms.string("RecoTauTag_tauIdMVAIsoDBnewDMwLT2017v2_WPEff80")
# Medium WP
patTauDiscriminationByMediumIsolationMVArun2v1DBnewDMwLT = patTauDiscriminationByVVLooseIsolationMVArun2v1DBnewDMwLT.clone()
patTauDiscriminationByMediumIsolationMVArun2v1DBnewDMwLT.mapping[0].cut = cms.string("RecoTauTag_tauIdMVAIsoDBnewDMwLT2017v2_WPEff70")
# Tight WP
patTauDiscriminationByTightIsolationMVArun2v1DBnewDMwLT = patTauDiscriminationByVVLooseIsolationMVArun2v1DBnewDMwLT.clone()
patTauDiscriminationByTightIsolationMVArun2v1DBnewDMwLT.mapping[0].cut = cms.string("RecoTauTag_tauIdMVAIsoDBnewDMwLT2017v2_WPEff60")
# VTight WP
patTauDiscriminationByVTightIsolationMVArun2v1DBnewDMwLT = patTauDiscriminationByVVLooseIsolationMVArun2v1DBnewDMwLT.clone()
patTauDiscriminationByVTightIsolationMVArun2v1DBnewDMwLT.mapping[0].cut = cms.string("RecoTauTag_tauIdMVAIsoDBnewDMwLT2017v2_WPEff50")
# VVTights WP
patTauDiscriminationByVVTightIsolationMVArun2v1DBnewDMwLT = patTauDiscriminationByVVLooseIsolationMVArun2v1DBnewDMwLT.clone()
patTauDiscriminationByVVTightIsolationMVArun2v1DBnewDMwLT.mapping[0].cut = cms.string("RecoTauTag_tauIdMVAIsoDBnewDMwLT2017v2_WPEff40")
# MVAIso DBnewDM Seqeunce
patTauDiscriminationByIsolationMVArun2v1DBnewDMwLTSeq = cms.Sequence(
    patTauDiscriminationByIsolationMVArun2v1DBnewDMwLTraw
    + patTauDiscriminationByVVLooseIsolationMVArun2v1DBnewDMwLT
    + patTauDiscriminationByVLooseIsolationMVArun2v1DBnewDMwLT
    + patTauDiscriminationByLooseIsolationMVArun2v1DBnewDMwLT
    + patTauDiscriminationByMediumIsolationMVArun2v1DBnewDMwLT
    + patTauDiscriminationByTightIsolationMVArun2v1DBnewDMwLT
    + patTauDiscriminationByVTightIsolationMVArun2v1DBnewDMwLT
    + patTauDiscriminationByVVTightIsolationMVArun2v1DBnewDMwLT
)
## DBoldDMdR0p3
# Raw
patTauDiscriminationByIsolationMVArun2v1DBoldDMdR0p3wLTraw = patDiscriminationByIsolationMVArun2v1raw.clone(
   PATTauProducer = cms.InputTag('slimmedTaus'),
   Prediscriminants = noPrediscriminants,
   loadMVAfromDB = cms.bool(True),
   mvaName = cms.string("RecoTauTag_tauIdMVAIsoDBoldDMdR0p3wLT2017v2"), # name of the training you want to use
   mvaOpt = cms.string("DBoldDMwLTwGJ"), # option you want to use for your training (i.e., which variables are used to compute the BDT score)
   requireDecayMode = cms.bool(True),
   srcChargedIsoPtSum = cms.string('chargedIsoPtSumdR03'),
   srcFootprintCorrection = cms.string('footprintCorrectiondR03'),
   srcNeutralIsoPtSum = cms.string('neutralIsoPtSumdR03'),
   srcPUcorrPtSum = cms.string('puCorrPtSum'),
   srcPhotonPtSumOutsideSignalCone = cms.string('photonPtSumOutsideSignalConedR03'),
   verbosity = cms.int32(0)
)
# VVLoose WP
patTauDiscriminationByVVLooseIsolationMVArun2v1DBoldDMdR0p3wLT = patDiscriminationByIsolationMVArun2v1VLoose.clone(
   PATTauProducer = cms.InputTag('slimmedTaus'),
   Prediscriminants = noPrediscriminants,
   toMultiplex = cms.InputTag('patTauDiscriminationByIsolationMVArun2v1DBoldDMdR0p3wLTraw'),
   key = cms.InputTag('patTauDiscriminationByIsolationMVArun2v1DBoldDMdR0p3wLTraw','category'),
   loadMVAfromDB = cms.bool(True),
   mvaOutput_normalization = cms.string("RecoTauTag_tauIdMVAIsoDBoldDMdR0p3wLT2017v2_mvaOutput_normalization"), # normalization fo the training you want to use
   mapping = cms.VPSet(
      cms.PSet(
         category = cms.uint32(0),
         cut = cms.string("RecoTauTag_tauIdMVAIsoDBoldDMdR0p3wLT2017v2_WPEff95"), # this is the name of the working point you want to use
         variable = cms.string("pt"),
      )
   )
)
# VLoose WP
patTauDiscriminationByVLooseIsolationMVArun2v1DBoldDMdR0p3wLT = patTauDiscriminationByVVLooseIsolationMVArun2v1DBoldDMdR0p3wLT.clone()
patTauDiscriminationByVLooseIsolationMVArun2v1DBoldDMdR0p3wLT.mapping[0].cut = cms.string("RecoTauTag_tauIdMVAIsoDBoldDMdR0p3wLT2017v2_WPEff90")
# Loose WP
patTauDiscriminationByLooseIsolationMVArun2v1DBoldDMdR0p3wLT = patTauDiscriminationByVVLooseIsolationMVArun2v1DBoldDMdR0p3wLT.clone()
patTauDiscriminationByLooseIsolationMVArun2v1DBoldDMdR0p3wLT.mapping[0].cut = cms.string("RecoTauTag_tauIdMVAIsoDBoldDMdR0p3wLT2017v2_WPEff80")
# Medium WP
patTauDiscriminationByMediumIsolationMVArun2v1DBoldDMdR0p3wLT = patTauDiscriminationByVVLooseIsolationMVArun2v1DBoldDMdR0p3wLT.clone()
patTauDiscriminationByMediumIsolationMVArun2v1DBoldDMdR0p3wLT.mapping[0].cut = cms.string("RecoTauTag_tauIdMVAIsoDBoldDMdR0p3wLT2017v2_WPEff70")
# Tight WP
patTauDiscriminationByTightIsolationMVArun2v1DBoldDMdR0p3wLT = patTauDiscriminationByVVLooseIsolationMVArun2v1DBoldDMdR0p3wLT.clone()
patTauDiscriminationByTightIsolationMVArun2v1DBoldDMdR0p3wLT.mapping[0].cut = cms.string("RecoTauTag_tauIdMVAIsoDBoldDMdR0p3wLT2017v2_WPEff60")
# VTight WP
patTauDiscriminationByVTightIsolationMVArun2v1DBoldDMdR0p3wLT = patTauDiscriminationByVVLooseIsolationMVArun2v1DBoldDMdR0p3wLT.clone()
patTauDiscriminationByVTightIsolationMVArun2v1DBoldDMdR0p3wLT.mapping[0].cut = cms.string("RecoTauTag_tauIdMVAIsoDBoldDMdR0p3wLT2017v2_WPEff50")
# VVTights WP
patTauDiscriminationByVVTightIsolationMVArun2v1DBoldDMdR0p3wLT = patTauDiscriminationByVVLooseIsolationMVArun2v1DBoldDMdR0p3wLT.clone()
patTauDiscriminationByVVTightIsolationMVArun2v1DBoldDMdR0p3wLT.mapping[0].cut = cms.string("RecoTauTag_tauIdMVAIsoDBoldDMdR0p3wLT2017v2_WPEff40")
# MVAIso DBoldDMdR0p3 Seqeunce
patTauDiscriminationByIsolationMVArun2v1DBoldDMdR0p3wLTSeq = cms.Sequence(
    patTauDiscriminationByIsolationMVArun2v1DBoldDMdR0p3wLTraw
    + patTauDiscriminationByVVLooseIsolationMVArun2v1DBoldDMdR0p3wLT
    + patTauDiscriminationByVLooseIsolationMVArun2v1DBoldDMdR0p3wLT
    + patTauDiscriminationByLooseIsolationMVArun2v1DBoldDMdR0p3wLT
    + patTauDiscriminationByMediumIsolationMVArun2v1DBoldDMdR0p3wLT
    + patTauDiscriminationByTightIsolationMVArun2v1DBoldDMdR0p3wLT
    + patTauDiscriminationByVTightIsolationMVArun2v1DBoldDMdR0p3wLT
    + patTauDiscriminationByVVTightIsolationMVArun2v1DBoldDMdR0p3wLT
)
### MVAIso 2015 for Nano on top of MiniAODv2
## DBoldDM
# Raw
patTauDiscriminationByIsolationMVArun2v1DBoldDMwLTraw2015 = patDiscriminationByIsolationMVArun2v1raw.clone(
   PATTauProducer = cms.InputTag('slimmedTaus'),
   Prediscriminants = noPrediscriminants,
   loadMVAfromDB = cms.bool(True),
   mvaName = cms.string("RecoTauTag_tauIdMVADBoldDMwLTv1"), # name of the training you want to use
   mvaOpt = cms.string("DBoldDMwLT"), # option you want to use for your training (i.e., which variables are used to compute the BDT score)
   requireDecayMode = cms.bool(True),
   verbosity = cms.int32(0)
)
# VLoose WP
patTauDiscriminationByVLooseIsolationMVArun2v1DBoldDMwLT2015 = patDiscriminationByIsolationMVArun2v1VLoose.clone(
   PATTauProducer = cms.InputTag('slimmedTaus'),
   Prediscriminants = noPrediscriminants,
   toMultiplex = cms.InputTag('patTauDiscriminationByIsolationMVArun2v1DBoldDMwLTraw2015'),
   key = cms.InputTag('patTauDiscriminationByIsolationMVArun2v1DBoldDMwLTraw2015','category'),
   loadMVAfromDB = cms.bool(True),
   mvaOutput_normalization = cms.string("RecoTauTag_tauIdMVADBoldDMwLTv1_mvaOutput_normalization"), # normalization fo the training you want to use
   mapping = cms.VPSet(
      cms.PSet(
         category = cms.uint32(0),
         cut = cms.string("RecoTauTag_tauIdMVADBoldDMwLTv1_WPEff90"), # this is the name of the working point you want to use
         variable = cms.string("pt"),
      )
   )
)
# Loose WP
patTauDiscriminationByLooseIsolationMVArun2v1DBoldDMwLT2015 = patTauDiscriminationByVLooseIsolationMVArun2v1DBoldDMwLT2015.clone()
patTauDiscriminationByLooseIsolationMVArun2v1DBoldDMwLT2015.mapping[0].cut = cms.string("RecoTauTag_tauIdMVADBoldDMwLTv1_WPEff80")
# Medium WP
patTauDiscriminationByMediumIsolationMVArun2v1DBoldDMwLT2015 = patTauDiscriminationByVLooseIsolationMVArun2v1DBoldDMwLT2015.clone()
patTauDiscriminationByMediumIsolationMVArun2v1DBoldDMwLT2015.mapping[0].cut = cms.string("RecoTauTag_tauIdMVADBoldDMwLTv1_WPEff70")
# Tight WP
patTauDiscriminationByTightIsolationMVArun2v1DBoldDMwLT2015 = patTauDiscriminationByVLooseIsolationMVArun2v1DBoldDMwLT2015.clone()
patTauDiscriminationByTightIsolationMVArun2v1DBoldDMwLT2015.mapping[0].cut = cms.string("RecoTauTag_tauIdMVADBoldDMwLTv1_WPEff60")
# VTight WP
patTauDiscriminationByVTightIsolationMVArun2v1DBoldDMwLT2015 = patTauDiscriminationByVLooseIsolationMVArun2v1DBoldDMwLT2015.clone()
patTauDiscriminationByVTightIsolationMVArun2v1DBoldDMwLT2015.mapping[0].cut = cms.string("RecoTauTag_tauIdMVADBoldDMwLTv1_WPEff50")
# VVTights WP
patTauDiscriminationByVVTightIsolationMVArun2v1DBoldDMwLT2015 = patTauDiscriminationByVLooseIsolationMVArun2v1DBoldDMwLT2015.clone()
patTauDiscriminationByVVTightIsolationMVArun2v1DBoldDMwLT2015.mapping[0].cut = cms.string("RecoTauTag_tauIdMVADBoldDMwLTv1_WPEff40")
# MVAIso DBoldDM Seqeunce
patTauDiscriminationByIsolationMVArun2v1DBoldDMwLT2015Seq = cms.Sequence(
    patTauDiscriminationByIsolationMVArun2v1DBoldDMwLTraw2015
    + patTauDiscriminationByVLooseIsolationMVArun2v1DBoldDMwLT2015
    + patTauDiscriminationByLooseIsolationMVArun2v1DBoldDMwLT2015
    + patTauDiscriminationByMediumIsolationMVArun2v1DBoldDMwLT2015
    + patTauDiscriminationByTightIsolationMVArun2v1DBoldDMwLT2015
    + patTauDiscriminationByVTightIsolationMVArun2v1DBoldDMwLT2015
    + patTauDiscriminationByVVTightIsolationMVArun2v1DBoldDMwLT2015
)


### FIXME: add other tau-Ids when ready

### put all new MVA tau-Id stuff to one Sequence
patTauMVAIDsSeq = cms.Sequence(
    patTauDiscriminationByIsolationMVArun2v1DBoldDMwLTSeq
    +patTauDiscriminationByIsolationMVArun2v1DBnewDMwLTSeq
    +patTauDiscriminationByIsolationMVArun2v1DBoldDMdR0p3wLTSeq
)
_patTauMVAIDsSeqExt = patTauMVAIDsSeq.copy()
_patTauMVAIDsSeqExt += patTauDiscriminationByIsolationMVArun2v1DBoldDMwLT2015Seq
from Configuration.Eras.Modifier_run2_miniAOD_94XFall17_cff import run2_miniAOD_94XFall17
run2_miniAOD_94XFall17.toReplaceWith(patTauMVAIDsSeq,_patTauMVAIDsSeqExt)

# embed new MVA tau-Ids into new tau collection
slimmedTausUpdated = cms.EDProducer("PATTauIDEmbedder",
    src = cms.InputTag('slimmedTaus'),
    tauIDSources = cms.PSet(
        #oldDM
        byIsolationMVArun2v1DBoldDMwLTraw2017v2 = cms.InputTag('patTauDiscriminationByIsolationMVArun2v1DBoldDMwLTraw'),
        byVVLooseIsolationMVArun2v1DBoldDMwLT2017v2 = cms.InputTag('patTauDiscriminationByVVLooseIsolationMVArun2v1DBoldDMwLT'),
        byVLooseIsolationMVArun2v1DBoldDMwLT2017v2 = cms.InputTag('patTauDiscriminationByVLooseIsolationMVArun2v1DBoldDMwLT'),
        byLooseIsolationMVArun2v1DBoldDMwLT2017v2 = cms.InputTag('patTauDiscriminationByLooseIsolationMVArun2v1DBoldDMwLT'),
        byMediumIsolationMVArun2v1DBoldDMwLT2017v2 = cms.InputTag('patTauDiscriminationByMediumIsolationMVArun2v1DBoldDMwLT'),
        byTightIsolationMVArun2v1DBoldDMwLT2017v2 = cms.InputTag('patTauDiscriminationByTightIsolationMVArun2v1DBoldDMwLT'),
        byVTightIsolationMVArun2v1DBoldDMwLT2017v2 = cms.InputTag('patTauDiscriminationByVTightIsolationMVArun2v1DBoldDMwLT'),
        byVVTightIsolationMVArun2v1DBoldDMwLT2017v2 = cms.InputTag('patTauDiscriminationByVVTightIsolationMVArun2v1DBoldDMwLT'),
        #newDM
        byIsolationMVArun2v1DBnewDMwLTraw2017v2 = cms.InputTag('patTauDiscriminationByIsolationMVArun2v1DBnewDMwLTraw'),
        byVVLooseIsolationMVArun2v1DBnewDMwLT2017v2 = cms.InputTag('patTauDiscriminationByVVLooseIsolationMVArun2v1DBnewDMwLT'),
        byVLooseIsolationMVArun2v1DBnewDMwLT2017v2 = cms.InputTag('patTauDiscriminationByVLooseIsolationMVArun2v1DBnewDMwLT'),
        byLooseIsolationMVArun2v1DBnewDMwLT2017v2 = cms.InputTag('patTauDiscriminationByLooseIsolationMVArun2v1DBnewDMwLT'),
        byMediumIsolationMVArun2v1DBnewDMwLT2017v2 = cms.InputTag('patTauDiscriminationByMediumIsolationMVArun2v1DBnewDMwLT'),
        byTightIsolationMVArun2v1DBnewDMwLT2017v2 = cms.InputTag('patTauDiscriminationByTightIsolationMVArun2v1DBnewDMwLT'),
        byVTightIsolationMVArun2v1DBnewDMwLT2017v2 = cms.InputTag('patTauDiscriminationByVTightIsolationMVArun2v1DBnewDMwLT'),
        byVVTightIsolationMVArun2v1DBnewDMwLT2017v2 = cms.InputTag('patTauDiscriminationByVVTightIsolationMVArun2v1DBnewDMwLT'),
        #oldDMdR0p3
        byIsolationMVArun2v1DBdR03oldDMwLTraw2017v2 = cms.InputTag('patTauDiscriminationByIsolationMVArun2v1DBoldDMdR0p3wLTraw'),
        byVVLooseIsolationMVArun2v1DBdR03oldDMwLT2017v2 = cms.InputTag('patTauDiscriminationByVVLooseIsolationMVArun2v1DBoldDMdR0p3wLT'),
        byVLooseIsolationMVArun2v1DBdR03oldDMwLT2017v2 = cms.InputTag('patTauDiscriminationByVLooseIsolationMVArun2v1DBoldDMdR0p3wLT'),
        byLooseIsolationMVArun2v1DBdR03oldDMwLT2017v2 = cms.InputTag('patTauDiscriminationByLooseIsolationMVArun2v1DBoldDMdR0p3wLT'),
        byMediumIsolationMVArun2v1DBdR03oldDMwLT2017v2 = cms.InputTag('patTauDiscriminationByMediumIsolationMVArun2v1DBoldDMdR0p3wLT'),
        byTightIsolationMVArun2v1DBdR03oldDMwLT2017v2 = cms.InputTag('patTauDiscriminationByTightIsolationMVArun2v1DBoldDMdR0p3wLT'),
        byVTightIsolationMVArun2v1DBdR03oldDMwLT2017v2 = cms.InputTag('patTauDiscriminationByVTightIsolationMVArun2v1DBoldDMdR0p3wLT'),
        byVVTightIsolationMVArun2v1DBdR03oldDMwLT2017v2 = cms.InputTag('patTauDiscriminationByVVTightIsolationMVArun2v1DBoldDMdR0p3wLT'),
    )
)
_tauIDSources2015 = cms.PSet(
    byIsolationMVArun2v1DBoldDMwLTraw2015 = cms.InputTag('patTauDiscriminationByIsolationMVArun2v1DBoldDMwLTraw2015'),
    byVLooseIsolationMVArun2v1DBoldDMwLT2015 = cms.InputTag('patTauDiscriminationByVLooseIsolationMVArun2v1DBoldDMwLT2015'),
    byLooseIsolationMVArun2v1DBoldDMwLT2015 = cms.InputTag('patTauDiscriminationByLooseIsolationMVArun2v1DBoldDMwLT2015'),
    byMediumIsolationMVArun2v1DBoldDMwLT2015 = cms.InputTag('patTauDiscriminationByMediumIsolationMVArun2v1DBoldDMwLT2015'),
    byTightIsolationMVArun2v1DBoldDMwLT2015 = cms.InputTag('patTauDiscriminationByTightIsolationMVArun2v1DBoldDMwLT2015'),
    byVTightIsolationMVArun2v1DBoldDMwLT2015 = cms.InputTag('patTauDiscriminationByVTightIsolationMVArun2v1DBoldDMwLT2015'),
    byVVTightIsolationMVArun2v1DBoldDMwLT2015 = cms.InputTag('patTauDiscriminationByVVTightIsolationMVArun2v1DBoldDMwLT2015')
)
_tauIDSourcesExt = cms.PSet(
    slimmedTausUpdated.tauIDSources,
    _tauIDSources2015
)
run2_miniAOD_94XFall17.toModify(slimmedTausUpdated,
          tauIDSources = _tauIDSourcesExt
)

patTauMVAIDsSeq += slimmedTausUpdated

##################### User floats producers, selectors ##########################


finalTaus = cms.EDFilter("PATTauRefSelector",
    src = cms.InputTag("slimmedTausUpdated"),
    cut = cms.string("pt > 18 && tauID('decayModeFindingNewDMs') && (tauID('byLooseCombinedIsolationDeltaBetaCorr3Hits') || tauID('byVLooseIsolationMVArun2v1DBoldDMwLT') || tauID('byVLooseIsolationMVArun2v1DBnewDMwLT') || tauID('byVLooseIsolationMVArun2v1DBdR03oldDMwLT') || tauID('byVVLooseIsolationMVArun2v1DBoldDMwLT2017v2') || tauID('byVVLooseIsolationMVArun2v1DBnewDMwLT2017v2') || tauID('byVVLooseIsolationMVArun2v1DBdR03oldDMwLT2017v2'))")
)
run2_miniAOD_94XFall17.toModify(finalTaus,
          cut =  cms.string("pt > 18 && tauID('decayModeFindingNewDMs') && (tauID('byLooseCombinedIsolationDeltaBetaCorr3Hits') || tauID('byVLooseIsolationMVArun2v1DBoldDMwLT2015') || tauID('byVLooseIsolationMVArun2v1DBnewDMwLT') || tauID('byVLooseIsolationMVArun2v1DBdR03oldDMwLT') || tauID('byVVLooseIsolationMVArun2v1DBoldDMwLT2017v2') || tauID('byVVLooseIsolationMVArun2v1DBnewDMwLT2017v2') || tauID('byVVLooseIsolationMVArun2v1DBdR03oldDMwLT2017v2'))")
)

##################### Tables for final output and docs ##########################
def _tauIdWPMask(pattern, choices, doc=""):
    return Var(" + ".join(["%d * tauID('%s')" % (pow(2,i), pattern % c) for (i,c) in enumerate(choices)]), "uint8", 
               doc=doc+": bitmask "+", ".join(["%d = %s" % (pow(2,i),c) for (i,c) in enumerate(choices)]))
def _tauId2WPMask(pattern,doc):
    return _tauIdWPMask(pattern,choices=("Loose","Tight"),doc=doc)
def _tauId5WPMask(pattern,doc):
    return _tauIdWPMask(pattern,choices=("VLoose","Loose","Medium","Tight","VTight"),doc=doc)
def _tauId6WPMask(pattern,doc):
    return _tauIdWPMask(pattern,choices=("VLoose","Loose","Medium","Tight","VTight","VVTight"),doc=doc)
def _tauId7WPMask(pattern,doc):
    return _tauIdWPMask(pattern,choices=("VVLoose","VLoose","Loose","Medium","Tight","VTight","VVTight"),doc=doc)

tauTable = cms.EDProducer("SimpleCandidateFlatTableProducer",
    src = cms.InputTag("linkedObjects","taus"),
    cut = cms.string(""), #we should not filter on cross linked collections
    name= cms.string("Tau"),
    doc = cms.string("slimmedTaus after basic selection (" + finalTaus.cut.value()+")"),
    singleton = cms.bool(False), # the number of entries is variable
    extension = cms.bool(False), # this is the main table for the taus
    variables = cms.PSet(P4Vars,
       charge = Var("charge", int, doc="electric charge"),                  
       jetIdx = Var("?hasUserCand('jet')?userCand('jet').key():-1", int, doc="index of the associated jet (-1 if none)"),
       decayMode = Var("decayMode()",int),
       idDecayMode = Var("tauID('decayModeFinding')", bool),
       idDecayModeNewDMs = Var("tauID('decayModeFindingNewDMs')", bool),

       leadTkPtOverTauPt = Var("leadChargedHadrCand.pt/pt ",float, doc="pt of the leading track divided by tau pt",precision=10),
       leadTkDeltaEta = Var("leadChargedHadrCand.eta - eta ",float, doc="eta of the leading track, minus tau eta",precision=8),
       leadTkDeltaPhi = Var("deltaPhi(leadChargedHadrCand.phi, phi) ",float, doc="phi of the leading track, minus tau phi",precision=8),

       dxy = Var("leadChargedHadrCand().dxy()",float, doc="d_{xy} of lead track with respect to PV, in cm (with sign)",precision=10),
       dz = Var("leadChargedHadrCand().dz()",float, doc="d_{z} of lead track with respect to PV, in cm (with sign)",precision=14),

       # these are too many, we may have to suppress some
       rawIso = Var( "tauID('byCombinedIsolationDeltaBetaCorrRaw3Hits')", float, doc = "combined isolation (deltaBeta corrections)", precision=10),
       chargedIso = Var( "tauID('chargedIsoPtSum')", float, doc = "charged isolation", precision=10),
       neutralIso = Var( "tauID('neutralIsoPtSum')", float, doc = "neutral (photon) isolation", precision=10),
       puCorr = Var( "tauID('puCorrPtSum')", float, doc = "pileup correction", precision=10),
       footprintCorr = Var( "tauID('footprintCorrection')", float, doc = "footprint correction", precision=10),
       photonsOutsideSignalCone = Var( "tauID('photonPtSumOutsideSignalCone')", float, doc = "sum of photons outside signal cone", precision=10),
                         
       rawMVAnewDM = Var( "tauID('byIsolationMVArun2v1DBnewDMwLTraw')",float, doc="byIsolationMVArun2v1DBnewDMwLT raw output discriminator",precision=10),
       rawMVAnewDM2017v2 = Var( "tauID('byIsolationMVArun2v1DBnewDMwLTraw2017v2')",float, doc="byIsolationMVArun2v1DBnewDMwLT raw output discriminator (2017v2)",precision=10),
       rawMVAoldDM = Var( "tauID('byIsolationMVArun2v1DBoldDMwLTraw')",float, doc="byIsolationMVArun2v1DBoldDMwLT raw output discriminator",precision=10),
       rawMVAoldDM2017v2 = Var( "tauID('byIsolationMVArun2v1DBoldDMwLTraw2017v2')",float, doc="byIsolationMVArun2v1DBoldDMwLT raw output discriminator (2017v2)",precision=10),
       rawMVAoldDMdR03 = Var( "tauID('byIsolationMVArun2v1DBdR03oldDMwLTraw')",float, doc="byIsolationMVArun2v1DBdR03oldDMwLT raw output discriminator",precision=10),
       rawMVAoldDMdR032017v2 = Var( "tauID('byIsolationMVArun2v1DBdR03oldDMwLTraw2017v2')",float, doc="byIsolationMVArun2v1DBdR03oldDMwLT raw output discriminator (2017v2)",precision=10),
       rawAntiEle = Var("tauID('againstElectronMVA6Raw')", float, doc= "Anti-electron MVA discriminator V6 raw output discriminator", precision=10),
       rawAntiEleCat = Var("tauID('againstElectronMVA6category')", int, doc="Anti-electron MVA discriminator V6 category"),
       
       idAntiMu = _tauId2WPMask("againstMuon%s3", doc= "Anti-muon discriminator V3: "),
       idAntiEle = _tauId5WPMask("againstElectron%sMVA6", doc= "Anti-electron MVA discriminator V6"),                         
       idMVAnewDM = _tauId6WPMask( "by%sIsolationMVArun2v1DBnewDMwLT", doc="IsolationMVArun2v1DBnewDMwLT ID working point"),
       idMVAnewDM2017v2 = _tauId7WPMask( "by%sIsolationMVArun2v1DBnewDMwLT2017v2", doc="IsolationMVArun2v1DBnewDMwLT ID working point (2017v2)"),
       idMVAoldDM = _tauId6WPMask( "by%sIsolationMVArun2v1DBoldDMwLT", doc="IsolationMVArun2v1DBoldDMwLT ID working point"),
       idMVAoldDM2017v2 = _tauId7WPMask( "by%sIsolationMVArun2v1DBoldDMwLT2017v2", doc="IsolationMVArun2v1DBoldDMwLT ID working point (2017v2)"),
       idMVAoldDMdR03 = _tauId6WPMask( "by%sIsolationMVArun2v1DBdR03oldDMwLT", doc="IsolationMVArun2v1DBdR03oldDMwLT ID working point"),
       idMVAoldDMdR032017v2 = _tauId7WPMask( "by%sIsolationMVArun2v1DBdR03oldDMwLT2017v2", doc="IsolationMVArun2v1DBoldDMdR0p3wLT ID working point (2017v2)"),
    

#   isoCI3hit = Var(  "tauID("byCombinedIsolationDeltaBetaCorrRaw3Hits")" doc="byCombinedIsolationDeltaBetaCorrRaw3Hits raw output discriminator"),
#   photonOutsideSigCone = Var( "tauID("photonPtSumOutsideSignalCone")" doc="photonPtSumOutsideSignalCone raw output discriminator"),


    )
)
_variables2015 = tauTable.variables.clone()
_variables2015.rawMVAoldDM = Var( "tauID('byIsolationMVArun2v1DBoldDMwLTraw2015')",float, doc="byIsolationMVArun2v1DBoldDMwLT raw output discriminator",precision=10)
_variables2015.idMVAoldDM = _tauId6WPMask( "by%sIsolationMVArun2v1DBoldDMwLT2015", doc="IsolationMVArun2v1DBoldDMwLT ID working point")
run2_miniAOD_94XFall17.toModify(tauTable,
          variables = _variables2015
)
tauGenJets.GenParticles = cms.InputTag("prunedGenParticles")
tauGenJets.includeNeutrinos = cms.bool(False)

genVisTaus = cms.EDProducer("GenVisTauProducer",
    src = cms.InputTag("tauGenJetsSelectorAllHadrons"),         
    srcGenParticles = cms.InputTag("prunedGenParticles")
)

genVisTauTable = cms.EDProducer("SimpleCandidateFlatTableProducer",
    src = cms.InputTag("genVisTaus"),
    cut = cms.string("pt > 10."),
    name = cms.string("GenVisTau"),
    doc = cms.string("gen hadronic taus "),
    singleton = cms.bool(False), # the number of entries is variable
    extension = cms.bool(False), # this is the main table for generator level hadronic tau decays
    variables = cms.PSet(
         pt = Var("pt", float,precision=8),
         phi = Var("phi", float,precision=8),
         eta = Var("eta", float,precision=8),
         mass = Var("mass", float,precision=8),                           
	 charge = Var("charge", int),
	 status = Var("status", int, doc="Hadronic tau decay mode. 0=OneProng0PiZero, 1=OneProng1PiZero, 2=OneProng2PiZero, 10=ThreeProng0PiZero, 11=ThreeProng1PiZero, 15=Other"),
	 genPartIdxMother = Var("?numberOfMothers>0?motherRef(0).key():-1", int, doc="index of the mother particle"),
    )
)

tausMCMatchLepTauForTable = cms.EDProducer("MCMatcher",  # cut on deltaR, deltaPt/Pt; pick best by deltaR
    src         = tauTable.src,                 # final reco collection
    matched     = cms.InputTag("finalGenParticles"), # final mc-truth particle collection
    mcPdgId     = cms.vint32(11,13),            # one or more PDG ID (11 = electron, 13 = muon); absolute values (see below)
    checkCharge = cms.bool(False),              # True = require RECO and MC objects to have the same charge
    mcStatus    = cms.vint32(1),                # PYTHIA status code (1 = stable, 2 = shower, 3 = hard scattering)
    maxDeltaR   = cms.double(0.3),              # Minimum deltaR for the match
    maxDPtRel   = cms.double(0.5),              # Minimum deltaPt/Pt for the match
    resolveAmbiguities    = cms.bool(True),     # Forbid two RECO objects to match to the same GEN object
    resolveByMatchQuality = cms.bool(True),    # False = just match input in order; True = pick lowest deltaR pair first
)

tausMCMatchHadTauForTable = cms.EDProducer("MCMatcher",  # cut on deltaR, deltaPt/Pt; pick best by deltaR
    src         = tauTable.src,                 # final reco collection
    matched     = cms.InputTag("genVisTaus"), # generator level hadronic tau decays
    mcPdgId     = cms.vint32(15),                    # one or more PDG ID (15 = tau); absolute values (see below)
    checkCharge = cms.bool(False),              # True = require RECO and MC objects to have the same charge
    mcStatus    = cms.vint32(),                 # CV: no *not* require certain status code for matching (status code corresponds to decay mode for hadronic tau decays)
    maxDeltaR   = cms.double(0.3),              # Maximum deltaR for the match
    maxDPtRel   = cms.double(1.),               # Maximum deltaPt/Pt for the match
    resolveAmbiguities    = cms.bool(True),     # Forbid two RECO objects to match to the same GEN object
    resolveByMatchQuality = cms.bool(True),    # False = just match input in order; True = pick lowest deltaR pair first
)

tauMCTable = cms.EDProducer("CandMCMatchTableProducer",
    src = tauTable.src,
    mcMap = cms.InputTag("tausMCMatchLepTauForTable"),
    mcMapVisTau = cms.InputTag("tausMCMatchHadTauForTable"),                         
    objName = tauTable.name,
    objType = tauTable.name, #cms.string("Tau"),
    branchName = cms.string("genPart"),
    docString = cms.string("MC matching to status==2 taus"),
)


tauSequence = cms.Sequence(patTauMVAIDsSeq + finalTaus)
tauTables = cms.Sequence(tauTable)
tauMC = cms.Sequence(tauGenJets + tauGenJetsSelectorAllHadrons + genVisTaus + genVisTauTable + tausMCMatchLepTauForTable + tausMCMatchHadTauForTable + tauMCTable)

