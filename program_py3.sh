#!/bin/bash

#SBATCH --job-name=ExtractPhoton  ### Job Name
#SBATCH --output=logExtractPhoton.out
#SBATCH --partition=long
#SBATCH --time=70:00:00 ### WallTime (hh:mm:ss) format "hours:minutes:seconds"or "days-hours",
#SBATCH --ntasks=80 ### maximum is 192
#SBATCH --account=jab ### Account used for job submission

# module load prun/1.3
# module load openmpi3/3.1.3
module load anaconda/3.7
# source activate /work/jab/envCR

mpirun -np $SLURM_NTASKS python3.7 main.py