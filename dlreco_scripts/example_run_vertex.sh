#!/bin/bash
# EXAMPLES

# COMMON OUTPUTS
VERTOUT=vertexout.root
VERTANA=vertexana.root
OUTDIR=vertexoutdir
mkdir -p $OUTDIR

# ==============================
# RUN IN OLD CONFIGURATION
# ==============================
# inputs
# -------
# tagger_anaout_larcv.root: UBDL-made
RECO=../LArCV/app/LArOpenCVHandle/cfg/mac/run_reco_server.py 
#CFG=vertex_configs/prod_fullchain_ssnet_combined_newtag_extbnb_c10_union_server.cfg
CFG=vertex_configs/prod_fullchain_ssnet_combined_newtag_extbnb_c10_union_server_alltrack.cfg
SUPERA=supera-Run004999-SubRun000006.root
SSNET=ssnetserveroutv2-larcv-Run004999-SubRun000006.root
OLDTAGGER=taggeroutv2-larcv-Run004999-SubRun000006.root
VERTOUT=vertexout_oldtagger_alltracks.root
VERTANA=vertexana_oldtagger_alltracks.root
#CMD="python $RECO $CFG $VERTANA $VERTOUT $SUPERA $SSNET $OLDTAGGER $OUTDIR"

# ==============================
# RUN ON MCC9-UBDL
# ==============================
# inputs
# -------
# tagger_anaout_larcv.root: UBDL-made
RECO=../LArCV/app/LArOpenCVHandle/cfg/mac/run_reco_mcc9.py 
CFG=vertex_configs/prod_fullchain_mcc9ssnet_combined_newtag_extbnb_c10_union.cfg

# w GDB (enter 'r' at prompt)
#gdb --args python $RECO $CFG $VERTANA $VERTOUT out_larcv_test.root tagger_anaout_larcv.root $OUTDIR
# w/o GDB
#python $RECO $CFG $VERTANA $VERTOUT out_larcv_test.root tagger_anaout_larcv.root $OUTDIR

# ==============================
# RUN ON MIX OF dllee_unified and UBDL inputs
# ==============================
RECO=../LArCV/app/LArOpenCVHandle/cfg/mac/run_reco_unified_ubdl_mix.py
CFG=vertex_configs/prod_fullchain_unifiedubdlmix_combined_newtag_extbnb_c10_union.cfg
#CFG=vertex_configs/prod_fullchain_unifiedubdlmix_combined_newtag_extbnb_c10_union_alltrack.cfg
# set file names
SSNET=ssnetserveroutv2-larcv-Run004999-SubRun000006.root
DLTAGGER=dltagger-larcv-mcc9_v13_nueintrinsics_overlay_run1-Run004999-SubRun000006.root
VERTOUT=vertexout_dltagger_ssnet.root
VERTANA=vertexana_dltagger_ssnet.root
CMD="python $RECO $CFG $VERTANA $VERTOUT $SSNET $DLTAGGER $OUTDIR"

# ============
# RUN COMMAND
# ============
echo "$CMD"
$CMD


