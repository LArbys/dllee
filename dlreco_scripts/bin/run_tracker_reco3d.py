#!/bin/env python
import os,sys

import argparse
parser = argparse.ArgumentParser(description="Run DL LEE Vertexer")
parser.add_argument('-c','--config',required=True,type=str,help="configuration file")
parser.add_argument('-i','--supera',required=False,type=str,default=None,help="Input supera file  (LARCV): has ADC image")
parser.add_argument('-t','--tagger',required=False,type=str,default=None,help="Input tagger file  (LARCV): has tagger info")
parser.add_argument('-p','--pgraph',required=True,type=str,default=None,help="Input vertexer file (LARCV): has particle graph and vertex info")
parser.add_argument('-sp','--spline-path',default=None,type=str,help="Path to dE/dx spline file.")
parser.add_argument('-d','--outdir',default="./",type=str,help="Output directory")

args = parser.parse_args(sys.argv[1:])

import ROOT, sys
from ROOT import std
from larcv import larcv

ROOT.gROOT.SetBatch(True)

CONFIG_FILE = args.config
IMG_FILE    = args.supera
TAGGER_FILE = args.tagger
PGRAPH_FILE = args.pgraph
OUTPUT_DIR  = args.outdir

os.system("mkdir -p %s"%(OUTPUT_DIR))

try:
    num = int(os.path.basename(PGRAPH_FILE).split(".")[0].split("_")[-1])
except:
    num = 0

#BASE_PATH = os.path.realpath(__file__)
#BASE_PATH = os.path.dirname(BASE_PATH)
BASE_PATH = os.environ["LARCV_BASEDIR"]+"/app/Reco3D/bin/"
sys.path.insert(0,BASE_PATH)

proc = larcv.ProcessDriver('ProcessDriver')

proc.configure(CONFIG_FILE)
flist=ROOT.std.vector('std::string')()
flist.push_back(ROOT.std.string(PGRAPH_FILE))
if args.supera is not None:
    flist.push_back(ROOT.std.string(IMG_FILE))
if args.tagger is not None:
    flist.push_back(ROOT.std.string(TAGGER_FILE))
proc.override_input_file(flist)

proc.override_ana_file(ROOT.std.string(os.path.join(OUTPUT_DIR,"tracker_anaout_%d.root" % num)))

alg_id = proc.process_id("Run3DTracker")
alg    = proc.process_ptr(alg_id)
print "GOT: ",alg,"@ id=",alg_id

SPLINE_PATH = os.path.join(BASE_PATH,"..","Proton_Muon_Range_dEdx_LAr_TSplines.root")
alg.SetSplineLocation(SPLINE_PATH)
alg.SetOutDir(OUTPUT_DIR)
alg.SetLLOutName(ROOT.std.string(os.path.join(OUTPUT_DIR,"tracker_reco_%d.root" % num)))

proc.initialize()
proc.batch_process()
proc.finalize()
