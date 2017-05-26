#!/bin/bash

# SPECIFY WHERE OPENCV IS
export OPENCV_LIBDIR=/usr/local/lib
export OPENCV_INCDIR=/usr/local/include

suffix=so
if [[ `uname` == 'Darwin' ]]; then
    suffix=dylib
fi

if [ ! -f $OPENCV_LIBDIR/libopencv_core.${suffix} ]; then
    echo "OPENCV LIBRARY NOT FOUND. Set env variable OPENCV_LIBDIR to where libopencv_core.${suffix} lives"
    return 1
fi

if [ ! -f $OPENCV_INCDIR/opencv/cv.h ]; then
    echo "OPENCV INCLUDES NOT FOUND. Please set env variable OPENCV_INCDIR to where opencv/cv.h lives"
    return 1
fi


