import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

####################################
from STAcc_v2.object_info.StarTracker import StarTracker
from STAcc_v2.object_info.RSO import RSO
from STAcc_v2.analyze.orbit_visualizer import *
####################################

#if 'key' not in st.session_state: 
#    st.session_state.key = 1

st.title("STAcc_v2 Beta Test")

# @st.cache_data  # caches the result of the function below, not having to read in the data every time it reloads
STckr_default = StarTracker(datasheet="startracker1_datasheet.pdf")
STckr_default.set_parameter_values()

if st.checkbox("Upload custom star tracker instead"):
    datasheet = st.file_uploader('Upload the datasheet to your chosen commercial star tracker here, or use the default.', type='pdf', accept_multiple_files=False, label_visibility="visible")
    STckr = StarTracker(datasheet=datasheet)
    STckr.set_parameter_values()
    st.write(STckr.fov)

#@st.cache_data
if st.checkbox("Get TLE"):

    from spacetrack import SpaceTrackClient

    username = st.text_input("Please type your username for Space-Track.org:")
    password = st.text_input("Please type your password for Space-Track.org:", type='password')
    
    Object_default = RSO()
    Object_default.say_hello()
    tle = Object_default.get_tle()
    #st.write(tle)  # works!!

    fig = plt.figure(figsize=(7,7))
    ax = fig.add_subplot(111,projection='3d')

    Object_default.orbit_plotter(ax)
    cone_plotter(ax)

    st.pyplot(fig)

    #Object_default.orbit_plotter()


        #show_plot()