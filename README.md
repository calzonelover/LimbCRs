# Hi there
Indirect measurement CRs spectrum from gamma-ray spectrum which measured by Fermi LAT

# To do list
* Investigate Flux why it's so weird : maybe from expmap or from count
* Redefined likelihood function from flux -> count => Likelihood ratio test SPL and BPL

# This work
* Extract Limb's gamma-ray flux data from `finaltree.root` and `exposuremap` by `PerfecrFlux.py`, then keep processing file in `alldat.olo`

# File description
* K&O model : `SPLwHe.f` , `BPLwHe.f`
* Scan Range of good trial parameter : `ScanMountain.py`