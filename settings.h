#ifndef SETTINGS
#define SETTINGS

// settings
#define PHOTON_PATH "data/raw/ft1/"

#define GAMMA 2.66
#define E_START_GEV 10
#define E_STOP_GEV 1000
#define N_E_BINS 50
#define IRF_NAME "P8R2_ULTRACLEANVETO_V6" // P8R2_SOURCE_V6 , P8R2_ULTRACLEANVETO_V6

#define WEEK_BEGIN 10
#define WEEK_END 540

#define THETA_LAT_CUTOFF 70.0

#define N_BINS_PHI_NADIR 180
#define PHI_NADIR_MIN 0.0
#define PHI_NADIR_MAX 360.0
#define N_BINS_THETA_NADIR 800
#define THETA_NADIR_MIN 0.0
#define THETA_NADIR_MAX 80.0

#define PI 3.14159265

// MPI
#define TAG_DONE 0
#define TAG_INPROGRESS 1

#endif