#!/bin/bash

# USE THIS SCRIPT TO GO TO THE HEAD BRANCHES OF ALL THE SUBMODULES
# YOU WANT TO DO THIS FIRST BEFORE MAKING CHANGES TO SUBMODULES
# REMEMBER TO UPDATE THE dllee_unified submodule pointers AFTER CHECKING IN SUBMODULE CHANGES

homedir=$PWD
echo "Starting from $homedir"

git submodule init
git submodule update
source configure.sh

echo "LARLITE: ${LARLITE_BASEDIR}"
echo "LARLITE: ${GEO2D_BASEDIR}"
echo "LARCV: ${LARCV_BASEDIR}"
echo "LAROPENCV: ${LAROPENCV_BASEDIR}"
echo "LARLITECV: ${LARLITECV_BASEDIR}"

cd $LARLITE_BASEDIR
#git checkout tmw_cosmicdisc_flash

cd $LARLITE_BASEDIR/UserDev/SelectionTool/LEEPreCuts
git submodule init
git submodule update
cd algosrc
git checkout master

cd $GEO2D_BASEDIR
git checkout develop

cd $LAROPENCV_BASEDIR
git checkout fmwk_update

cd $LARCV_BASEDIR
git checkout develop

cd $LARLITECV_BASEDIR
git checkout tmw_muon_tagger

cd $homedir

echo "DONE"
