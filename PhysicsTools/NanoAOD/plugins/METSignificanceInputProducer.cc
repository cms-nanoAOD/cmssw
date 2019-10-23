// system include files
#include <memory>

// user include files
#include "DataFormats/Math/interface/deltaR.h"

#include "RecoVertex/VertexTools/interface/VertexDistance3D.h"
#include "RecoVertex/VertexPrimitives/interface/ConvertToFromReco.h"
#include "RecoVertex/VertexPrimitives/interface/VertexState.h"

#include <vector>

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/global/EDProducer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/Run.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/StreamID.h"

#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/VertexReco/interface/Vertex.h"

#include "DataFormats/Common/interface/View.h"
#include "DataFormats/Candidate/interface/VertexCompositePtrCandidate.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"

#include "PhysicsTools/NanoAOD/interface/MatchingUtils.h"
#include "DataFormats/NanoAOD/interface/FlatTable.h"
#include "boost/algorithm/string.hpp"


class METSignificanceInputProducer : public edm::global::EDProducer<> {
    public:

    explicit METSignificanceInputProducer(const edm::ParameterSet &iConfig)
    {
        
        std::vector<edm::InputTag> srcLeptonsTags = iConfig.getParameter< std::vector<edm::InputTag> >("srcLeptons");
        for(std::vector<edm::InputTag>::const_iterator it=srcLeptonsTags.begin();it!=srcLeptonsTags.end();it++) {
            lepTokens_.push_back( consumes<edm::View<reco::Candidate> >( *it ) );
        }

        pfJetsToken_ = consumes<edm::View<pat::Jet> >(iConfig.getParameter<edm::InputTag>("srcPfJets"));
        pfCandidatesToken_ = consumes<edm::View<reco::Candidate> >(iConfig.getParameter<edm::InputTag>("srcPFCandidates"));
        produces<nanoaod::FlatTable>();

        std::vector<edm::ParameterSet> srcParameters = iConfig.getParameter< std::vector<edm::ParameterSet> >("METSigParams");
        for(std::vector<edm::ParameterSet>::const_iterator it=srcParameters.begin();it!=srcParameters.end();it++) {
            dRmatch = (*it).getParameter<double>("dRMatch");
            jetThreshold = (*it).getParameter<double>("jetThreshold");
        }

        dR2match_ = dRmatch*dRmatch;

    }
    
    ~METSignificanceInputProducer() override {};

    //static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);
    bool cleanJet(const pat::Jet& jet, const std::vector< edm::Handle<reco::CandidateView> >& leptons ) const;


    static void fillDescriptions(edm::ConfigurationDescriptions& descriptions){
        edm::ParameterSetDescription desc;

        desc.add<edm::InputTag>("srcPFCandidates")->setComment("input PF candidates collection");
        desc.add<edm::InputTag>("srcPfJets")->setComment("input PF jets collection for cleaning");
        edm::InputTag leps;
        desc.add<std::vector<edm::InputTag>>("srcLeptons")->setComment("input lepton collections for cleaning");  
        edm::ParameterSetDescription params;
        params.add<double>("dRMatch");
        params.add<double>("jetThreshold");
        params.add<std::string>("name");
        desc.addVPSet("METSigParams", params, std::vector<edm::ParameterSet>())->setComment("Parameters");
        //desc.addPSet("METSigParams")->setComment("input parameters");
        descriptions.add("METSigInputTable", desc);

    }


    private:

    void produce(edm::StreamID, edm::Event&, const edm::EventSetup&) const override;


    // ----------member data ---------------------------

    edm::EDGetTokenT<edm::View<pat::Jet> > pfJetsToken_;
    edm::EDGetTokenT<edm::View<reco::Candidate> > pfCandidatesToken_;
    std::vector<edm::EDGetTokenT<edm::View<reco::Candidate> > > lepTokens_;
    std::vector<edm::EDGetTokenT<edm::View<edm::ParameterSet> > > paramTokens_;
    double dR2match_, dRmatch, jetThreshold;

};

namespace {
    struct ptr_hash : public std::unary_function<reco::CandidatePtr, std::size_t> {
        std::size_t operator()(const reco::CandidatePtr& k) const
        {
            if(k.refCore().isTransient()) return (unsigned long)k.refCore().productPtr() ^ k.key();
            else return k.refCore().id().processIndex() ^ k.refCore().id().productIndex() ^ k.key();
        }
    };
}

