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
if st.checkbox("Wanna make a startracker? Click here to use the default"):
    STckr_default = StarTracker(datasheet="startracker1_datasheet.pdf")
    STckr_default.set_parameter_values()
if st.checkbox("Upload custom star tracker datasheet instead"):
    datasheet = st.file_uploader('Upload the datasheet to your chosen commercial star tracker here, or use the default.', type='pdf', accept_multiple_files=False, label_visibility="visible")
    STckr = StarTracker(datasheet=datasheet)
    STckr.set_parameter_values()


#@st.cache_data
if st.checkbox("Get TLE"):
    from spacetrack import SpaceTrackClient

    username = st.text_input("Please type your username for Space-Track.org:")
    password = st.text_input("Please type your password for Space-Track.org:", type='password')
    
    if st.checkbox("Give your satellite a name!"):
        name_RSO = st.text_input("Input name here:")
    else:
        name_RSO = "Noah"
    
    Object_default = RSO(username, password)
    Object_default.say_hello(name=name_RSO)

    tle = Object_default.get_tle()
    #st.write(tle)  # works!!

    fig = plt.figure(figsize=(7,7))
    ax = fig.add_subplot(111,projection='3d')

    Object_default.orbit_plotter(ax, elev=10)

    xpos = st.sidebar.slider("X Position of Star Tracker", 0,100, 0)
    ypos = st.sidebar.slider("Y Position of Star Tracker", 0,100, 0)
    zpos = st.sidebar.slider("Z Position of Star Tracker", 0,1000, 200)

    reach = st.sidebar.slider("Height of Star Tracker View Cone", 1000,5000, 1500)
    
    xrot = st.sidebar.slider("Rotate Star Tracker Around x-Axis (in rad)", 0.0,2*np.pi, 0.0)
    yrot = st.sidebar.slider("Rotate Star Tracker Around y-Axis (in rad)", 0.0,2*np.pi, 0.0)
    zrot = st.sidebar.slider("Rotate Star Tracker Around z-Axis (in rad)", 0.0,2*np.pi, 0.0)

    try:
        STckr_default == None
        STckr_default.fov_plotter(ax, tip_position=(xpos, ypos, zpos), height=reach, theta=xrot, phi=yrot, psi=zrot)
    except NameError:
        st.write("Not using the default star tracker.")
    try:
        STckr == None
        STckr.fov_plotter(ax, tip_position=(xpos, ypos, zpos), height=reach, theta=xrot, phi=yrot, psi=zrot)
    except NameError:
        st.write("Try using the default star tracker.")

    st.pyplot(fig)