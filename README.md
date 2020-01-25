# Limb's CR

## Todo

- Compare 2 methods flux calculation
- Find the articles for
  - LAT energy biases
  - Earth's altitude shifted 
- ?? Shall we change fraction of p/He in rigidity to be a free parameter and compare to AMS-02 rather than using it
- Recalculate flux
- Connect the gfortran model with c++ kernel to fit experimental data
- Finding the sigma from 
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
