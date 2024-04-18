from spacetrack import SpaceTrackClient
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
import math as m

class RSO:
    def __init__(self, name="Noah", color='red'):
        # self.mag = magnitude
        # self.xpos, self.ypos, self.zpos = x_pos, y_pos, z_pos
        self.name = name
        self.color = color

    def say_hello(self):
        print(f'Hi, I am your RSO named {self.name}!')

    def get_tle(self, username='kylyn.smith@yale.edu', password='kFs29ceil80*!*!', norad_cat_id=[25544, 41335]):
        '''
        Uses spacetrack package to query orbit information about any satellite from space-track.org database
        Outputs tle specs in required format for use by other methods within the class
        '''
        #id = input("Type the ID of the satellite you would like to track with your star tracker. The default is [25544, 41335].")
        stc = SpaceTrackClient(username, password)
        tle = stc.tle_latest(norad_cat_id=norad_cat_id, ordinal=1, format='tle')

        unprocessed_tle = tle.split("\n")[0:-1]
        processed_tle = []
        for i in unprocessed_tle:
            processed_tle.append(i+"\n")

        return processed_tle
        #In future edits, this function will be expanded to allow for users to edit
        #not only the star tracker's specs but the chosen RSO's too.
        #######################

    def orbit_plotter(self, ax):
        '''
        TODO: write docstring

        Adapted from https://python.plainenglish.io/plot-satellites-real-time-orbits-with-python-s-matplotlib-3c7ccd737638
        Plots the orbit of a satellite from its TLE information, which must be processed as seen above.
        Takes in an axis object and plots the Earth, an orbit, and the star tracker onto it.
        '''
        data = self.get_tle()

        # values for Earth:
            # mu is earth’s standard gravitational parameter
            # r is earth’s radius in km
            # D is the amount of hours in a sideral day
        mu = 398600.4418
        r = 6781
        D = 24*0.997269

        # first, we add the Earth to the plot:
        u, v = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
        ax.plot_wireframe(r*np.cos(u)*np.sin(v), r*np.sin(u)*np.sin(v), r*np.cos(v), color="b", lw=0.5, zorder=0)
        
        # this segment extracts and stores the data found in the satellite's TLE
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

        # R is a rotation matrix built from three rotations, based on orbital positioning data from the TLE
        R = np.matmul(np.array([[m.cos(orb["RAAN"]),-m.sin(orb["RAAN"]),0],[m.sin(orb["RAAN"]),m.cos(orb["RAAN"]),0],[0,0,1]]),(np.array([[1,0,0],[0,m.cos(orb["i"]),-m.sin(orb["i"])],[0,m.sin(orb["i"]),m.cos(orb["i"])]])))
        R = np.matmul(R,np.array([[m.cos(orb["omega"]),-m.sin(orb["omega"]),0],[m.sin(orb["omega"]),m.cos(orb["omega"]),0],[0,0,1]]))
        
        # then, this loops through the parametric orbit and computes the x, y, z positions at each stage
        x,y,z = [],[],[]
        for i in np.linspace(0,2*m.pi,100):
            P = np.matmul(R,np.array([[orb["a"]*m.cos(i)],[orb["b"]*m.sin(i)],[0]]))-np.matmul(R,np.array([[orb["c"]],[0],[0]]))
            x += [P[0]]
            y += [P[1]]
            z += [P[2]]
            ax.plot(x,y,z,zorder=5,color='r')


        plt.title("Orbit of this RSO [var_name?] as of "+orb["t"].strftime("%m %Y"))
        
        ax.set_xlabel("X-axis (km)")
        ax.set_ylabel("Y-axis (km)")
        ax.set_zlabel("Z-axis (km)")

        ax.xaxis.set_tick_params(labelsize=7)
        ax.yaxis.set_tick_params(labelsize=7)
        ax.zaxis.set_tick_params(labelsize=7)
        ax.set_aspect('equal', adjustable='box')

        return ax