#include "SecondaryVertexFitter.h"


SecondaryVertexFitter::SecondaryVertexFitter( TransientTrackCollection & ttks_, const std::vector<float> &mass_, bool refit_){
  mass = mass_;
  //create vertex
  KalmanVertexFitter vtxFitter( refit_ );
  SecVertex=vtxFitter.vertex( ttks_ ); 
  if (!SecVertex.isValid() ) {m_success=false; return;}
  m_success=true;

  //refit
  if ( SecVertex.hasRefittedTracks() && refit_ )
     KFrefitted=SecVertex.refittedTracks();
  else
    KFrefitted=ttks_;  

  // create mother
  for (reco::TransientTrack & trk: KFrefitted){
    SVch+=trk.charge();
    math::PtEtaPhiMLorentzVector vtemp(trk.track().pt(),trk.track().eta(),trk.track().phi(),mass[&trk-&KFrefitted[0]]);
    SV+=vtemp;
  }
 }

SecondaryVertexFitter::~SecondaryVertexFitter() {}

math::PtEtaPhiMLorentzVector
SecondaryVertexFitter::daughterP4(unsigned int idaughter){
  return math::PtEtaPhiMLorentzVector(KFrefitted[idaughter].track().pt(),KFrefitted[idaughter].track().eta(),KFrefitted[idaughter].track().phi(),mass[idaughter]);
}

int
 SecondaryVertexFitter::daughterCh(unsigned int idaughter){
  return KFrefitted[idaughter].charge();
}

