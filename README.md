# Hi there
Indirect measurement CRs spectrum from gamma-ray spectrum which measured by Fermi LAT

# Issue
* Extract new finaltree.root file which contained a LAT_rocking_angle
* Extract better gamma-ray spectrum that take into account LAT_rocking_angle
* Make a new approximation flux -> compare to previous Limb's paper (2014) ? (waiting root file)
* Flux value from exposure map was so weird ???
* Redefined likelihood function from flux -> count comparation

# This work
* Extract Limb's gamma-ray flux data from `finaltree.root` and `exposuremap` by `PerfecrFlux.py`, then keep processing file in `alldat.olo`
* Find error of parameter by using Monte Carlo simulation : `ErrorStat.py` , `ErrorTotal.py`

# File description
* K&O model : `SPLwHe.f` , `BPLwHe.f`
* Scan Range of good trial parameter : `ScanMountain.py`