#!/bin/bash

#SBATCH -J extractPhoton # Job name 
#SBATCH --partition long
#SBATCH -o log_extractPhoton.out # Name of stdout output file (%j becomes %jobId)
#SBATCH -N 1 # Total number of nodes requested
#SBATCH -n 1 # Total number tasks per node
#SBATCH -t 72:00:00 # Run time (hh:mm:ss) - 1.0 hours

module load anaconda/2.7
source /opt/ohpc/pub/apps/anaconda2/bin/activate fermi

python main.py