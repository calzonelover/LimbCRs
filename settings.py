THETA_LAT_CUTOFF = 70.0
EVENT_CLASS = 24 # ULTRACLEANVETO
THETA_NADIR_CUT_MIN, THETA_NADIR_CUT_MAX = None, None

# 2D Map
N_BINS_PHI_NADIR = int(180/9)
PHI_NADIR_MIN, PHI_NADIR_MAX = 0.0, 360.0
D_PHI = (PHI_NADIR_MAX - PHI_NADIR_MIN)/N_BINS_PHI_NADIR

N_BINS_THETA_NADIR = int(1600/16)
THETA_NADIR_MIN, THETA_NADIR_MAX = 0.0, 160.0
D_THETA = (THETA_NADIR_MAX - THETA_NADIR_MIN)/N_BINS_THETA_NADIR