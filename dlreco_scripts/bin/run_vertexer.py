#!/bin/env python
import os, sys

#BASE_PATH = os.path.realpath(__file__)
#BASE_PATH = os.path.dirname(BASE_PATH)
#sys.path.insert(0,BASE_PATH)

import argparse
parser = argparse.ArgumentParser(description="Run DL LEE Vertexer")
parser.add_argument('-c','--config',required=True,type=str,help="configuration file")
parser.add_argument('-a','--anaout',required=True,type=str,help="Output Ana file")
parser.add_argument('-o','--output',required=True,type=str,help="Output LArCV file")
parser.add_argument('-d','--outdir',default="./",type=str,help="Output directory")
parser.add_argument('input_larcv',type=str,nargs='+',help="Input LArCV files. Some combination of files must have: ADC image, tagger image, CROI, SSNet info")

args = parser.parse_args(sys.argv[1:])

from larcv import larcv
import ROOT
from ROOT import std

proc = larcv.ProcessDriver('ProcessDriver')

# configuration
proc.configure(args.config)

# input larcv files
flist=ROOT.std.vector('std::string')()
for f in args.input_larcv:
    flist.push_back(f)
proc.override_input_file(flist)

# output ana file
proc.override_ana_file(os.path.join(args.outdir,args.anaout))

# larcv output
proc.override_output_file(os.path.join(args.outdir,args.output))

# intialize
proc.initialize()

# start process
proc.batch_process()

# save and close
proc.finalize()


