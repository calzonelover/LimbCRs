#!/bin/bash

#SBATCH -J montecarlo # Job name 
#SBATCH --partition long
#SBATCH -o montecarlo_%j.out # Name of stdout output file (%j becomes %jobId)
#SBATCH -N 1 # Total number of nodes requested
#SBATCH -t 72:00:00 # Run time (hh:mm:ss) - 1.0 hours

module load anaconda/2.7
source /opt/ohpc/pub/apps/anaconda2/bin/activate fermi

python main.py