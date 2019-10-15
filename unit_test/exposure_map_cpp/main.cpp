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
    

    //std::cout << ft2_rows[20].DEC_SCZ << std::endl;
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