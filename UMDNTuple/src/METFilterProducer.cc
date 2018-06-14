#include <bitset>
#include <sstream>
#include <iostream>
#include "UMDNTuple/UMDNTuple/interface/METFilterProducer.h"
#include "FWCore/Framework/interface/Event.h"

METFilterProducer::METFilterProducer(  ) 
{

}

void METFilterProducer::initialize( const std::string &prefix,
            const edm::EDGetTokenT<edm::TriggerResults>& trigTok,
            TTree *tree) {

    _prefix = prefix;
    _filterToken = trigTok;

    //tree->Branch("passedTriggers", &_passing_triggers );

}


void METFilterProducer::produce(const edm::Event &iEvent ) {

    edm::Handle<edm::TriggerResults> filters;
    iEvent.getByToken(_filterToken,filters);

    if( !filters.isValid() || filters.failedToGet() ) {
        std::cout << "could not get filter results.  Will not set filters!" << std::endl;
        return;
    }

    //_passing_triggers->clear();

    const edm::TriggerNames filtNames( iEvent.triggerNames( *filters ) );

    for (unsigned i = 0; i < filtNames.size(); i++) {
      std::string trigname = filtNames.triggerName(i);
      std::cout << trigname << std::endl;
    }
    //if( _trigger_idx_map.size() == 0 ) {

    //    for (unsigned i = 0; i < trigNames.size(); i++) {

    //        std::string trigname = trigNames.triggerName(i);

    //        std::string::size_type version_pos = trigname.find_last_of("_");

    //        std::string trigname_mod = trigname.substr( 0, version_pos );

    //        std::map<std::string, int>::const_iterator mitr = _trigger_map.find(trigname_mod);

    //        if( mitr != _trigger_map.end() ) {
    //            _trigger_idx_map.push_back( std::make_pair(i, mitr->second) );
    //        }
    //    }
    //}

    //for( std::vector<std::pair<int,int> >::const_iterator mitr = _trigger_idx_map.begin();
    //        mitr != _trigger_idx_map.end(); ++mitr ) {
    //    if( triggers->accept( mitr->first ) ) {
    //        _passing_triggers->push_back( mitr->second );
    //    }
    //}

}

