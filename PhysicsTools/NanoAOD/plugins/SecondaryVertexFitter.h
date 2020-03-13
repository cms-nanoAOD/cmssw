// -*- C++ -*-
// //
// // Package:    PhysicsTools/NanoAOD
// // Class:      SecondaryVertexFitter
// // 
//
//  Description: [one line class summary]
//
//   Implementation:
//        [Notes on implementation]
//        */
//        //
//        // Original Author:  George Karathanasis, georgios.karathanasis@cern.ch
//        //         Created:  Mon, 7 Sep 2019 09:26:39 GMT
//        //
//        //
//
//
#ifndef SECONDARYVERTEXFITTER_H
#define SECONDARYVERTEXFITTER_H


#include "MagneticField/Engine/interface/MagneticField.h"
#include "MagneticField/Records/interface/IdealMagneticFieldRecord.h"
#include "TrackingTools/TransientTrack/interface/TransientTrackBuilder.h"
#include "TrackingTools/Records/interface/TransientTrackRecord.h"
#include "RecoVertex/VertexPrimitives/interface/TransientVertex.h"
#include "RecoVertex/KalmanVertexFit/interface/KalmanVertexFitter.h"
#include "TLorentzVector.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "TrackingTools/TransientTrack/interface/TransientTrack.h"
#include "CommonTools/Statistics/interface/ChiSquaredProbability.h"
#include <vector>

class SecondaryVertexFitter{

 typedef std::vector<reco::TransientTrack> TransientTrackCollection;

 public: 

  SecondaryVertexFitter() {};
  SecondaryVertexFitter( TransientTrackCollection & ttks, const std::vector<float> &mass, bool refit_);   
  virtual ~SecondaryVertexFitter();

  bool success() { return m_success; }

  // mom properties
  math::PtEtaPhiMLorentzVector motherP4() { return SV; }  
  int motherCh() { return SVch; }

  //position
  GlobalPoint motherXYZ(){ return SecVertex.position(); }
  GlobalError motherXYZError(){ return SecVertex.positionError(); }

  // vertex quality
  float chi2() { return m_success ? SecVertex.totalChiSquared() : 999; }
  float dof() { return m_success ? SecVertex.degreesOfFreedom() : -1; }
  float prob() { return m_success ? ChiSquaredProbability(chi2(), dof()) : 0; }

  // daughter properties
  math::PtEtaPhiMLorentzVector daughterP4(unsigned int idaughter);
  int daughterCh(unsigned int idaughter);
 
  
  

 private:
  bool m_success; 
  TransientVertex SecVertex;
  int SVch=0;
  TransientTrackCollection KFrefitted;
  std::vector<float> mass;
  math::PtEtaPhiMLorentzVector SV;

};
#endif
