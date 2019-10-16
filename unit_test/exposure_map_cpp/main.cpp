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

    float *t_eq_sp = (float*)malloc(9*sizeof(float));
    // get_T_eq_sp(ft2_rows[40].DEC_ZENITH, ft2_rows[40].RA_ZENITH, t_eq_sp);
    // for (unsigned int i=0; i<9; i++){
    //   std::cout << t_eq_sp[i] << std::endl;
    // }
	float *t_eq_p = (float*)malloc(9*sizeof(float));
	float *inv_t_eq_p = (float*)malloc(9*sizeof(float));
	// get_T_eq_p(ft2_rows[40].DEC_SCX, ft2_rows[40].RA_SCX, ft2_rows[40].DEC_SCZ, ft2_rows[40].RA_SCZ, t_eq_p);
	// inverseMatrix(t_eq_p, inv_t_eq_p, 3);
    for (unsigned int i=0; i<9; i++){
      std::cout << t_eq_p[i] << std::endl;
    }
    // for (unsigned int i=0; i<9; i++){
    //   std::cout << inv_t_eq_p[i] << std::endl;
    // }

	free(t_eq_sp);free(t_eq_p);
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

float d2r(float d){
    return d * PI / 180.0;
}

float r2d(float r){
    return r * 180.0 / PI;
}

void get_T_eq_sp(float de_sp, float ra_sp, float *t_eq_sp){
    float *x_p = (float*)malloc(3*sizeof(float));
    float *y_p = (float*)malloc(3*sizeof(float));
    float *z_p = (float*)malloc(3*sizeof(float));
    x_p[0] = cos(de_sp)*cos(ra_sp); x_p[1] = cos(de_sp)*sin(ra_sp); x_p[2] = sin(de_sp);
    z_p[0] = 0.0f; z_p[1] = -sin(de_sp); z_p[2] = cos(de_sp);
    crossProduct(z_p, x_p, y_p);
    for (unsigned int i=0; i<9; i++){
      if (i < 3) t_eq_sp[i] = x_p[i%3];
      if (i > 2 && i < 6) t_eq_sp[i] = y_p[i%3];
      if (i > 5 && i < 9) t_eq_sp[i] = z_p[i%3];
    }
	free(x_p);free(y_p);free(z_p);
}

void get_T_eq_p(float de_x_p, float ra_x_p, float de_z_p, float ra_z_p, float *t_eq_p){
    float *x_p = (float*)malloc(3*sizeof(float));
    float *y_p = (float*)malloc(3*sizeof(float));
    float *z_p = (float*)malloc(3*sizeof(float));
	x_p[0] = cos(de_x_p)*cos(ra_x_p); x_p[1] = cos(de_x_p)*sin(ra_x_p); x_p[2] = sin(de_x_p);
	z_p[0] = cos(de_z_p)*cos(ra_z_p); z_p[1] = cos(de_z_p)*sin(ra_z_p); z_p[2] = sin(de_z_p);
	crossProduct(z_p, x_p, y_p);
    for (unsigned int i=0; i<9; i++){
      if (i < 3) t_eq_p[i] = x_p[i%3];
      if (i > 2 && i < 6) t_eq_p[i] = y_p[i%3];
      if (i > 5 && i < 9) t_eq_p[i] = z_p[i%3];
    }
    free(x_p);free(y_p);free(z_p);
}

// Matrix inversion
// the result is put in Y
void inverseMatrix(float *x, float *y, int order){
	float **_x = new float*[order];
	float **_y = new float*[order];
	for (unsigned int j=0; j<order; j++){
		for (unsigned int i=0; i<order; i++){
			_x[i][j] = x[i+j*order];
		}
	}
	matrixInversion(_x, order, _y);
	for (unsigned int j=0; j<order; j++){
		for (unsigned int i=0; i<order; i++){
			y[i+j*order] = _y[i][j];
		}
	}
    delete [] _x;
    delete [] _y;
}

void matrixInversion(float **A, int order, float **Y)
{
    // get the determinant of a
    double det = 1.0/calcDeterminant(A,order);
 
    // memory allocation
    float *temp = new float[(order-1)*(order-1)];
    float **minor = new float*[order-1];
    for(int i=0;i<order-1;i++)
        minor[i] = temp+(i*(order-1));
 
    for(int j=0;j<order;j++)
    {
        for(int i=0;i<order;i++)
        {
            // get the co-factor (matrix) of A(j,i)
            getMinor(A,minor,j,i,order);
            Y[i][j] = det*calcDeterminant(minor,order-1);
            if( (i+j)%2 == 1)
                Y[i][j] = -Y[i][j];
        }
    }
 
    // release memory
    //delete [] minor[0];
    delete [] temp;
    delete [] minor;
}
 
// calculate the cofactor of element (row,col)
int getMinor(float **src, float **dest, int row, int col, int order)
{
    // indicate which col and row is being copied to dest
    int colCount=0,rowCount=0;
 
    for(int i = 0; i < order; i++ )
    {
        if( i != row )
        {
            colCount = 0;
            for(int j = 0; j < order; j++ )
            {
                // when j is not the element
                if( j != col )
                {
                    dest[rowCount][colCount] = src[i][j];
                    colCount++;
                }
            }
            rowCount++;
        }
    }
 
    return 1;
}
 
// Calculate the determinant recursively.
double calcDeterminant( float **mat, int order)
{
    // order must be >= 0
    // stop the recursion when matrix is a single element
    if( order == 1 )
        return mat[0][0];
 
    // the determinant value
    float det = 0;
 
    // allocate the cofactor matrix
    float **minor;
    minor = new float*[order-1];
    for(int i=0;i<order-1;i++)
        minor[i] = new float[order-1];
 
    for(int i = 0; i < order; i++ )
    {
        // get minor of element (0,i)
        getMinor( mat, minor, 0, i , order);
        // the recusion is here!
 
        det += (i%2==1?-1.0:1.0) * mat[0][i] * calcDeterminant(minor,order-1);
        //det += pow( -1.0, i ) * mat[0][i] * CalcDeterminant( minor,order-1 );
    }
 
    // release memory
    for(int i=0;i<order-1;i++)
        delete [] minor[i];
    delete [] minor;
 
    return det;
}