#ifndef METFILTERPRODUCER_H
#define METFILTERPRODUCER_H
#include <vector>
#include <string>
#include "TTree.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "DataFormats/Common/interface/TriggerResults.h"
#include "FWCore/Common/interface/TriggerNames.h"


class METFilterProducer {

    public :
        METFilterProducer();

        //void initialize( const TTree *tree );
        void initialize( const std::string &prefix, 
                         const edm::EDGetTokenT<edm::TriggerResults >&, 
                         TTree * );

        void produce(const edm::Event &iEvent );
        void endRun( ) {};


    private :

        std::string _prefix;

        edm::EDGetTokenT<edm::TriggerResults> _filterToken;


};
#endif
