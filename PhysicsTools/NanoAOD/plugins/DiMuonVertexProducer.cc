// -*- C++ -*-
//
// Package:    PhysicsTools/NanoAOD
// Class:      DiMuonVertexProducer
// 
/*
 Description: [one line class summary]

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  George Karathanasis georgios.karathanasis@cern.ch
//         Created:  Mon, 7 Dec 2019 09:26:39 GMT
//
//



// system include files
#include <memory>
#include <sstream>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/stream/EDProducer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/StreamID.h"

#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/PatCandidates/interface/CompositeCandidate.h"
#include "CommonTools/Utils/interface/StringCutObjectSelector.h"
#include "CommonTools/Utils/interface/StringObjectFunction.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "DataFormats/NanoAOD/interface/FlatTable.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/Common/interface/View.h"
#include "MagneticField/Engine/interface/MagneticField.h"
#include "MagneticField/Records/interface/IdealMagneticFieldRecord.h"
#include "TrackingTools/TransientTrack/interface/TransientTrack.h"

#include "PhysicsTools/NanoAOD/plugins/SecondaryVertexFitter.h"



constexpr float MUON_MASS= 0.105;

typedef std::vector<reco::TransientTrack> TransientTrackCollection;
typedef std::vector<pat::CompositeCandidate> CompositeCandidateCollection;


class DiMuonVertexProducer : public edm::stream::EDProducer<> {

  public:
     explicit DiMuonVertexProducer(const edm::ParameterSet &iConfig) :
       muons_(consumes<edm::View<pat::Muon>>(iConfig.getParameter<edm::InputTag>("muons"))),
       bspot_{consumes<reco::BeamSpot>( iConfig.getParameter<edm::InputTag>("beamSpot") )},
       pvs_{consumes< std::vector<reco::Vertex> >( iConfig.getParameter<edm::InputTag>("vertices") )},
       mu1_cuts_{iConfig.getParameter<std::string>("mu1Selection")},
       mu2_cuts_{iConfig.getParameter<std::string>("mu2Selection")},
       pre_vtxfit_cuts_{iConfig.getParameter<std::string>("preVtxSelection")},
       post_vtxfit_cuts_{iConfig.getParameter<std::string>("postVtxSelection")},
       refit_{iConfig.getParameter<bool>("RefitTracks")},
       fitTunePTransientTracks_{iConfig.getParameter<bool>("FitTunePTransientTracks")}
       {       
          produces<pat::CompositeCandidateCollection>("diMuons");
       }

        ~DiMuonVertexProducer() override {}

    private:
        void produce(edm::Event&, edm::EventSetup const&) override ;

        const edm::EDGetTokenT<edm::View<pat::Muon>> muons_;
        const edm::EDGetTokenT<reco::BeamSpot> bspot_; 
        const edm::EDGetTokenT<std::vector<reco::Vertex>> pvs_;
        const StringCutObjectSelector<pat::Muon> mu1_cuts_;
        const StringCutObjectSelector<pat::Muon> mu2_cuts_;
        const StringCutObjectSelector<pat::CompositeCandidate> pre_vtxfit_cuts_;
        const StringCutObjectSelector<pat::CompositeCandidate> post_vtxfit_cuts_;        
        bool refit_;
        bool fitTunePTransientTracks_=false;
              
};

// ------------ method called to produce the data  ------------
void
DiMuonVertexProducer::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) 
{
   
    edm::Handle<edm::View<pat::Muon>> muons;
    iEvent.getByToken(muons_, muons);
    edm::Handle<reco::BeamSpot> bspot;
    iEvent.getByToken(bspot_, bspot);  
    edm::Handle<std::vector<reco::Vertex>> pvs;
    iEvent.getByToken(pvs_, pvs);  

    edm::ESHandle<MagneticField> bFieldHandle;
    iSetup.get<IdealMagneticFieldRecord>().get(bFieldHandle);
     
    std::unique_ptr<pat::CompositeCandidateCollection> pairs(new pat::CompositeCandidateCollection());
    math::XYZPoint pv = (pvs->front()).position();

    // muon pair creation 
    for( edm::View<pat::Muon>::const_iterator mu= muons->begin(); mu!=muons->end(); ++mu){
      // remove mu not qualified for trailing mu
      if ( !mu2_cuts_(*mu) ) continue;

      for( edm::View<pat::Muon>::const_iterator mu2= mu+1; mu2!=muons->end(); ++mu2){
        // remove mu not qualified for trailing mu
        if ( !mu2_cuts_(*mu2) ) continue;
         // remove mu not qualified for leading mu        
        if ( !mu1_cuts_(*mu) && !mu1_cuts_(*mu2) ) continue;

        //create pair
        pat::CompositeCandidate muon_pair;
        muon_pair.setP4(mu->p4() + mu2->p4());
        muon_pair.setCharge(mu->charge() + mu2->charge());
        muon_pair.addUserFloat("deltaR", reco::deltaR(*mu, *mu2));

        // cut before vertex
        if ( !pre_vtxfit_cuts_(muon_pair) ) continue;
        reco::TransientTrack tranmu1((*(mu->bestTrack())), &(*bFieldHandle));
        reco::TransientTrack tranmu2((*(mu2->bestTrack())), &(*bFieldHandle));

        if(fitTunePTransientTracks_){
          tranmu1=reco::TransientTrack((*(mu->tunePMuonBestTrack() )), &(*bFieldHandle));
          tranmu2=reco::TransientTrack((*(mu2->tunePMuonBestTrack() )), &(*bFieldHandle));
        }

        //fit
        TransientTrackCollection mutrk{ tranmu1, tranmu2};
        SecondaryVertexFitter vtx(mutrk,{MUON_MASS,MUON_MASS},refit_);

        // remove failures
        if ( !vtx.success() ) continue;

        //pair after fit
        muon_pair.addUserFloat("fit_pt",vtx.motherP4().pt());
        muon_pair.addUserFloat("fit_eta",vtx.motherP4().eta());
        muon_pair.addUserFloat("fit_phi",vtx.motherP4().phi());
        muon_pair.addUserFloat("fit_mass",vtx.motherP4().mass());
        muon_pair.addUserFloat("fit_charge",vtx.motherCh());

        //vertex quality
        muon_pair.addUserFloat("chi2",vtx.chi2());
        muon_pair.addUserFloat("dof",vtx.dof());
        muon_pair.addUserFloat("prob",vtx.prob());

        //vertex position
        muon_pair.addUserFloat("vtx_x",vtx.motherXYZ().x());
        muon_pair.addUserFloat("vtx_y",vtx.motherXYZ().y());
        muon_pair.addUserFloat("vtx_z",vtx.motherXYZ().z());

        //distance variables
	GlobalPoint Dispbeamspot(
				 -1*((bspot->x0()-vtx.motherXYZ().x())+(vtx.motherXYZ().z()-bspot->z0())* bspot->dxdz()),
				 -1*((bspot->y0()-vtx.motherXYZ().y())+ (vtx.motherXYZ().z()-bspot->z0()) * bspot->dydz()), 0);

        float Lxy = Dispbeamspot.perp();  
        float eLxy= vtx.motherXYZError().rerr(Dispbeamspot); 
        eLxy = TMath::Sqrt( eLxy );

        muon_pair.addUserFloat("IP_fromBS",Lxy);
        muon_pair.addUserFloat("EIP_fromBS",eLxy);
        muon_pair.addUserFloat("SIP_fromBS",eLxy !=0 ? Lxy/eLxy : 0);
	
        GlobalPoint DispFromPV(
			        pv.x()-vtx.motherXYZ().x(),
			        pv.y()-vtx.motherXYZ().y(), 
                                0 
                               );

        float LxyPV = DispFromPV.perp();  
        float eLxyPV= vtx.motherXYZError().rerr(DispFromPV); 
        eLxyPV = TMath::Sqrt( eLxyPV );

        muon_pair.addUserFloat("IP_fromPV",LxyPV);
        muon_pair.addUserFloat("EIP_fromPV",eLxyPV);
        muon_pair.addUserFloat("SIP_fromPV",eLxyPV != 0 ? LxyPV/eLxyPV : 0);

        //daughter refited
	std::vector<unsigned> DaughterOrder{0,1};
        if (mu2->pt()>mu->pt() ){
	  DaughterOrder.clear();
      	  DaughterOrder=std::vector<unsigned>({1,0});          
        }
        int muOrder=1;
        for (unsigned i: DaughterOrder){
          muon_pair.addUserFloat("mu"+std::to_string(muOrder)+"_pt",vtx.daughterP4(i).pt());
          muon_pair.addUserFloat("mu"+std::to_string(muOrder)+"_eta",vtx.daughterP4(i).eta()); 
          muon_pair.addUserFloat("mu"+std::to_string(muOrder)+"_phi",vtx.daughterP4(i).phi());
          muOrder++;
        }

        //daughter idx
        if (mu->pt()>mu2->pt() ){
          muon_pair.addUserInt("mu1_idx",mu-muons->begin());
          muon_pair.addUserInt("mu2_idx",mu2-muons->begin());
        } else{
          muon_pair.addUserInt("mu1_idx",mu2-muons->begin());
          muon_pair.addUserInt("mu2_idx",mu-muons->begin());
        }

        // cuts after vertex
        if ( !post_vtxfit_cuts_(muon_pair) ) continue;
        pairs->emplace_back(muon_pair);

      }
    }
      
    iEvent.put(std::move(pairs),"diMuons");
}


//define this as a plug-in
DEFINE_FWK_MODULE(DiMuonVertexProducer);
