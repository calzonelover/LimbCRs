# Limb's CR

- 540 #row of all FT2: 9012755
- 

## Todo

- Compare 2 methods flux calculation
- Find the articles for
  - LAT energy biases
  - Earth's altitude shifted 
- ?? Shall we change fraction of p/He in rigidity to be a free parameter and compare to AMS-02 rather than using it
- Recalculate flux
- Connect the gfortran model with c++ kernel to fit experimental data
- Finding the sigma from LRT 
- Performing Monte Carlo Simulation

## Resources

* Weekly raw data
https://fermi.gsfc.nasa.gov/ssc/data/access/

* FITs Column descriptions
https://fermi.gsfc.nasa.gov/ssc/data/analysis/documentation/Cicerone/Cicerone_Data/LAT_Data_Columns.html


* Effective area
https://www.slac.stanford.edu/exp/glast/groups/canda/lat_Performance.htm

* F. Spada Fermi LAT highlight 2016
https://agenda.infn.it/event/10546/contributions/3646/attachments/2619/2904/spada-LAT_CRIS2016.pdf

* Inverse theory class
https://mcsc.sc.mahidol.ac.th/courses/ita/

### New Galaxy (Space) Cluster
* Slurm and OpenMPI job submission
  https://hpcrcf.atlassian.net/wiki/spaces/TCP/pages/7287338/How-to+Submit+a+MPI+Job

* Cluster Monitoring
  http://space.sc.mahidol.ac.th/ganglia/?m=load_one&c=Galaxy-Cluster&h=&p=2&tab=m&vn=&hide-hf=false&hc=4&p=2

* Submit the job
  >> sbatch limbCRs.sh

* Check available module
  ```bash
  module avail
  ```

### CPP

Guild https://hiltmon.com/blog/2013/07/03/a-simple-c-plus-plus-project-structure/





### Optimized parameters (best fit)

## Simulated Annealing

SPL

N_all: 0.0108013 , N_0: 3.77133 , g1: 2.6637 , g2: 2.63837 , E_b: 367.323
T: 9.87849e-05, Loss: 361.647

BPL
N_all: 0.0102916 , N_0: 3.8547 , g1: 2.94758 , g2: 2.52203 , E_b: 336.069
T: 9.5402e-05, Loss: 670.067

## Particle Swarm Algorithm

SPL
<!-- - negative-log-Likelihood = 359.34
- gamma1 = 2.67 -->
N_all: 0.0108668 , N_0: 2.82851 , g1: 2.70266 , g2: 2.65207 , E_b: 342.546
Loss: 359.023 , Loss SD: 0.0397608

BPL
N_all: 0.0108818 , N_0: 1.98848 , g1: 2.86015 , g2: 2.63161 , E_b: 333.115
Loss: 358.937 , Loss SD: 0.0914711

<!-- P-Value is .917594 -->
Sigma = 1.38