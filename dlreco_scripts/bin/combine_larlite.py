import os,sys
import argparse

parser = argparse.ArgumentParser(description="Combine LARLITE rootfiles")
parser.add_argument("filelist",type=str,nargs='+')
parser.add_argument("-o","--output",required=True,type=str)

args = parser.parse_args(sys.argv[1:])

import ROOT
from larlite import larlite

io = larlite.storage_manager(larlite.storage_manager.kBOTH)
for f in args.filelist:
    io.add_in_filename( f )
print "output file: ",args.output
io.set_out_filename( args.output )
io.open()

nentries = io.get_entries()
for ientry in xrange(nentries):
    io.go_to(ientry)

io.close()
