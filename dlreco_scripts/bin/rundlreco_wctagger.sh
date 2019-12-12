#!/bin/bash

echo "<<<<<< RUN DL RECO SCRIPT w/ use WC Tagger on dlmerged >>>>>>"

INPUT_DLMERGED=$1

echo "INPUT FILE (expecting dlmerged file): $INPUT_DLMERGED"

# SETUP ENV FOR WC TAGGER BIN
export PATH=$LARCV_BASEDIR/app/WC_Tagger:$PATH

echo "<<< CHECK ENV AFTER DLLEE_UNIFIED >>>"
export 

# DIRS
NUEID_INTER_DIR=${LARLITECV_BASEDIR}/app/LLCVProcessor/InterTool/Sel/NueID/mac/ # using ups
SHOWER_MAC_DIR=${LARLITECV_BASEDIR}/app/LLCVProcessor/DLHandshake/mac/ # using ups

# CONFIGS
# -------
VERTEX_CONFIG=$DLLEE_UNIFIED_BASEDIR/dlreco_scripts/vertex_configs/prod_fullchain_mcc9ssnet_wctagger_nosecondshower.cfg
TRACKER_CONFIG=$DLLEE_UNIFIED_BASEDIR/dlreco_scripts/tracker_configs/tracker_read_cosmo_tickbackwards.cfg
NUEID_INTER_CONFIG=${NUEID_INTER_DIR}/inter_nue_data_mcc9.cfg
SHOWER_RECO_CONFIG=$SHOWER_MAC_DIR/config_nueid.cfg
SHOWER_RECO_DQDS=$SHOWER_MAC_DIR/dqds_mc_xyz.txt

# LARLITE FILES TO MERGE
# -----------------------
LARLITE_FILE_LIST="nueid_ll_out_0.root shower_reco_out_0.root extracted_larlite_reco2d.root tracker_reco.root"

echo "<<< CONFIGS >>>"
echo "VERTEX:  ${VERTEX_CONFIG}"
echo "TRACKER: ${TRACKER_CONFIG}"
echo "NUEID:   ${NUEID_INTER_CONFIG}"
echo "SHOWER-CFG:  ${SHOWER_RECO_CONFIG}"
echo "SHOWER-DQDS: ${SHOWER_RECO_DQDS}"
echo ""

echo "LARLITE FILES: ${LARLITE_FILE_LIST}"
echo ""

echo "<<< CHECK ENV AFTER DLLEE_UNIFIED >>>"
export 

echo "<<< PRIMARY CHAIN >>>"
echo "< RUN WC TAGGER >"
ls $INPUT_DLMERGED > input_larcv.txt
$LARCV_BASEDIR/app/WC_Tagger/./thrumu_maker input_larcv.txt
TAGGER_LARCV=thrumu_outfile.root

echo "<<< RUN VERTEXER >>>"
#python $DLLEE_UNIFIED_BASEDIR/dlreco_scripts/bin/run_vertexer.py -c $VERTEX_CONFIG -a vertexana.root -o vertexout.root -d ./ $INPUT_DLMERGED $TAGGER_LARCV
VERTEXOUT=vertexout.root
VERTEXANA=vertexana.root

echo "<<< RUN TRACKER >>>"
python $DLLEE_UNIFIED_BASEDIR/dlreco_scripts/bin/run_tracker_reco3d.py -c $TRACKER_CONFIG -i $VERTEXOUT -t $TAGGER_LARCV -p $VERTEXOUT -d ./ 
TRACKEROUT=tracker_reco.root
TRACKERANA=tracker_anaout.root
mv -f tracker_reco_0.root $TRACKEROUT
mv -f tracker_anaout_0.root  $TRACKERANA

echo "<<< EXTRACT RECO2D >>>"
RECO2D=extracted_larlite_reco2d.root
python extract_reco2d.py $INPUT_DLMERGED $RECO2D

echo "<<< RUN SHOWER RECO >>>"
echo "  < make inter file > "
echo "python ${NUEID_INTER_DIR}/inter_ana_nue_server.py -c ${NUEID_INTER_CONFIG} -mc -d -id 0 -od ./ -re larlite_reco2d.root vertexout.root"
python ${NUEID_INTER_DIR}/inter_ana_nue_server.py -c ${NUEID_INTER_CONFIG} -mc -d -id 0 -od ./ -re $RECO2D vertexout.root

echo "  < shower file >"
python ${SHOWER_MAC_DIR}/reco_recluster_shower.py -c $SHOWER_RECO_CONFIG -mc -id 0 -od ./ --reco2d $RECO2D -dqds $SHOWER_RECO_DQDS nueid_lcv_out_0.root

echo "<< combine larlite files >>"
python $DLLEE_UNIFIED_BASEDIR/dlreco_scripts/bin/combine_larlite.py -o larlite_dlmerged.root $LARLITE_FILE_LIST
echo "<<< HADD ROOT FILES >>>"
hadd -f merged_dlreco.root $VERTEXOUT $VERTEXANA $TRACKERANA nueid_lcv_out_0.root larlite_dlmerged.root
#echo "<<< Append UBDL Products >>>"
#python $DLLEE_UNIFIED_BASEDIR/dlreco_scripts/bin/append_ubdlproducts.py merged_dlreco.root out_larcv_test.root

echo "<<< cleanup excess root files >>>"
