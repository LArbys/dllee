#!/bin/bash

# SPECIFY WHERE OPENCV IS
export OPENCV_LIBDIR=/usr/local/lib
export OPENCV_INCDIR=/usr/local/include

if [ ! -f $OPENCV_LIBDIR/libopencv_core.so ]; then
    echo "OPENCV LIBRARY NOT FOUND"
    return 1
fi

if [ ! -f $OPENCV_INCDIR/opencv/cv.h ]; then
    echo "OPENCV INCLUDES NOT FOUND"
    return 1
fi


