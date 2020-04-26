LIBDIR := utility/cpp

# g++ unit_test/flx_map/flxmap.cpp $(LIBDIR)/*.cpp -o program `root-config --cflags --glibs` -std=c++11
# g++ unit_test/flx_map/readexpmap.cpp $(LIBDIR)/*.cpp -o program `root-config --cflags --glibs` -std=c++11
# g++ unit_test/model/test.cpp $(LIBDIR)/*.cpp -o program `root-config --cflags --glibs` -std=c++11
# g++ unit_test/nadir_dependency/nad_vs_e.cpp $(LIBDIR)/*.cpp -o program `root-config --cflags --glibs` -std=c++11
# g++ unit_test/flx_map/flxmap_compare.cpp $(LIBDIR)/*.cpp -o program `root-config --cflags --glibs` -std=c++11

run:
	g++ unit_test/model/fit.cpp $(LIBDIR)/*.cpp -o program `root-config --cflags --glibs` -std=c++11
	./program
	# g++ unit_test/model/vsother.cpp $(LIBDIR)/*.cpp -o program `root-config --cflags --glibs` -std=c++11
	# ./program
	# g++ unit_test/flx_map/readexpmap.cpp $(LIBDIR)/*.cpp -o program `root-config --cflags --glibs` -std=c++11
	# ./program

compile:
	mpic++ unit_test/exposure_map_cpp/main_mpi3.cpp -o unit_test/exposure_map_cpp/limb_exposure_mpi -std=c++11

rootenv:
	module load anaconda/2.7
	source /opt/ohpc/pub/apps/anaconda2/bin/activate fermi

sync:
	rsync -av ../LimbCRs/ jab@newgalaxy:/work/jab/LimbCRs	
# rsync -auv ../LimbCRs/ jab@newgalaxy:/work/jab/LimbCRs

compile_and_sync: compile sync

clean:
	rm -rf data/exposure_map/P8R2_SOURCE_V6/*
	rm -rf data/exposure_map/P8R2_ULTRACLEANVETO_V6/*
	rm -rf *.png
	rm -rf data/root/extracted_data.root
	rm -rf data/exposure_map/w*
	rm -rf model/simdata/*.csv