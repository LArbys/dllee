#!/bin/bash

set -e

# setup environment variables
source setup.sh

# setup larlite
source larlite/config/setup.sh

# setup laropencv
source LArOpenCV/setup_laropencv.sh

# setup Geo2D
source Geo2D/config/setup.sh

# setup LArCV
source LArCV/configure.sh

# setup larlitecv
source larlitecv/configure.sh

