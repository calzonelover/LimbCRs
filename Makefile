LIBDIR := utility/cpp

# g++ unit_test/flx_map/flxmap.cpp $(LIBDIR)/*.cpp -o program `root-config --cflags --glibs` -std=c++11
# g++ unit_test/flx_map/readexpmap.cpp $(LIBDIR)/*.cpp -o program `root-config --cflags --glibs` -std=c++11
# g++ unit_test/model/test.cpp $(LIBDIR)/*.cpp -o program `root-config --cflags --glibs` -std=c++11
run:
	g++ unit_test/model/test.cpp $(LIBDIR)/*.cpp -o program `root-config --cflags --glibs` -std=c++11
	./program

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
	rm data/exposure_map/P8R2_SOURCE_V6/*
	rm data/exposure_map/P8R2_ULTRACLEANVETO_V6/*
	rm *.png
	rm data/root/extracted_data.root