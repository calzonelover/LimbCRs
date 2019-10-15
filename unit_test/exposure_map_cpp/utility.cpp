#include <stdlib.h>
#include <vector>
#include <math.h> 

#include "utility.h"

void crossProduct(float *_A, float *_B, float *_C) {
    _C[0] = _A[1] * _B[2] - _A[2] * _B[1]; 
    _C[1] = _A[0] * _B[2] - _A[2] * _B[0]; 
    _C[2] = _A[0] * _B[1] - _A[1] * _B[0]; 
}

float d2r(float d){
    return d * PI / 180.0;
}

float r2d(float r){
    return r * 180.0 / PI;
}

void get_T_eq_sp(float de_sp, float ra_sp, float *t_eq_p){
    float *x_p, *z_p, *y_p = (float*)malloc(3*sizeof(float));
    x_p[0] = cos(de_sp)*cos(ra_sp); x_p[1] = cos(de_sp)*sin(ra_sp);x_p[2] = sin(ra_sp);
    z_p[0] = 0.0; z_p[1] = -sin(de_sp); z_p[2] = cos(de_sp);
    crossProduct(z_p, x_p, y_p);
    for (unsigned int i=0; i<9; i++){
        if (i < 3) t_eq_p = &x_p[i];
        if (i >= 3 && i < 6) t_eq_p = &y_p[i];
        if (i >= 6 && i < 9) t_eq_p = &z_p[i];
    }
}