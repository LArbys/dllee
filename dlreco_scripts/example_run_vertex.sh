
# EXAMPLES

# ==============================
# RUN ON MCC9-UBDL
# ==============================
# inputs
# -------
# tagger_anaout_larcv.root: UBDL-made
RECO=../LArCV/app/LArOpenCVHandle/cfg/mac/run_reco_mcc9.py 
CFG=vertex_configs/prod_fullchain_mcc9ssnet_combined_newtag_extbnb_c10_union.cfg
VERTOUT=vertexout.root
VERTANA=vertexana.root
OUTDIR=vertexoutdir

mkdir -p $OUTDIR

# w GDB (enter 'r' at prompt)
#gdb --args python $RECO $CFG $VERTANA $VERTOUT out_larcv_test.root tagger_anaout_larcv.root $OUTDIR
# w/o GDB
python $RECO $CFG $VERTANA $VERTOUT out_larcv_test.root tagger_anaout_larcv.root $OUTDIR

# ==============================
# RUN ON MIX OF dllee_unified and UBDL inputs
# ==============================
RECO=../LArCV/app/LArOpenCVHandle/cfg/mac/run_reco_unified_ubdl_mix.py
CFG=vertex_configs/prod_fullchain_unifiedubdlmix_combined_newtag_extbnb_c10_union.cfg
# set file names
SUPERA=supera_file.root
SSNET=ssnet_server_file.root
DLTAGGER=dltagger_larcv_out.root
python $RECO $CFG $VERTANA $VERTOUT $SUPERA $SSNET $DLTAGGER $OUTDIR

