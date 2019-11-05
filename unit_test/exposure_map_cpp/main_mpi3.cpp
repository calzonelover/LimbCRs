#include <stdio.h>
#include <stdlib.h>
#include <string>
#include <vector>
#include <sstream>
#include <iostream>
#include <fstream>
#include <ctime>
#include <math.h>

#include <mpi.h>

#include "main_mpi.h"

/*
 Compile using c++ 11
 g++ main.cpp -o out -std=c++11
 Elapses time 7.37503 s (livetime week 164)
 Elapses time 11.8531 s (expmap week 164 including 50 energy mid bins)

 // MPI
 week 164 performance
  * Normal res Master-Slave
    - slave 1: CPU time 15.079796 s
    - slave 2: CPU time 7.867394 s
    - slave 4: CPU time 3.842406 s
    - slave 6: CPU time 2.668725 s
    - slave 8: CPU time 2.324213 s
    - slave 10: CPU time 1.972297 s
  * Full res Master-Slave
    - (slave=11) CPU time 784.306050 s

 Full week 10-550 takes around 5 hour with 150 slaves

 how to run
 >> mpic++ main_mpi.cpp -o out.o -std=c++11
 >> mpirun -np 2 out.o
*/

int main(int argc, char** argv){
    // MPI
    int rank, size;
    MPI_Status status;
    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);
    
    MPI_Datatype MPI_EXPMAP, MPI_FT2;
    int block_lengths_expmap[2] = {1, N_BINS_PHI_NADIR*N_BINS_THETA_NADIR};
    MPI_Aint offsets_expmap[2] = {offsetof(EXPMAP, energyGEV), offsetof(EXPMAP, exp_map)};
    MPI_Datatype type_expmap[2] = { MPI_FLOAT, MPI_DOUBLE };
    MPI_Type_create_struct(
        2,
        block_lengths_expmap,
        offsets_expmap,
        type_expmap,
        &MPI_EXPMAP
    );
    MPI_Type_commit(&MPI_EXPMAP);
    MPI_Type_contiguous(10, MPI_FLOAT, &MPI_FT2);
    MPI_Type_commit(&MPI_FT2);

    if (rank == 0){
		printf("number of processes = %d\n", size);
	}
	printf("Init process rank %d\n", rank);

    d_phi = float(PHI_NADIR_MAX-PHI_NADIR_MIN)/float(N_BINS_PHI_NADIR);
    d_theta = float(THETA_NADIR_MAX-THETA_NADIR_MIN)/float(N_BINS_THETA_NADIR);

    expmaps = getZeroExposureMaps();
    std::vector<EFFECTIVE_AREA> effs = getEffectiveAreas();

    if (rank == 0){ // Master
        int numsent;
        int j, slave;

        std::vector<FT2> ft2_rows = getAllFT2fromCSV();
        numsent = 0;

        double start_t = MPI_Wtime();
        // wake slave up (first send)
        for (unsigned int i=1; i<size; i++){
            j = numsent++;
            MPI_Send(&ft2_rows[j], 1, MPI_FT2, i, TAG_INPROGRESS, MPI_COMM_WORLD);
            std::cout << "Master send to slave # " << i << std::endl;
        }
        for (unsigned int i=0; i<ft2_rows.size(); i++){
            MPI_Recv(&slave, 1, MPI_INT, MPI_ANY_SOURCE, MPI_ANY_TAG, MPI_COMM_WORLD, &status);
            if (numsent < ft2_rows.size()){
                j = numsent++;
                MPI_Send(&ft2_rows[j], 1, MPI_FT2, slave, TAG_INPROGRESS, MPI_COMM_WORLD);
            }
            else {
                MPI_Send(&ft2_rows[j], 1, MPI_FT2, slave, TAG_DONE, MPI_COMM_WORLD);
            }
        }
        double stop_t = MPI_Wtime();
        double cpu_time = stop_t-start_t;
        printf("Master-Slave (slave=%d) CPU time %lf s\n", size-1,cpu_time);
    }
    else { // Slave
        int tag; FT2 ft2_row;

        r_sp = (float*)malloc(3*sizeof(float));
        r_eq = (float*)malloc(3*sizeof(float));
        r_p = (float*)malloc(3*sizeof(float));
        t_eq_p = (float*)malloc(9*sizeof(float));
        t_eq_sp = (float*)malloc(9*sizeof(float));
        inv_t_eq_sp = (float*)malloc(9*sizeof(float));

        do {
            MPI_Recv(&ft2_row, 1, MPI_FT2, 0, MPI_ANY_TAG, MPI_COMM_WORLD, &status);
            tag = status.MPI_TAG;
            if (tag == TAG_DONE)
                break;
            get_T_eq_sp(
                d2r(ft2_row.DEC_ZENITH), d2r(ft2_row.RA_ZENITH),
                t_eq_sp
            );
            inverseMatrix(t_eq_sp, inv_t_eq_sp, 3);
            get_T_eq_p(
                d2r(ft2_row.DEC_SCX), d2r(ft2_row.RA_SCX),
                d2r(ft2_row.DEC_SCZ), d2r(ft2_row.RA_SCZ),
                t_eq_p
            );
            for (unsigned int i_phi_nad=0; i_phi_nad < N_BINS_PHI_NADIR; i_phi_nad++){
                for (unsigned int i_theta_nad=0; i_theta_nad < N_BINS_THETA_NADIR; i_theta_nad++){
                    phi_nadir = d2r(float(PHI_NADIR_MIN) + d_phi * float(i_phi_nad));
                    theta_nadir = d2r(float(THETA_NADIR_MIN) + d_theta * float(i_theta_nad));

                    r_sp[0] = -cos(theta_nadir); r_sp[1] = sin(theta_nadir)*sin(phi_nadir); r_sp[2] = sin(theta_nadir)*cos(phi_nadir);
                    matrix_mul_vector(inv_t_eq_sp, r_sp, r_eq, 3, 3);
                    matrix_mul_vector(t_eq_p, r_eq, r_p, 3, 3);

                    rho = sqrt(r_p[0]*r_p[0] + r_p[1]*r_p[1]);
                    theta_p = float(PI)/2.0f - atan(r_p[2]/rho);
                    phi_p = r_p[1] < 0.0f ? acos(r_p[0]/rho) : 2.0f*float(PI) - acos(r_p[0]/rho);
                    if (r2d(theta_p) < float(THETA_LAT_CUTOFF)){
                        for (unsigned int i_energy=0; i_energy<N_E_BINS; i_energy++){
                            expmaps[i_energy].exp_map[i_phi_nad + i_theta_nad * N_BINS_PHI_NADIR] += 
                                double(ft2_row.LIVETIME * effs[i_energy].eff_m2[int(floor(r2d(theta_p)))]);
                        }
                    }
                }
            }
            MPI_Send(&rank, 1, MPI_INT, 0, rank, MPI_COMM_WORLD);
        } while (true);
        free(r_sp);free(r_eq);free(r_p);
        free(t_eq_p);free(t_eq_sp);free(inv_t_eq_sp);
    }
    // Gather Expmap
    MPI_Barrier(MPI_COMM_WORLD);
    if (rank == 0){
        std::vector<EXPMAP> recv_expmaps = getZeroExposureMaps();
        for (unsigned int i=1; i<size; i++){
            MPI_Recv(recv_expmaps.data(), N_E_BINS, MPI_EXPMAP, MPI_ANY_SOURCE, MPI_ANY_TAG, MPI_COMM_WORLD, &status);
            for (unsigned int i_energy=0; i_energy<N_E_BINS; i_energy++){
                for (unsigned int i=0; i<N_BINS_THETA_NADIR*N_BINS_PHI_NADIR; i++) expmaps[i_energy].exp_map[i] += recv_expmaps[i_energy].exp_map[i];
            }
        }
    } else {
        MPI_Send(expmaps.data(), N_E_BINS, MPI_EXPMAP, 0, rank, MPI_COMM_WORLD);
    }
    // Write Expmap
    MPI_Barrier(MPI_COMM_WORLD);
    if (rank == 0){
        for (unsigned int i_energy=0; i_energy<N_E_BINS; i_energy++){
            std::string specialname_out = "../../data/exposure_map/" + std::string(IRF_NAME) +"/expmap_E" + std::to_string(int(floor(effs[i_energy].energy_mid_bin))) + ".csv";
            writeFile(specialname_out, expmaps[i_energy].exp_map, N_BINS_PHI_NADIR*N_BINS_THETA_NADIR);
        }
    }
    MPI_Type_free(&MPI_EXPMAP); MPI_Type_free(&MPI_FT2);
    MPI_Finalize();
    return 0;
}










