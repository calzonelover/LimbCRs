import numpy as np
import math

def d2r(d):
    return d * math.pi / 180.0

def r2d(r):
    return r * 180.0 / math.pi

def get_T_eq_sp(de_sp, ra_sp):
    x_p = [math.cos(de_sp)*math.cos(ra_sp), math.cos(de_sp)*math.sin(ra_sp), math.sin(de_sp)]
    # y_p = [math.cos(de_sp)*math.cos(ra_sp+math.pi/2), math.cos(de_sp)*math.sin(ra_sp+math.pi/2), math.sin(de_sp)]
    z_p = [0.0, -math.sin(de_sp), math.cos(de_sp)]
    y_p = np.cross(z_p, x_p)
    return np.array([x_p, y_p, z_p])

def get_T_eq_p(de_x_p, ra_x_p, de_z_p, ra_z_p):
    x_p = [math.cos(de_x_p)*math.cos(ra_x_p), math.cos(de_x_p)*math.sin(ra_x_p), math.sin(de_x_p)]
    z_p = [math.cos(de_z_p)*math.cos(ra_z_p), math.cos(de_z_p)*math.sin(ra_z_p), math.sin(de_z_p)]
    y_p = np.cross(z_p, x_p)
    return np.array([x_p, y_p, z_p])