// ------------ method called to produce the data  ------------
void
METSignificanceInputProducer::produce(edm::StreamID streamID, edm::Event& iEvent, const edm::EventSetup& iSetup) const {

    edm::Handle<reco::CandidateView> pfCandidatesH;
    iEvent.getByToken( pfCandidatesToken_, pfCandidatesH );

    edm::Handle<edm::View<pat::Jet> > jets;
    iEvent.getByToken( pfJetsToken_, jets );

    std::vector< edm::Handle<reco::CandidateView> > leptons;
    for ( std::vector<edm::EDGetTokenT<edm::View<reco::Candidate> > >::const_iterator srcLeptons_i = lepTokens_.begin();
            srcLeptons_i != lepTokens_.end(); ++srcLeptons_i ) {

        edm::Handle<reco::CandidateView> leptons_i;
        iEvent.getByToken(*srcLeptons_i, leptons_i);
        leptons.push_back( leptons_i );
    }

    double resolution, sumPt, sumPtUp, pt, eta, energy;
    const edm::View<reco::Candidate>* pfCandidates=pfCandidatesH.product();

    // for lepton and jet subtraction
    std::unordered_set<reco::CandidatePtr,ptr_hash> footprint;

    // create footprints for leptons with pt>10
    // PF candidates for leptons with pt<10 should be part of sumPt
    for ( const auto& lep_i : leptons ) {
        int nLep = 0;
        for( const auto& lep : *lep_i ) {
            nLep++;
            if( lep.pt() > 10 ){
                for( unsigned int n=0; n < lep.numberOfSourceCandidatePtrs(); n++ ){
                    if( lep.sourceCandidatePtr(n).isNonnull() and lep.sourceCandidatePtr(n).isAvailable() ){
                        footprint.insert(lep.sourceCandidatePtr(n));
                    } 
                }
            }
        }
    }

    // reset sumPt
    sumPt = 0;
    sumPtUp = 0;

    // add footprints of jets
    // and at the same time add jets below threshold to sumPt
    for(const auto& jet : *jets) {
        // disambiguate jets and leptons
        // clean all leptons from jets
        if(!cleanJet(jet, leptons) ) continue;
        // low pt jets are added to sumPt
        if(jet.pt() < jetThreshold){
            sumPt += jet.pt();
            //what to do with sumPtUp??
        }
        // all clean jets are added to footprints so that the associated candidates are not part of sumPt
        for( unsigned int n=0; n < jet.numberOfSourceCandidatePtrs(); n++){
            if( jet.sourceCandidatePtr(n).isNonnull() and jet.sourceCandidatePtr(n).isAvailable() ){
                footprint.insert(jet.sourceCandidatePtr(n));
            }
        }
    }

    // add PF candidate momenta to sumPt
    for(size_t i = 0; i< pfCandidates->size();  ++i) {
        // check if candidate exists in a lepton or jet
        bool cleancand = true;
        if(footprint.find( pfCandidates->ptrAt(i) )==footprint.end()) {
            //dP4 recovery
            for( const auto& it : footprint) {
                if( (it->p4()-(*pfCandidates)[i].p4()).Et2()<0.000025 ){
                    cleancand = false;
                    break;
                }
            }
            resolution = 0;
            // if not, add to sumPt
            if( cleancand ){
                pt = (*pfCandidates)[i].pt();
                energy = (*pfCandidates)[i].energy();
                eta = (*pfCandidates)[i].eta();

                sumPt += pt;

                if ((*pfCandidates)[i].charge() != 0){
                    resolution = sqrt( pow(0.00009*energy,2) + pow(0.0085/sin(2*atan(exp(-eta))),2));
                }
                else if ((*pfCandidates)[i].pdgId() == 130){
                    if (abs(eta) < 1.3){
                        resolution = sqrt(0.64/energy + 0.0025); //min missing
                    }
                    else {
                        resolution = sqrt(1./energy + 0.0016); //min missing
                    }
                }
                else if ((*pfCandidates)[i].pdgId() == 22){
                    resolution = sqrt(0.00009/energy + 0.000001);
                }
                else if ((*pfCandidates)[i].pdgId() == 1 || (*pfCandidates)[i].pdgId() == 2 ){
                    resolution = sqrt(1./energy + 0.0025);
                }
                sumPtUp += (0 + resolution)*pt ;
            }
        }
    }

    auto out = std::make_unique<nanoaod::FlatTable>(1, "MET", true, true);
    out->setDoc("Inputs for MET Significance");
    out->addColumnValue<float>("sumPt", sumPt, "sumPt for MET Significance", nanoaod::FlatTable::FloatColumn);
    out->addColumnValue<float>("sumPtUnclustEnDeltaUp", sumPtUp, "sumPt, unclustered Energy up (MET_sumPt_mod-MET_sumPt)", nanoaod::FlatTable::FloatColumn);
    iEvent.put(std::move(out));

}

//// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
//template <typename T>
//void
//BJetEnergyRegressionVarProducer<T>::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
//  //The following says we do not know what parameters are allowed so do no validation
//  // Please change this to state exactly what you do use, even if it is no parameters
//  edm::ParameterSetDescription desc;
//  desc.add<edm::InputTag>("src")->setComment("jet input collection");
////   desc.add<edm::InputTag>("musrc")->setComment("muons input collection");
////   desc.add<edm::InputTag>("elesrc")->setComment("electrons input collection");
//  desc.add<edm::InputTag>("pvsrc")->setComment("primary vertex input collection");
//  desc.add<edm::InputTag>("svsrc")->setComment("secondary vertex input collection");
//  desc.add<edm::InputTag>("gpsrc")->setComment("genparticles for nu recovery");
//  std::string modname;
//  if (typeid(T) == typeid(pat::Jet)) modname+="Jet";
//  modname+="RegressionVarProducer";
//  descriptions.add(modname,desc);
//}

//typedef METSignificanceInputProducer<double> METSignificanceInputProducer;

bool
METSignificanceInputProducer::cleanJet(const pat::Jet& jet, const std::vector< edm::Handle<reco::CandidateView> >& leptons ) const {
    for ( const auto& lep_i : leptons ) {
        for( const auto& lep : *lep_i ) {
            if (lep.pt() > 0){
                if ( reco::deltaR2(lep, jet) < dR2match_ ) {
                    return false;
                }
            }
        }
    }
    return true;
}


//define this as a plug-in
DEFINE_FWK_MODULE(METSignificanceInputProducer);


