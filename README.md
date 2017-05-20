# dllee

Unified Repository To Build DL LEE code in one shot

This repository contains git submodules to the various frameworks and modules the DL LEE analysis uses.

Warning: I don't know what happens when one works on submodule code. Will things get royally f-ed up?

# Dependencies

* ROOT (6 Highly recommended. 5 might work, but not really supported)
* OpenCV

## ROOT

To build ROOT follow these [instuctions](https://root.cern.ch/building-root).

But if you are logging into NuDot (MIT), Wu (Columbia), or at Fermilab, ROOT is already available. Do not install you own copy. Ask some one how to set it up.

## OpenCV

We officially support OpenCV 3.0.

Again, if logging into one of the machines listed above, OpenCV should already be available.

If installing on your laptop here are some quick instructions for a few OS we've worked on

### Ubuntu 16.10

These [instructions](http://docs.opencv.org/3.0-beta/doc/tutorials/introduction/linux_install/linux_install.html) mostly work.  For those with an NVIDIA GPU and Ubuntu 16.10, there are conflicts with gcc 5 and CUDA 8's nvcc.  Follow the instructions normally. When you get to the build stage, you might get an error about GCC versions.  Go into CMakeCache.txt and change the gcc compiler version that supports nvcc.  Rerun cmake. Then the build should work.

# Building the code

First, you need to setup two environment variables that point to the location of OpenCV libraries and headers.  Do this in setup.sh. The location that is the default is typically for Ubuntu.

Then, setup the various environment variables

    source setup.sh
    source configure.sh


Then give the build a shot. Let Taritree know if you can't get it to work.

    source build.sh


You should see

    << installing headers >>
    make[1]: Leaving directory '/home/twongjirad/working/larbys/dllee_unified/larlitecv/app/ContainedROI'
    
    Compiling TaggerCROI...
    make[1]: Entering directory '/home/twongjirad/working/larbys/dllee_unified/larlitecv/app/TaggerCROI'
    << checking dependencies>>
    << generating dict >>
    << compiling PayloadWriteMethods.cxx >>
    << compiling TaggerCROITypes.cxx >>
    << compiling TaggerCROIVPayload.cxx >>
    << compiling TaggerCROIAlgo.cxx >>
    << compiling TaggerCROIAlgoConfig.cxx >>
    << compiling TaggerCROIDict.cxx >>
    << installing headers >>
    make[1]: Leaving directory '/home/twongjirad/working/larbys/dllee_unified/larlitecv/app/TaggerCROI'

    Linking library...
    
    DONE

# Resetup the environment

Go to the folder this README is in, then

    source setup.sh
    source configure.sh

Right now, the scripts assume you are in this folder.