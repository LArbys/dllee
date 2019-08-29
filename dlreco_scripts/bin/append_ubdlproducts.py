import sys
import ROOT as rt

mergefile       = sys.argv[1]
clustermaskfile = sys.argv[2]

import ROOT as rt

fmask  = rt.TFile(clustermaskfile)
treenames = ["clustermask_mrcnn_masks_tree","sparseimg_larflow_tree","sparseimg_sparseuresnetout_tree"]
trees = {}
for t in treenames:
    trees[t] = fmask.Get(t)

fmerge = rt.TFile(mergefile,"update")
for t in treenames:
    trees[t].CloneTree().Write()

fmask.Close()
fmerge.Close()



