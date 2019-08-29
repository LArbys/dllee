import os,sys
import argparse


inputfile = sys.argv[1]
outputfile = sys.argv[2]

if os.path.exists(outputfile):
    print "Output file already exists. Exiting to prevent inadvertent overwrite"
    sys.exit(1)

import ROOT as rt

fin  = rt.TFile(inputfile)
fout = rt.TFile(outputfile,"new")

vertexana_trees = ["NuFilterTree","MCTree","ShapeAnalysis","MatchAnalysis","SecondShowerAnalysis",
                   "VertexTree","EventVertexTree","PGraphTruthMatch"]

chains = {}
for vt in vertexana_trees:
    chains[vt] = fin.Get(vt)

for vt in vertexana_trees:
    chains[vt].CloneTree().Write("%s_VtxTrk"%(vt))

fout.Close()
