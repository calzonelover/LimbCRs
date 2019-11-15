#!/usr/bin/env bash

#SBATCH --job-name=ExpCalcULTRA  ### Job Name
#SBATCH --output=logCalcExpMapULTRA.out
#SBATCH --time=24:00:00 ### WallTime (hh:mm:ss) format "hours:minutes:seconds"or "days-hours",
#SBATCH --ntasks=55 ### maximum is 192
#SBATCH --account=jab ### Account used for job submission

echo 'begin exposure calculation process'

module load prun/1.3
module load openmpi3/3.1.3

cd /work/jab/LimbCRs/unit_test/exposure_map_cpp/
mpirun -x LD_LIBRARY_PATH -np $SLURM_NTASKS /work/jab/LimbCRs/unit_test/exposure_map_cpp/limb_exposure_mpi
# mpirun -x LD_LIBRARY_PATH -machinefile /work/jab/LimbCRs/machinefile -np $SLURM_NTASKS /work/jab/LimbCRs/unit_test/exposure_map_cpp/limb_exposure_mpi