from httpx import HTTPStatusError
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

import datetime as dt
import math as m
from spacetrack import SpaceTrackClient

class RSO:
    def __init__(self, username, password, name="Noah", color='red', norad_cat_id=25544):
        '''
        Initalize a resident space object using either the default ID or one input from the user.

        Args:
            self
            username (str): your username for Space-Track.org
            password (str): your password for Space-Track.org
            name (str): a fun name for your RSO
            color (str): a fun color for your RSO's orbit path
            norad_cat_id (str): a number indicating your RSO's ID in the catalogue

        Attributes:
            These should be self-explanatory.
        '''
        self.username = username
        self.password = password
        self.color = color
        self.name = name
        self.id = norad_cat_id

    def get_tle(self):
        '''
        Uses spacetrack package to query orbit information about any satellite from space-track.org database.
        Outputs tle specs in the required format for use by other methods within the class.

        Args:
            self

        Returns:
            processed_tle (str): a string with TLE information carefully edited to be utilized
                by the following functions for plotting (shoutout to Sebastian for help on this)
        '''

        stc = SpaceTrackClient(self.username, self.password)
        tle = stc.tle_latest(norad_cat_id=self.id, ordinal=1, format='tle')
        unprocessed_tle = tle.split("\n")[0:-1]
        processed_tle = []
        for i in unprocessed_tle:
            processed_tle.append(i+"\n")
        
        return processed_tle

        # In future edits, this function can be expanded to allow for users to edit
        # not only the star tracker's specs but the chosen RSO's TLE to a theoretical one.
        #######################

    def say_hello(self):
        '''
        A cute lil function to greet the user.
        It also serves to check that input IDs and names are being utilized.

        Args:
            self
        '''
        st.subheader(f'Hi, I am your RSO named {self.name}! My NORAD CAT ID is {self.id}.')

    def orbit_coords(self):
        '''
        Adapted from https://python.plainenglish.io/plot-satellites-real-time-orbits-with-python-s-matplotlib-3c7ccd737638
        Plots the orbit of a satellite from its TLE information, which must be processed as seen above.

        Args:
            self

        Returns:
            x, y, z (lists): basic position information for the satellite's at each step throughout its orbit
        '''
        data = self.get_tle()

        mu = 398600.4418  # Earth’s standard gravitational parameter
        D = 24*0.997269  # amount of hours in a sideral day

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
            P = np.matmul(R,np.array([[orb["a"]*m.cos(i)],[orb["b"]*m.sin(i)],[0]]))\
                -np.matmul(R,np.array([[orb["c"]],[0],[0]]))
            x += [P[0]]
            y += [P[1]]
            z += [P[2]]

        plt.title(f'Orbit of {self.name} (NORAD ID = {self.id}) as of {orb["t"].strftime("%m / %Y")}')

        return x, y, z