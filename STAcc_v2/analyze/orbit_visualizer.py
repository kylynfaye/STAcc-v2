import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.linalg import norm


def cone_plotter(radius=500, height=5000, tip_position=(0,0,6781), azim=45, elev=20):
    '''
    Include variables for thetap, psi, phi for rotations when implementing that
    '''
    fig = plt.figure()
    ax = fig.add_subplot(111,projection='3d')

    a, b, c = tip_position
    #choose=max(radius,height)

    theta = np.linspace(0,2*np.pi,60)
    r = np.linspace(0,radius,50)
    T, R = np.meshgrid(theta, r)

    X = R * np.cos(T) + a
    Y = R * np.sin(T) + b
    Z = (np.sqrt((X-a)**2 + (Y-b)**2)/(radius/height)) + c

    # Z[Z < 0] = np.nan
    # Z[Z > 2000] = np.nan

    #ERot = np.array([[np.cos(thetap)*np.cos(psi), 
                #        -np.cos(phi)*np.sin(psi) + np.sin(phi)*np.sin(thetap)*np.cos(psi), 
                 #       np.sin(phi)*np.sin(psi) + np.cos(phi)*np.sin(thetap)*np.cos(psi)],
                 #       [np.cos(thetap)*np.sin(psi), 
                 #       np.cos(phi)*np.cos(psi) + np.sin(phi)*np.sin(thetap)*np.sin(psi),
                 #       -np.sin(phi)*np.cos(psi) + np.cos(phi)*np.sin(thetap)*np.sin(psi)],
                 #       [-np.sin(thetap),
                 #       np.sin(phi)*np.cos(thetap),
                 #       np.cos(phi)*np.cos(thetap)]])
    
    #xp, yp, zp = ERot.dot(np.vstack([X,Y,Z]))


    #from scipy.spatial.transform import Rotation as R
    #Rotation Scipy Docs: https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.transform.Rotation.html
    #r = R.from_euler('zyx', [90, 45, 30], degrees=True)
    #xp,yp,zp = np.dot(r.as_matrix(),[X,Y,Z])
    #ax.plot_wireframe(xp,yp,zp)

    ax.plot_wireframe(X, Y, Z, color='g')
    ax.set_zlim(-10000,10000)
    ax.set_ylim(-10000,10000)
    ax.set_xlim(-10000,10000)
    ax.view_init(azim=azim, elev=elev)

    return fig, ax


import datetime as dt
import math as m
from spacetrack import SpaceTrackClient

def download_tle():
    '''
    Queries orbit information about any satellite from space-track.org database
    Downloads TLE as .txt file
    '''
    stc = SpaceTrackClient('kylyn.smith@yale.edu', 'kFs29ceil80*!*!')
    tle = stc.tle_latest(norad_cat_id=[25544, 41335], ordinal=1, format='tle')
    with open("tle.txt", "w") as text_file:
        text_file.write(tle)

def orbit_plotter():
    '''
    Adapted from https://python.plainenglish.io/plot-satellites-real-time-orbits-with-python-s-matplotlib-3c7ccd737638
    Plots the orbit of a satellite from its TLE file, which must be downloaded
    and in the working directory.
    '''
    ADDR = 'tle.txt'
    data = open(ADDR,"r").readlines()

    # values for Earth:
        # mu is earth’s standard gravitational parameter
        # r is earth’s radius
        # D is the amount of hours in a sideral day
    mu = 398600.4418
    r = 6781
    D = 24*0.997269

    fig = plt.figure()
    ax = plt.axes(projection='3d',computed_zorder=False)
    for i in range(len(data)//2):
        if data[i*2][0] != "1":
            print("Wrong TLE format at line "+str(i*2)+". Lines ignored.")
            continue
        if int(data[i*2][18:20]) > int(dt.date.today().year%100):
            orb = {"t":dt.datetime.strptime("19"+data[i*2][18:20]+" "+data[i*2][20:23]+" "+str(int(24*float(data[i*2][23:33])//1))+" "+str(int(((24*float(data[i*2][23:33])%1)*60)//1))+" "+str(int((((24*float(data[i*2][23:33])%1)*60)%1)//1)), "%Y %j %H %M %S")}
        else:
            orb = {"t":dt.datetime.strptime("20"+data[i*2][18:20]+" "+data[i*2][20:23]+" "+str(int(24*float(data[i*2][23:33])//1))+" "+str(int(((24*float(data[i*2][23:33])%1)*60)//1))+" "+str(int((((24*float(data[i*2][23:33])%1)*60)%1)//1)), "%Y %j %H %M %S")}
        orb.update({"name":data[i*2+1][2:7],"e":float("."+data[i*2+1][26:34]),"a":(mu/((2*m.pi*float(data[i*2+1][52:63])/(D*3600))**2))**(1./3),"i":float(data[i*2+1][9:17])*m.pi/180,"RAAN":float(data[i*2+1][17:26])*m.pi/180,"omega":float(data[i*2+1][34:43])*m.pi/180})
        orb.update({"b":orb["a"]*m.sqrt(1-orb["e"]**2),"c":orb["a"]*orb["e"]})

    # R is our rotation matrix built from three rotations
    R = np.matmul(np.array([[m.cos(orb["RAAN"]),-m.sin(orb["RAAN"]),0],[m.sin(orb["RAAN"]),m.cos(orb["RAAN"]),0],[0,0,1]]),(np.array([[1,0,0],[0,m.cos(orb["i"]),-m.sin(orb["i"])],[0,m.sin(orb["i"]),m.cos(orb["i"])]])))
    R = np.matmul(R,np.array([[m.cos(orb["omega"]),-m.sin(orb["omega"]),0],[m.sin(orb["omega"]),m.cos(orb["omega"]),0],[0,0,1]]))
    x,y,z = [],[],[]
    # we loop through the parametric orbit and compute the positions' x, y, z
    for i in np.linspace(0,2*m.pi,100):
        P = np.matmul(R,np.array([[orb["a"]*m.cos(i)],[orb["b"]*m.sin(i)],[0]]))-np.matmul(R,np.array([[orb["c"]],[0],[0]]))
        x += [P[0]]
        y += [P[1]]
        z += [P[2]]
        #we plot the orbits in the for loop
        ax.plot(x,y,z,zorder=5)

    #then we plot the earth
    u, v = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
    ax.plot_wireframe(r*np.cos(u)*np.sin(v),r*np.sin(u)*np.sin(v),r*np.cos(v),color="b",alpha=0.5,lw=0.5,zorder=0)
    
    plt.title("Orbit of this RSO [var_name?] as of "+orb["t"].strftime("%m %Y"))
    
    ax.set_xlabel("X-axis (km)")
    ax.set_ylabel("Y-axis (km)")
    ax.set_zlabel("Z-axis (km)")

    ax.xaxis.set_tick_params(labelsize=7)
    ax.yaxis.set_tick_params(labelsize=7)
    ax.zaxis.set_tick_params(labelsize=7)
    ax.set_aspect('equal', adjustable='box')

    return fig, ax