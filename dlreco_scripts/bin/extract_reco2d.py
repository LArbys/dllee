import os,sys
from larlite import larlite


io = larlite.storage_manager( larlite.storage_manager.kBOTH )
io.add_in_filename( sys.argv[1] )
io.set_out_filename( "extracted_larlite_reco2d.root" )
io.set_data_to_read(  larlite.data.kHit, "gaushit" )
io.set_data_to_write( larlite.data.kHit, "gaushit" )
io.open()

nentries = io.get_entries()
io.next_event()
for ientry in xrange(0,nentries):
    io.next_event()
io.close()


