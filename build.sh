#!/bin/bash

source setup.sh
source configure.sh

homedir=$PWD

cd $LARLITE_BASEDIR
make -j4 || return 1

cd $LARLITE_BASEDIR/UserDev/BasicTool
make -j4 || return 1

cd $LARLITE_BASEDIR/UserDev/RecoTool
make -j4 || return 1

cd $LARLITE_BASEDIR/UserDev/SelectionTool/OpT0Finder
make -j4 || return 1

cd $GEO2D_BASEDIR
make -j4 || return 1

cd $LAROPENCV_BASEDIR
make -j4 || return 1

cd $LARCV_BASEDIR
make -j4 || return 1

cd $LARLITECV_BASEDIR
make -j4 || return 1

cd $homedir

echo "DONE"
