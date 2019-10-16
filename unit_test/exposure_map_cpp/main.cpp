#include <stdio.h>
#include <stdlib.h>
#include <string> 
#include <vector>
#include <sstream> //istringstream
#include <iostream> // cout
#include <fstream> // ifstream
#include <math.h> 

#include "main.h"

/*
 Compile using c++ 11
 g++ main.cpp -o out -std=c++11
*/

int main(){
    int week = 164;
    std::string file_ft2 = getFT2Filename(week);
    std::vector<FT2> ft2_rows = readCSV(file_ft2);

    float *t_eq_p = (float*)malloc(9*sizeof(float));
    get_T_eq_sp(ft2_rows[40].DEC_ZENITH, ft2_rows[40].RA_ZENITH, t_eq_p);
    std::cout << "\n\n Separate \n\n" << std::endl;
    for (unsigned int i=0; i<9; i++){
      std::cout << t_eq_p[i] << std::endl;
    }
    // std::cout << ft2_rows[20].DEC_SCZ << std::endl;
}

std::vector<FT2> readCSV(std::string _filename){
  std::ifstream file(_filename);
  std::vector<FT2> ft2_rows;
  
  if (!file.good()){
    std::cout << "file " << _filename << " does not exist"  << std::endl;
    std::cout << "Program exit!" << std::endl;
    exit(0);
  }

  std::string line;
  int row_i = 0;

  while (getline(file, line,'\n'))
	{
    if (row_i > 0 && !file.eof()){
      std::istringstream templine(line);
      // std::cout << line << std::endl;
      std::vector<float> row;
      std::string data;
      while (std::getline(templine, data,','))
      {
        row.push_back(atof(data.c_str()));
      }
      
      FT2 row_ft2 = {
        .DEC_SCX = row[1],
        .DEC_SCZ = row[2],
        .DEC_ZENITH = row[3],
        .LIVETIME = row[4],
        .RA_SCX = row[5],
        .RA_SCZ = row[6],
        .RA_ZENITH = row[7],
        .ROCK_ANGLE = row[8],
        .START = row[9],
        .STOP = row[10],
      };
      ft2_rows.push_back(row_ft2);
    }
    row_i++;
	}
  file.close();
  return ft2_rows;
}

std::string getFT2Filename(int _week){
  std::string week = std::to_string(_week);
  while (week.size() < 3){
    week = "0" + week;
  }
  return "ft2_w" + week + ".csv";
}


/* Utility */
void crossProduct(float *_A, float *_B, float *_C){
    _C[0] = _A[1] * _B[2] - _A[2] * _B[1]; 
    _C[1] = _A[0] * _B[2] - _A[2] * _B[0]; 
    _C[2] = _A[0] * _B[1] - _A[1] * _B[0]; 
}

// void matrixMultiply(float *_A, float *_B, float *_C){

// }

float d2r(float d){
    return d * PI / 180.0;
}

float r2d(float r){
    return r * 180.0 / PI;
}

void get_T_eq_sp(float de_sp, float ra_sp, float *t_eq_p){
    float *x_p = (float*)malloc(3*sizeof(float));
    float *y_p = (float*)malloc(3*sizeof(float));
    float *z_p = (float*)malloc(3*sizeof(float));
    x_p[0] = cos(de_sp)*cos(ra_sp); x_p[1] = cos(de_sp)*sin(ra_sp); x_p[2] = sin(ra_sp);
    z_p[0] = 0.0f; z_p[1] = -sin(de_sp); z_p[2] = cos(de_sp);
    crossProduct(z_p, x_p, y_p);
    for (unsigned int i=0; i<9; i++){
        if (i < 3) *t_eq_p = x_p[i];
        if (i >= 3 && i < 6) *t_eq_p = y_p[i];
        if (i >= 6 && i < 9) *t_eq_p = z_p[i];
    }
    for (unsigned int i=0; i<3; i++){
      std::cout << x_p[i] << std::endl;
    }
    for (unsigned int i=0; i<3; i++){
      std::cout << y_p[i] << std::endl;
    }
    for (unsigned int i=0; i<3; i++){
      std::cout << z_p[i] << std::endl;
    }
    std::cout << "\n Full \n" << std::endl;
    for (unsigned int i=0; i<9; i++){
      std::cout << t_eq_p[i] << std::endl;
    }
}