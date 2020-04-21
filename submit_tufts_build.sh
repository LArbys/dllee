#!/bin/bash

#SBATCH --job-name=build_dlu_v1_0_5
#SBATCH --output=dlunified_build.log
#SBATCH --ntasks=1
#SBATCH --mem-per-cpu=4000
#SBATCH --time=30:00
#SBATCH --cpus-per-task=4

module load singularity

UNIFIED_DIR=/cluster/tufts/wongjiradlab/twongj01/production/dllee_unified_v1_0_5/
ROOT_DIR=/usr/local/root/root-6.16.00/
#CONTAINER=/cluster/tufts/wongjiradlab/larbys/larbys-containers/singularity_ubdl_deps_py2_10022019.simg
CONTAINER=/cluster/tufts/wongjiradlab/larbys/larbys-containers/singularity_dldependencies_pytorch1.3.sing

#singularity exec $CONTAINER bash -c "source $ROOT_DIR/bin/thisroot.sh && cd $UNIFIED_DIR && source setup.sh && source configure.sh && source clean.sh && source build.sh"
singularity exec $CONTAINER bash -c "source $ROOT_DIR/bin/thisroot.sh && cd $UNIFIED_DIR && source setup.sh && source configure.sh && source build.sh"
