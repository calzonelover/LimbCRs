#!/bin/bash

#SBATCH --job-name=ExtractPhoton  ### Job Name
###SBATCH --partition=long
#SBATCH --output=logExtractPhoton.out
#SBATCH --time=24:00:00 ### WallTime (hh:mm:ss) format "hours:minutes:seconds"or "days-hours",
#SBATCH --ntasks=148
#SBATCH --account=jab ### Account used for job submission

module load prun/1.3
module load openmpi3/3.1.3
module load anaconda/3.7
source activate /work/jab/envCR

mpirun -np $SLURM_NTASKS python main_mpi.py
