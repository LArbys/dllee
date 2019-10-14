#!/bin/bash

# 10-Oct-2019 WGS
# At Nevis we use environment modules to act to
# set up our environment. 

# Note that as of Oct-2019, these are the software versions
# which will work in CentOS 7. Eventually there will be more
# CentOS 7-compatible versions. 

module load cmake root/06.08.06 opencv/3.1

# Additional compilation notes:
# - Even though "module load python/2.7" is part of the
#   environment setup above, I still had to install
#   numpy and python2-numpy for numpy to import properly
#   in the build process. (This probably means that there's
#   something in these scripts that assumes the location of
#   the python site-packages directory.)
# - Half-way through the build process, somehow 
#   OPENCV_INCDIR and OPENCV_LIBDIR are reset. I had to do
#     module unload opencv
#     module load opencv
#   for the build process to continue.
