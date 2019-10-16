#ifndef MAIN
#define MAIN

typedef struct FT2
{
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

typedef struct EXPOSURE {
    float thetaNadir;
    float phiNadir;
    float livetime;
    float exposure;
} EXPOSURE;

std::string getFT2Filename(int _week);
std::vector<FT2> readCSV(std::string _filename);

/* Utility */
#define PI 3.14159265

void crossProduct(float *_A, float *_B, float *_C);

float d2r(float d);
float r2d(float r);

void get_T_eq_sp(float de_sp, float ra_sp, float *t_eq_p);

#endif

