Scripts to Run the Different Components

Steps in the primary reco chain
* Tagger
* SSNet
* Vertexer
* Likelihood variables
* MPID


Steps in the DL-Tagger development chain
* DLTagger
* SSNet
* Vertexer
* Likelihood variables
* MPID

## Tagger

Inputs

* larcv file containing
⋅⋅* `wire`: ADC wholeview images
⋅⋅* `wire`: Channel status images
* larlite opreco file
⋅⋅* `SimpleFlashBeam`:  opflashes in the beam window (for CROI)
⋅⋅* `opHitBeam`: ophits in the beam window (for Precuts)

# To run

* List input files in an input list

      ls out_larcv_test.root > input_larcv.txt
      ls larlite_opreco.root > input_larlite.txt

* Run tagger

      run_tagger [config script]


The default configuration script uses `input_larcv.txt` and `input_larlite.txt` as the input files.

Configufation script to use depends on the file type (because the BNB window is different for each).
Scripts can be found in `tagger_scripts` in this folder.

| File type    | configuration script |
| ------------ | -------------------- |
| BNB          | tagger_bnbdata_v2_splity_mcc9.cfg |
| MC Overlay   | tagger_overlay_v2_splity_mcc9.cfg |
| MC corsika   | tagger_mcv2_splity.cfg |
| EXT-BNB      | tagger_extbnb_v2_splity_mcc9.cfg |
| EXT-unbiased | tagger_extbnb_v2_splity_mcc9.cfg |

### Notes

You might have to change where the photon library file is in the file.

## SSNet (MCC9 SparseConvNet)

This should have been made as a part of production.
To run it as a separate process, you will need to use the `UBDL` repository.

## SSNet (MCC8 caffe network)

TBD

## Vertexer

There is a python helper script and vertxer configuration files in the `dlreco_scripts` folder of the `dllee_unified` repository.

```
python $DLLEE_UNIFIED_BASEDIR/dlreco_scripts/bin/run_vertexer.py -c $VERTEX_CONFIG -a vertexana.root -o vertexout.root -d ./ $SUPERA $TAGGER
```

where `$DLLEE_UNIFIED_BASEDIR` is the location of your dllee_unified repository. 
This environment variable is setup for you when you run the `configure.sh` script found in the top-level folder of the repo.
`$VERTEX_CONFIG` is the vertex configuration file (see the table in the next section for which to run).  
`$SUPERA` is the `larcv` file with the ADC image (usually the `wire` tree).
`$TAGGER` is the output of the tagger file (DL or Baseline versions).

### Config files to use

The configuration one uses for the vertexer depends on the input 

| Config description            | Input supera  | Input tagger | other |  config file   |
| ----------------------------- | ------------- | ------------ | ----- | -----------    |
| Baseline/MCC8 developed tools | dllee_unified | old tagger   |  N/A  | prod_fullchain_ssnet_combined_newtag_extbnb_c10_union_server.cfg |
| Run on FNAL                   | ubdl          | old tagger   |  N/A  | prod_fullchain_mcc9ssnet_combined_newtag_extbnb_c10_union.cfg |
