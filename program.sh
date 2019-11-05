#!/bin/bash

#SBATCH -J ft2convert # Job name 
#SBATCH -o log_ft2convert.out # Name of stdout output file (%j becomes %jobId)
#SBATCH -N 1 # Total number of nodes requested
#SBATCH -n 1 # Total number tasks per node
#SBATCH -t 24:00:00 # Run time (hh:mm:ss) - 1.0 hours

module load anaconda/3.7

python main.py