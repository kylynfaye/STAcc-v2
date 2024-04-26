import numpy as np
import matplotlib.pyplot as plt

from STAcc_v2.object_info.StarTracker import StarTracker
from STAcc_v2.object_info.RSO import RSO

def range_calculator(x, y, z, X, Y, Z):
    color = 'red'
    
    for xi, yi, zi in zip(x, y, z):
        xi = xi[0]
        yi = yi[0]
        zi = zi[0]
        if (xi < np.max(X)) & (xi > np.min(X)) & \
           (yi < np.max(Y)) & (yi > np.min(Y)) & \
           (zi < np.max(Z)) & (zi > np.min(Z)):
            color = 'green'
            break

    return color

##########
# Future iterations may consider utilizing the accuracy measurements listed on
# star tracker datasheets to implement another layer of green/red checking.
##########