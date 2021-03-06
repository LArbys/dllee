# dllee unified

Unified Repository To Build DL LEE code in one shot

This repository contains git submodules to the various frameworks and modules the DL LEE analysis uses.

Warning: if you built the code using this repo and want to work on one of the submodules, 
remember to check if you are on a DETACHED HEAD state before making modifications: `git branch` to check. 
However, the `.gitmodules` file in the repo tries to not make this an issue.

# Dependencies

* ROOT 6 (ROOT 5 no longer supported)
* OpenCV (3.1 is the officially supported version -- but may work with other 3.X)

## Pre-reqs

### Ubuntu/Linux

* One can use apt-get to install the dependencies for ROOT and OpenCV 3
* ROOT and OpenCV 3 can be built by downloading the source and following instructions found online

### OS X

* One first needs to install X code on OS X
* Our group is mostly familiar with home brew to serve as the OS X package manager
* Use brew to install pre-reqs for ROOT and OpenCV 3 itself. Make sure to specify `brew install opencv3` and not just `opencv` which installs OpenCV 2. 
* If you're using OS X El Capitan or later, make sure you disable SIP (System Integrity Protection). 

## ROOT

To build ROOT follow these [instuctions](https://root.cern.ch/building-root). ROOT 6 is the currently supported (and recommended) version.

But if you are logging into NuDot (MIT), Wu (Columbia), or at Fermilab, ROOT is already available. Do not install you own copy. Ask some one how to set it up.

## OpenCV

We officially support OpenCV 3.1. (But versions on home brew seem to work OK.)

Again, if logging into one of the machines listed above, OpenCV should already be available.

If installing on your laptop here are some quick instructions for a few OS we've worked on.

For Fermilab, there is an opencv UPS product available for SL7.


# Checking out the code

First clone the repository as one would go

    git clone https://github.com/LArbys/dllee_unified

You'll get a folder with what look like folders. But there are submodule links, 
which point to a specific commit in the various repositories that make up the DL LEE code. 
To "activate" them, type the following

    git submodule init
    git submodule update

# Updating the code

This unified repository is expected to update often. To get to the latest, go the folder where this README is located and type

    git pull
    git submodule update

The second step is needed for all the submodules to go to their latest state as well.

# Building the code (generic)

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

# Building the Code Fermilab

Things are setup for SL7 only. This means working on `uboonebuild02`.

First, clone the repository somewhere. Probably in your `/uboone/app/users/` folder.
Then run:

    source build_fnal.sh

This should setup dependencies via UPS and begin the build.

# Checking in changes

If you develop using this repository, remember, the other packages like larlite, LArCV, etc. are submodules.  This can cause an issue if for some reason, the submodules when updated get put into a DETACHED HEAD. This means they are not tracking some past series of commits. The consequence is that if you go into those folders, change things, and commit it, those changes could get lost when you try to update your branch or change to another.

So when developing a submodule it might be a good idea to check if the submodule is on the right branch. Below is the list of branches used by the unified repo. (Note this is subject to change as the software develops. If you notice this is wrong, email taritree about it.)

* larlite: dlreco_tmw
* Geo2D: develop
* LArOpenCV: fmwk_update
* LArCV: develop
* larlitecv: tmw_muon_tagger

Note, the repo. has a `.gitmodule` file to solve this, but the maintainer might have messed this up.

# Resetup the environment (after build complete)

Go to the folder this README is in, then

    source setup.sh
    source configure.sh

Right now, the scripts assume you are in the same folder as this README.
