#ifndef SETTINGS
#define SETTINGS

// settings
#define PHOTON_PATH "data/raw/ft1/"

#define GAMMA 2.66

#define E_START_GEV 10
#define E_STOP_GEV 1000

#define THETA_E_NAD_MIN 68.4
#define THETA_E_NAD_MAX 70.0
#define THETA_NAD_BG_MIN 72.0
#define THETA_NAD_BG_MAX 80.0

#define N_E_BINS 50
#define IRF_NAME "P8R2_ULTRACLEANVETO_V6" // P8R2_SOURCE_V6 , P8R2_ULTRACLEANVETO_V6

#define WEEK_BEGIN 10
#define WEEK_END 540 // 399 old work, 540 new work

#define THETA_LAT_CUTOFF 70.0

/// Initial params
#define INI_TOTAL_NORM 0.01
#define INI_NORM_PL 2.2
// #define INI_GAMMA1 2.7 // SPL
#define INI_GAMMA1 2.84 // BPL
#define INI_GAMMA2 2.60
#define INI_E_BREAK 340.0
// range of params
#define INI_TOTAL_NORM_MIN 0.001
#define INI_TOTAL_NORM_MAX 0.1
#define INI_NORM_PL_MIN 1.0
#define INI_NORM_PL_MAX 5.0
// SPL
#define INI_GAMMA1_MIN 2.5
#define INI_GAMMA1_MAX 2.9
// BPL
// #define INI_GAMMA1_MIN 2.6
// #define INI_GAMMA1_MAX 3.0

#define INI_GAMMA2_MIN 2.6
#define INI_GAMMA2_MAX 2.7
#define INI_E_BREAK_MIN 310.0
#define INI_E_BREAK_MAX 350.0

// Visualize
#define N_BINS_PHI_NADIR 180
#define PHI_NADIR_MIN 0.0
#define PHI_NADIR_MAX 360.0
#define N_BINS_THETA_NADIR 800
#define THETA_NADIR_MIN 0.0
#define THETA_NADIR_MAX 80.0

// Constant
#define PI 3.14159265
#define PROTON_MASS 0.938

// MPI
#define TAG_DONE 0
#define TAG_INPROGRESS 1

#endif