import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import datetime as dt
import math as m

def cone_plotter(ax, radius=50, height=750, tip_position=(0,0,7000), azim=45, elev=20):
    '''
    TODO: include variables for thetap, psi, phi for rotations when implementing that
    TODO: convert radius/height variables to field of view from StarTracker class using some trig identity
    '''

    a, b, c = tip_position
    theta = np.linspace(0,2*np.pi,60)
    r = np.linspace(0,radius,50)
    T, R = np.meshgrid(theta, r)

    X = R * np.cos(T) + a
    Y = R * np.sin(T) + b
    Z = (np.sqrt((X-a)**2 + (Y-b)**2)/(radius/height)) + c

    ax.plot_wireframe(X, Y, Z, color='g')
    ax.set_zlim(-7500,7500)
    # ax.set_ylim(-10000,10000)
    # ax.set_xlim(-10000,10000)
    ax.view_init(azim=azim, elev=elev)

    return ax

from 

def show_plot():
    '''
    Function to plot everything at once,
    takes any optional args or uses the functions' respective defaults
    '''
    fig = plt.figure(figsize=(7,7))
    ax = fig.add_subplot(111,projection='3d')
    ax = orbit_plotter(ax, filepath='tle.txt')
    cone_plotter(ax, radius=50, height=750, tip_position=(0,0,7000), azim=45, elev=20)

    plt.show()
