#ifndef MAIN
#define MAIN

// settings
#define GAMMA 2.66
#define E_START_GEV 10
#define E_STOP_GEV 1000
#define N_E_BINS 50

#define THETA_LAT_CUTOFF 70.0

#define N_BINS_PHI_NADIR 20
#define PHI_NADIR_MIN 0.0
#define PHI_NADIR_MAX 360.0
#define N_BINS_THETA_NADIR 100
#define THETA_NADIR_MIN 0.0
#define THETA_NADIR_MAX 160.0

typedef struct FT2 {
  float DEC_SCX;
  float DEC_SCZ;
  float DEC_ZENITH;
  float LIVETIME;
  float RA_SCX;
  float RA_SCZ;
  float RA_ZENITH;
  float ROCK_ANGLE;
  float START;
  float STOP;
} FT2;

typedef struct EXPMAP {
  float energyGEV;
  double *exp_map;
} EXPMAP;

std::string getSpecialFilename(int _week, std::string name);
std::vector<FT2> readCSV(std::string _filename);

/* Utility */
#define PI 3.14159265

float d2r(float d);
float r2d(float r);

void get_T_eq_sp(float de_sp, float ra_sp, float *t_eq_sp);
void get_T_eq_p(float de_x_p, float ra_x_p, float de_z_p, float ra_z_p, float *t_eq_p);

template <class T>
void crossProduct(T *_A, T *_B, T *_C);

template <class T>
void matrix_mul_vector(T *m, T *v, T *v_out, int N, int M);

template <class T>
void printMatrix(T *x, int n, int m);

template <class T>
void writeFile(std::string filename, T *vec, int size_vec);

void assignEnergyBin(float *_energy_mid_bins, float energy_start_gev, float energy_end_gev);
std::vector<EXPMAP> getZeroExposureMaps();

// Matrix inversion
void inverseMatrix(float *x, float *y, int order);
void matrixInversion(float **A, int order, float **Y);
int getMinor(float **src, float **dest, int row, int col, int order);
double calcDeterminant(float **mat, int order);

double *live_map; std::vector<EXPMAP> expmaps; float *energy_mid_bins;
float d_phi, d_theta;
float phi_nadir, theta_nadir, rho, theta_p, phi_p;

unsigned int week;

float *r_sp, *r_eq, *r_p, *t_eq_p, *t_eq_sp, *inv_t_eq_sp;

clock_t t_begin, t_end;

#endif

