import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import datetime as dt
import math as m

def star_tracker_plotter(ax, tip_position=(0,0,200), FOV1=0.261799, FOV2=0.314159, height=3000, theta=10, phi=60, psi=0):
    a, b, c = tip_position
    r = 6781

    num_points = 50
    thetap = np.linspace(0, 2*np.pi, num_points)  # Azimuthal angle
    z = np.linspace(0, height, num_points)  # Height of the cone (decreasing)

    T, Z = np.meshgrid(thetap, z)

    major_radius = height*np.tan(FOV1/2)
    minor_radius = height*np.tan(FOV2/2)

    majradius = major_radius * (1 - Z / height)  # Linearly varying radius
    minradius = minor_radius * (1 - Z / height)  # Linearly varying radius

    X = majradius * np.cos(T) + a
    Y = minradius * np.sin(T) + b
    Z = -Z + r + c + height # just orients the cone to start at the north pole

    points = np.array([X.flatten(), Y.flatten(), Z.flatten()])

    Euler_Rotation_Matrix = np.array([[np.cos(theta)*np.cos(psi), 
                   -np.cos(phi)*np.sin(psi) + np.sin(phi)*np.sin(theta)*np.cos(psi), 
                        np.sin(phi)*np.sin(psi) + np.cos(phi)*np.sin(theta)*np.cos(psi)],
                        [np.cos(theta)*np.sin(psi), 
                        np.cos(phi)*np.cos(psi) + np.sin(phi)*np.sin(theta)*np.sin(psi),
                        -np.sin(phi)*np.cos(psi) + np.cos(phi)*np.sin(theta)*np.sin(psi)],
                        [-np.sin(theta),
                        np.sin(phi)*np.cos(theta),
                        np.cos(phi)*np.cos(theta)]])
    
    rotated = np.dot(Euler_Rotation_Matrix, points)
    Xrot = rotated[0].reshape(X.shape)
    Yrot = rotated[1].reshape(Y.shape)
    Zrot = rotated[2].reshape(Z.shape)

    r = 6781
    u, v = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
    ax.plot_wireframe(r*np.cos(u)*np.sin(v), r*np.sin(u)*np.sin(v), r*np.cos(v), color="b", lw=0.5, zorder=0)

    ax.plot_wireframe(X, Y, Z, edgecolor='teal', alpha=0.3)
    ax.plot_wireframe(Xrot, Yrot, Zrot, edgecolor='k', alpha=0.3)

    return ax

# fig = plt.figure(figsize=(7,7))
# ax = fig.add_subplot(111,projection='3d')
# star_tracker_plotter(ax, tip_position)