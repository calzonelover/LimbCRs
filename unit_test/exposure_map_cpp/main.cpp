#include <stdlib.h>
#include <string>
#include <vector>
#include <sstream> //istringstream
#include <iostream> // cout
#include <fstream> // ifstream

#define WEEK 164

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

void crossProduct(float *_A, float *_B, float *_C);
void readCSV(char *_filename, float *_out);

int main(){
  char file_ft2[] = "ft2_w164.csv";
  float *out;
  readCSV(file_ft2, out);
}

void crossProduct(float *_A, float *_B, float *_C) {
    _C[0] = _A[1] * _B[2] - _A[2] * _B[1]; 
    _C[1] = _A[0] * _B[2] - _A[2] * _B[0]; 
    _C[2] = _A[0] * _B[1] - _A[1] * _B[0]; 
}

void readCSV(char *_filename, float *_out){
  std::ifstream file(_filename);
  std::vector<float> matrix;
  std::string line;

  while (getline(file, line,'\n'))
	{
	  std::istringstream templine(line);
	  std::string data;
    std::cout << line << std::endl;

	  for (std::getline(templine, data,','))
	  {
	    std::cout << data << std::endl;
	  }
    exit(0);
	  while (std::getline(templine, data,','))
	  {
	    matrix.push_back(atof(data.c_str()));
	  }
	}
  
  std::cout << matrix.size();
  file.close();
}