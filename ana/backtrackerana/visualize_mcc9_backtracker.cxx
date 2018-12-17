#include <iostream>

// larlite
#include "DataFormat/storage_manager.h"
#include "DataFormat/opflash.h"
#include "DataFormat/mctrack.h"
#include "DataFormat/mcshower.h"
#include "DataFormat/mcpart.h"
#include "DataFormat/hit.h"
#include "DataFormat/event_ass.h"

// larcv
#include "DataFormat/IOManager.h"
#include "DataFormat/EventImage2D.h"

// purpose of this ana-script is to project the backtrack information into the image
// and study how good (poor) the coverage is.
// is it good enough for
//  (1) truth studies?
//  (2) label making?

int main( int nargs, char** argv ) {

  larcv::IOManager io_larcv( larcv::IOManager::kREAD );
  io_larcv.add_in_file( "../../testdata/mcc9tag2_bnbintrinsic/larcv_wholeview_87c5e418-88ea-42e9-9b10-e068aa031bca.root" );
  io_larcv.initialize();

  larlite::storage_manager io_larlite( larlite::storage_manager::kREAD );
  io_larlite.add_in_filename( "../../testdata/mcc9tag2_bnbintrinsic/larlite_backtracker_befe6cc3-82f6-4360-a140-92cc3d3ca16a.root" );
  io_larlite.add_in_filename( "../../testdata/mcc9tag2_bnbintrinsic/larlite_opreco_6b8fbfef-e150-463f-9342-f9cc18568f1c.root" );
  io_larlite.open();

  larcv::IOManager io_out( larcv::IOManager::kWRITE );
  io_out.set_out_file( "output_backtrackerana.root" );
  io_out.initialize();

  // EVENT LOOP

  size_t nentries = io_larcv.get_n_entries();

  for ( size_t ientry=0; ientry<nentries; ientry++ ) {

    std::cout << "----------------------" << std::endl;
    std::cout << "[entry " << ientry << "]" << std::endl;
    
    io_larcv.read_entry( ientry );
    io_larlite.go_to( ientry );

    // larcv
    auto ev_img = (larcv::EventImage2D*)io_larcv.get_data( larcv::kProductImage2D, "wire" );
    auto const& img_v = ev_img->Image2DArray();

    // larlite
    auto ev_hits     = (larlite::event_hit*)     io_larlite.get_data( larlite::data::kHit,         "gaushit" );
    auto ev_opflash  = (larlite::event_opflash*) io_larlite.get_data( larlite::data::kOpFlash,     "simpleFlashBeam" );
    auto ev_mctrack  = (larlite::event_mctrack*) io_larlite.get_data( larlite::data::kMCTrack,     "mcreco" );
    auto ev_mcshower = (larlite::event_mcshower*)io_larlite.get_data( larlite::data::kMCShower,    "mcreco" );
    auto ev_mcpart   = (larlite::event_mcpart*)  io_larlite.get_data( larlite::data::kMCParticle,  "largeant" );    
    auto ev_backtrak = (larlite::event_ass*)     io_larlite.get_data( larlite::data::kAssociation, "gaushitTruthMatch" );

    //larlite::AssID_t hit2track_id  = ev_backtrak->find_one_assid( larlite::data::kHit, larlite::data::kMCTrack );
    //larlite::AssID_t hit2shower_id = ev_backtrak->find_one_assid( larlite::data::kHit, larlite::data::kMCShower );
    larlite::AssID_t hit2mcpart_id = ev_backtrak->find_one_assid( larlite::data::kHit, larlite::data::kMCParticle );
    std::cout << "event_mcpart: " << ev_mcpart->size() << std::endl;
    
    // if ( hit2track_id == larlite::kINVALID_ASS ) {
    //   std::cout << "found valid hit->mctrack association" << std::endl;
    // }
    // if ( hit2shower_id == larlite::kINVALID_ASS ) {
    //   std::cout << "found valid hit->mcshower association" << std::endl;
    // }
    if ( hit2mcpart_id != larlite::kINVALID_ASS ) {
      std::cout << "found valid hit->mcparticle association" << std::endl;
    }

    const larlite::AssSet_t& hit2part_ass = ev_backtrak->association( hit2mcpart_id );

    
    // debug to dump out assignment
    // for ( auto const& asspair : ev_backtrak->association_keys() ) {
    //   std::cout << "[ass] " << asspair.first.second << " -> " << asspair.second.second << std::endl;
    // }

    for ( auto const& flash : *ev_opflash ) {
      std::cout << " beam flash: " << flash.TotalPE() << std::endl;
    }

    auto evout_img      = (larcv::EventImage2D*)io_out.get_data( larcv::kProductImage2D, "wire" ); // backtracker ancestor id    
    auto evout_ancestor = (larcv::EventImage2D*)io_out.get_data( larcv::kProductImage2D, "btancestor" ); // backtracker ancestor id
    std::vector< larcv::Image2D > ancestor_v;
    auto evout_instance = (larcv::EventImage2D*)io_out.get_data( larcv::kProductImage2D, "btinstance" ); // backtracker ancestor id
    std::vector< larcv::Image2D > instance_v;
    for ( auto const& img : ev_img->Image2DArray() ) {
      larcv::Image2D ancestor( img.meta() );
      ancestor.paint(0);
      ancestor_v.emplace_back( std::move(img) );

      larcv::Image2D instance( img.meta() );
      instance.paint(0);
      instance_v.emplace_back( std::move(instance) );
    }

    // collect mctrackids and trackid->ancestormap
    std::set<int>     mctrackidx_set;
    std::map<int,int> idx2ancestor_m;
    std::map<int,int> trkidx2vecidx;
    int itrk=0;
    for ( auto const& trk : *ev_mctrack ) {
      mctrackidx_set.insert( trk.TrackID() );
      idx2ancestor_m[trk.TrackID()] = trk.AncestorTrackID();
      trkidx2vecidx[trk.TrackID()] = itrk;
      itrk++;
    }
    int ishr=0;
    for ( auto const& shr : *ev_mcshower ) {
      mctrackidx_set.insert( shr.TrackID() );
      idx2ancestor_m[shr.TrackID()] = shr.AncestorTrackID();
      trkidx2vecidx[shr.TrackID()] = ishr;
      ishr++;
    }
    
    // 1) loop through hits
    // 2) label ancestor image
    // 3) go through an label pixels above threshold w/o labels with -1
    int ihitidx      = -1;
    int nhits_label  = 0;
    int nhits_hasass = 0;
    int nhits_hasid  = 0;
    for ( auto const& hit : *ev_hits ) {
      ihitidx++;
      
      int plane = (int)hit.WireID().Plane;
      auto const& meta = img_v[plane].meta();
      int wire  = (int)hit.WireID().Wire;
      int hit_start_tick = 2400+hit.StartTick();
      int hit_end_tick   = 2400+hit.EndTick();
      if ( hit_start_tick>meta.max_y() ) continue;
      if ( hit_end_tick<=meta.min_y() )    continue;

      nhits_label++;
      
      int start_row = ( hit_start_tick>meta.pos_y( meta.rows()-1 ) ) ? meta.row(hit_start_tick) : meta.rows()-1;
      int end_row   = ( hit_end_tick<meta.max_y() )   ? meta.row(hit_end_tick)   : 0;
      int col       = meta.col(wire);

      if ( end_row<start_row ) {
	int tmp = end_row;
	end_row = start_row;
	start_row = tmp;
      }

      // get mcpart idx
      const larlite::AssUnit_t& ass_part = hit2part_ass.at( ihitidx );
      if ( ass_part.size()>0 ) {
	nhits_hasass++;
	int mcpartidx = ass_part.front();
	auto it_id = mctrackidx_set.find( mcpartidx );
	bool hasid = it_id!=mctrackidx_set.end();
	// int pdg = -1;
	// if ( hasid ) pdg = ev_mctrack->at( trkidx2vecidx[mcpartidx] ).PdgCode();
	// std::cout << " hit[" << ihitidx << "] (r,c)=(" << start_row << "-" << end_row << "," << col << ") "
	// 	  << " nparts=" << ass_part.size() << " mcpartidx=" << mcpartidx << " hasid=" << hasid << " pdg=" << pdg << std::endl;
	if ( hasid ) {
	  nhits_hasid++;
	  for ( size_t row=start_row; row<=end_row; row++ )
	    instance_v[plane].set_pixel( row, col, mcpartidx );
	}
      }
    }
    std::cout << "number of hits labeled: " << nhits_label << "/" << ev_hits->size() << std::endl;
    std::cout << "number of hits w/ assoc: " << nhits_hasass << "/" << ev_hits->size() << std::endl;
    std::cout << "number of hits w/ has-id: " << nhits_hasid << "/" << ev_hits->size() << std::endl;        
    
    int nabove_thresh[3]  = {0,0,0};
    int nabove_wlabel[3] = {0,0,0};
    int npix_labeled[3]   = {0,0,0};
    float qabove_thresh[3] = {0,0,0};
    float qabove_wlabel[3] = {0,0,0};
    for ( size_t p=0; p<ev_img->Image2DArray().size(); p++ ) {
      auto const& img    = ev_img->Image2DArray()[p];
      auto const& img_id = instance_v[p];
      for ( size_t r=0; r<img.meta().rows(); r++ ) {
	for ( size_t c=0; c<img.meta().cols(); c++ ) {
	  if ( img.pixel(r,c)>10.0 ) {
	    nabove_thresh[p]++;
	    qabove_thresh[p] += img.pixel(r,c);
	    if ( img_id.pixel(r,c)>0 ) {
	      nabove_wlabel[p]++;
	      qabove_wlabel[p] += img.pixel(r,c);
	    }
	  }
	  if ( img_id.pixel(r,c)>0 ) {
	    npix_labeled[p]++;
	  }
	}
      }
      float frac_wlabel = float(nabove_wlabel[p])/float(nabove_thresh[p]);
      float frac_qlabel = float(qabove_wlabel[p])/float(qabove_thresh[p]);      
      std::cout << "plane[" << p << "] "
		<< " abovethresh=" << nabove_thresh[p] << " w/label=" << nabove_wlabel[p] << " pix-frac=" << frac_wlabel
		<< " q-above=" << qabove_thresh[p] << " q-w/-label=" << qabove_wlabel[p] << " q-frac=" << frac_qlabel
		<< " npix_labeled=" << npix_labeled[p] << std::endl;
    }
    //   auto const& img = ev_img->Image2DArray()[p];
    //   auto& ancestor  = ancestor_v[p];
    evout_instance->Emplace( std::move(instance_v) );
    for ( auto const& img : img_v ) 
      evout_img->Append( img );

    io_out.set_id( io_larcv.event_id().run(), io_larcv.event_id().subrun(), io_larcv.event_id().event() );
    io_out.save_entry();
  }

  
  io_out.finalize();

  
  return 0;
}
