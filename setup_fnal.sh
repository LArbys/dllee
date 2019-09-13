#!/bin/bash

# SETUP dependencies through UPS
source /cvmfs/uboone.opensciencegrid.org/products/setup_uboone.sh
setup root v6_12_06a -q e17:prof
setup python v2_7_14b
setup numpy v1_14_3 -q e17:p2714b:openblas:prof
setup opencv v3_1_0_nogui -q e17

# SPECIFY WHERE OPENCV IS
export OPENCV_LIBDIR=${OPENCV_LIB}
export OPENCV_INCDIR=${OPENCV_INC}

# uncomment this if you want to include headers using #include "larcv/PackageName/Header.h"
#export LARCV_PREFIX_INCDIR=1

suffix=so
if [[ `uname` == 'Darwin' ]]; then
    suffix=dylib
    # setting opencv paths to use location used by homebrew.
    # change this here, if you used another location
    export OPENCV_LIBDIR=/usr/local/opt/opencv3/lib
    export OPENCV_INCDIR=/usr/local/opt/opencv3/include    
fi

if [ ! -f $OPENCV_LIBDIR/libopencv_core.${suffix} ]; then
    echo "OPENCV LIBRARY NOT FOUND. Set env variable OPENCV_LIBDIR to where libopencv_core.${suffix} lives"
    return 1
fi

if [ ! -f $OPENCV_INCDIR/opencv/cv.h ]; then
    echo "OPENCV INCLUDES NOT FOUND. Please set env variable OPENCV_INCDIR to where opencv/cv.h lives"
    return 1
fi


