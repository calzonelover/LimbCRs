#!/bin/bash

echo 'begin exposure calculation process'

cd /work/jab/LimbCRs/unit_test/exposure_map_cpp/

mpic++ main_mpi3.cpp -o limb_exposure_mpi -std=c++11
# mpirun -np 4 ./limb_exposure_mpi
mpirun -x LD_LIBRARY_PATH -machinefile /work/jab/LimbCRs/spaceMachineFile ./limb_exposure_mpi

cd /work/jab/LimbCRs