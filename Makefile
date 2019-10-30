compile:
	mpic++ unit_test/exposure_map_cpp/main_mpi3.cpp -o unit_test/exposure_map_cpp/limb_exposure_mpi -std=c++11

sync:
	rsync -avu ../LimbCRs/ jab@newgalaxy:/work/jab/LimbCRs

compile_and_sync: compile sync

clean:
	rm data/exposure_map/P8R2_SOURCE_V6/*
	rm data/exposure_map/P8R2_ULTRACLEANVETO_V6/*
