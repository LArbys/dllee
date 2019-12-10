import sys
import ROOT as rt

mergefile   = sys.argv[1]
supera_file = sys.argv[2]

import ROOT as rt

fmask  = rt.TFile(supera_file)
treenames = ["chstatus_wire_tree"]
trees = {}
for t in treenames:
    trees[t] = fmask.Get(t)

fmerge = rt.TFile(mergefile,"update")
for t in treenames:
    trees[t].CloneTree().Write()

fmask.Close()
fmerge.Close()



