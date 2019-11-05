#ifndef GENPARTICLEPRODUCER_H
#define GENPARTICLEPRODUCER_H
#include <vector>
#include <set>
#include <string>
#include "TTree.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/JetReco/interface/GenJet.h"
#include "DataFormats/PatCandidates/interface/MET.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"


class GenParticleProducer {

    public :
        GenParticleProducer();

        //void initialize( const TTree *tree );
        void initialize( const std::string &prefix, 
                         const edm::EDGetTokenT<std::vector<reco::GenParticle> >&genTok, 
                         const edm::EDGetTokenT<std::vector<reco::GenJet> >&genDressedLeptonTok,
                         const edm::EDGetTokenT<std::vector<reco::MET> >&genMetTok,
                         TTree *tree, float minPt =1, std::vector<int> genVIP = {});

        void produce(const edm::Event &iEvent );


    private :

        std::string _prefix;

        int gen_n;

        std::vector<float> *gen_pt;
        std::vector<float> *gen_eta;
        std::vector<float> *gen_phi;
        std::vector<float> *gen_e;
        std::vector<int> *gen_PID;
        std::vector<int> *gen_status;
        std::vector<int> *gen_motherPID;
        std::vector<Bool_t> *gen_isPromptFinalState;
        std::vector<Bool_t> *gen_fromHardProcessFinalState;
        std::vector<Bool_t> *gen_fromHardProcessBeforeFSR;

        edm::EDGetTokenT<std::vector<reco::GenParticle> > _genPartToken;
        
        int gen_dl_n;
        std::vector<float> *gen_dl_pt;
        std::vector<float> *gen_dl_eta;
        std::vector<float> *gen_dl_phi;
        std::vector<float> *gen_dl_e;
        std::vector<int>   *gen_dl_PID;
        
        edm::EDGetTokenT<std::vector<reco::GenJet> > _genDressedLeptonToken;
        
        float gen_met_pt;
        float gen_met_phi;
        
        edm::EDGetTokenT<std::vector<reco::MET> > _genMetToken;

        float _minPt;
        std::set<int> _genVIP;

};
#endif
