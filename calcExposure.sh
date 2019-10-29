#!/bin/bash
#SBATCH --job-name=JabExp  ### Job Name
#SBATCH --time=01:00:00 ### WallTime (hh:mm:ss) - 1.0 hours
#SBATCH --ntasks=192 ### maximum is 192
#SBATCH --account=jab ### Account used for job submission

echo 'begin exposure calculation process'

module load intel/17
module load openmpi
module load mkl

cd /work/jab/LimbCRs/unit_test/exposure_map_cpp/
mpic++ /work/jab/LimbCRs/unit_test/exposure_map_cpp/main_mpi3.cpp -o /work/jab/LimbCRs/unit_test/exposure_map_cpp/limb_exposure_mpi -std=c++11
# mpirun -np 4 ./limb_exposure_mpi
# srun --mpi=pmix_v2 -n 4 /work/jab/LimbCRs/unit_test/exposure_map_cpp/limb_exposure_mpi
mpirun -np $SLURM_NTASKS /work/jab/LimbCRs/unit_test/exposure_map_cpp/limb_exposure_mpi