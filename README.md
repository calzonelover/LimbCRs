# Hi there
Indirect measurement CRs spectrum from gamma-ray spectrum which measured by Fermi LAT
# Issue
* FixRegionFlux branch : fix correction of region of interest when deal with theta-nadir shift due to LAT altitude
# This work
* Extract Limb's gamma-ray flux data from `finaltree.root` and `exposuremap` by `PerfecrFlux.py`, then keep processing file in `alldat.olo`
* Find error of parameter by using Monte Carlo simulation : `ErrorStat.py` , `ErrorTotal.py`
# File description
* K&O model : `SPLwHe.f` , `BPLwHe.f`
* Scan Range of good trial parameter : `ScanMountain.py`
