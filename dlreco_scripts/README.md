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
| BNB          | tagger_data_v2_splity.cfg |
| MC Overlay   | tagger_overlay_v2_splity.cfg |
| MC corsika   | tagger_mcv2_splity.cfg |
| EXT-BNB      | tagger_extbnb_v2_splity.cfg   (missing) |
| EXT-unbiased | tagger_unbiased_v2_splity.cfg (missing) |

### Notes

You might have to change where the photon library file is in the file.

## SSNet (MCC9 SparseConvNet)

This should have been made as a part of production.
To run it as a separate process, you will need to use the `UBDL` repository.

## SSNet (MCC8 caffe network)

TBD

## Vertexer

