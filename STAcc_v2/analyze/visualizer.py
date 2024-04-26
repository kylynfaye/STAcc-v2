import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

import datetime as dt
import math as m
from mpl_toolkits.mplot3d import Axes3D

def earth_plotter(ax):
    '''
    Plots the Earth, to-scale, in a 3D matplotlib figure.

    Args:
        ax (Axes object): takes in a set of axes onto which to plot the Earth

    Args:
        ax (Axes object): outputs the set of axes with the Earth now overlaid
    '''
    r = 6781
    u, v = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
    ax.plot_wireframe(r*np.cos(u)*np.sin(v), r*np.sin(u)*np.sin(v), r*np.cos(v), color='cornflowerblue', lw=0.5, zorder=0)
    return ax

def fov_plotter(ax, Xrot, Yrot, Zrot, color):
    '''
    Plots the field of view cone of the star tracker, to-scale, in a 3D matplotlib figure.

    Args:
        ax (Axes object): takes in a set of axes onto which to plot the FOV cone

    Args:
        ax (Axes object): outputs the set of axes with the cone now overlaid
    '''
    r = 6781
    u, v = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
    ax.plot_wireframe(r*np.cos(u)*np.sin(v), r*np.sin(u)*np.sin(v), r*np.cos(v), color="b", lw=0.5, zorder=0)

    ax.plot_wireframe(Xrot, Yrot, Zrot, edgecolor=color, alpha=0.08)

    return ax


def orbit_plotter(ax, x, y, z, color='red', azim=45, elev=10):
    '''
    Plots the orbit of the RSO, to-scale, in a 3D matplotlib figure.

    Args:
        ax (Axes object): takes in a set of axes onto which to plot the RSO

    Args:
        ax (Axes object): outputs the set of axes with the RSO's orbit path now overlaid
    '''
    ax.plot(x,y,z, zorder=5, color=color, alpha=0.75)
        
    ax.set_xlabel("X-axis (km)")
    ax.set_ylabel("Y-axis (km)")
    ax.set_zlabel("Z-axis (km)")

    ax.set_zlim(-7500,7500)
    ax.set_ylim(-10000,10000)
    ax.set_xlim(-10000,10000)

    ax.view_init(azim=azim, elev=elev)

    ax.xaxis.set_tick_params(labelsize=7)
    ax.yaxis.set_tick_params(labelsize=7)
    ax.zaxis.set_tick_params(labelsize=7)

    return ax