// IO
std::string getSpecialFilename(int _week, std::string name){
  std::string week = std::to_string(_week);
  while (week.size() < 3){
    week = "0" + week;
  }
  return name + "_w" + week + ".csv";
}

std::vector<FT2> readFT2CSV(std::string _filename){
  std::string _filename2 = "../../data/raw/csv/" + _filename;
  std::ifstream file(_filename2);
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

void readEffCSV(std::string _filename, float energy_mid_bin, double *out_eff_m2, float *out_theta_nadirs){
    std::ifstream file(_filename);
    if (!file.good()){
        std::cout << "file " << _filename << " does not exist"  << std::endl;
        std::cout << "Program exit!" << std::endl;
        exit(0);
    }

    std::string line;
    int row_i = 0;

    while(getline(file, line,'\n')){
        if (row_i > 0 && !file.eof() && row_i <= int(THETA_LAT_CUTOFF+1)){
            std::istringstream templine(line);
            std::vector<float> row;
            std::string data;            
            while (std::getline(templine, data,','))
            {
                row.push_back(atof(data.c_str()));
            }
            out_eff_m2[row_i-1] = double(row[1]);
            out_theta_nadirs[row_i-1] = row[0];
        }
        row_i++;
    }
    file.close();
}

std::vector<FT2> getAllFT2fromCSV(){
    std::vector<FT2> ft2_rows;
    for (unsigned int week = WEEK_BEGIN; week <= WEEK_END; week++){
        std::string file_ft2 = getSpecialFilename(week, "ft2");
        std::vector<FT2> _ft2_rows = readFT2CSV(file_ft2);
        ft2_rows.insert(ft2_rows.end(), _ft2_rows.begin(), _ft2_rows.end());
    }
    std::cout << "#row of all FT2: " << ft2_rows.size() << std::endl;
    return ft2_rows;
}

template <class T>
void writeFile(std::string filename, T *vec, int size_vec){
	std::ofstream out_hist;
	out_hist.open(filename);
    for (unsigned int i=0; i < N_BINS_PHI_NADIR; i++){
        for (unsigned int j=0; j < N_BINS_THETA_NADIR; j++){
            out_hist << vec[i + j * N_BINS_PHI_NADIR] << "," << std::endl;
        }
    }
	out_hist.close();
}

// TRANSFORM
float d2r(float d){
    return d * float(PI) / 180.0f;
}

float r2d(float r){
    return r * 180.0f / float(PI);
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

// MATH
template <class T>
void crossProduct(T *_A, T *_B, T *_C){
    _C[0] = _A[1] * _B[2] - _A[2] * _B[1];
    _C[1] = _A[2] * _B[0] - _A[0] * _B[2];
    _C[2] = _A[0] * _B[1] - _A[1] * _B[0];
}



template <class T>
void matrix_mul_vector(T *m, T *v, T *v_out, int N, int M){
    for (unsigned int j=0;j<M;j++)
    {
        T sum = 0;
        for (unsigned int i=0;i<N;i++)
        {
            sum += m[i+j*3] * v[i];
        }
        v_out[j] = sum;
    }
}

template <class T>
void printMatrix(T *x, int n, int m){
    for (unsigned int j=0;j<m;j++){
		for (unsigned int i=0;i<n;i++){
			std::cout << x[i+j*n] << " ";
		}
        std::cout << std::endl;
	}
}

// MATRIX INVERSION
void inverseMatrix(float *x, float *y, int order){
    float **_x = new float*[order];
    float **_y = new float*[order];
    for(unsigned int i=0 ; i<order ; i++)
    {
        _x[i] = new float[order];
        _y[i] = new float[order];
    }
	for (unsigned int j=0;j<order;j++){
		for (unsigned int i=0;i<order;i++){
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

/* Utility */
void assignEnergyBin(float *_energy_mid_bins, float energy_start_gev = float(E_START_GEV), float energy_end_gev = float(E_STOP_GEV)){
    float divider, e2d, e1d, ln;
    float *energy_edge_bins = (float*)malloc((N_E_BINS+1)*sizeof(float));
    for (unsigned int i=0; i <= N_E_BINS; i++){
        energy_edge_bins[i] = energy_start_gev * pow(energy_end_gev/energy_start_gev, float(i)/float(N_E_BINS));
    }
    for (unsigned i=0; i < N_E_BINS; i++){
        divider = 1.0f - float(GAMMA);
        e2d = pow(energy_edge_bins[i+1], divider);
        e1d = pow(energy_edge_bins[i], divider);
        ln = log(0.5f*(e2d - e1d)+ e1d);
        _energy_mid_bins[i] = exp(ln/(divider));
    }
    free(energy_edge_bins);
}

std::vector<EXPMAP> getZeroExposureMaps(){
    std::vector<EXPMAP> expmaps;
    float *energy_mid_bins = (float*)malloc(N_E_BINS*sizeof(float));
    assignEnergyBin(energy_mid_bins);
    for (unsigned int k=0; k<N_E_BINS; k++){
        EXPMAP expmap = {
            .energyGEV = energy_mid_bins[k],
        };
        for (unsigned int i=0; i<N_BINS_THETA_NADIR*N_BINS_PHI_NADIR; i++) expmap.exp_map[i] = double(0);
        expmaps.push_back(expmap);
    }
    free(energy_mid_bins);
    return expmaps;
}

std::vector<EFFECTIVE_AREA> getEffectiveAreas(){
    std::vector<EFFECTIVE_AREA> eff_rows;
    std::string _filename;
    float energy_mid_bin;

    float *energy_mid_bins = (float*)malloc(N_E_BINS*sizeof(float));
    assignEnergyBin(energy_mid_bins);
    for (unsigned int i=0; i<N_E_BINS; i++){
        energy_mid_bin = energy_mid_bins[i];
        _filename = "../../effective_area/static_table/" + std::string(IRF_NAME) + "/eff_E" + std::to_string(int(floor(energy_mid_bin))) + ".csv";        
        EFFECTIVE_AREA eff = {
            .eff_m2 = (double*)malloc(int(THETA_LAT_CUTOFF+1)*sizeof(double)),
            .theta_nadir = (float*)malloc(int(THETA_LAT_CUTOFF+1)*sizeof(float)),
            .energy_mid_bin = energy_mid_bin,
        };
        readEffCSV(_filename, energy_mid_bin, eff.eff_m2, eff.theta_nadir);
        eff_rows.push_back(eff);
    }
    free(energy_mid_bins);
    return eff_rows;
}