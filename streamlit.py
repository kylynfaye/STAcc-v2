####################################
from STAcc_v2.object_info.StarTracker import StarTracker
from STAcc_v2.object_info.RSO import RSO
from STAcc_v2.analyze.accuracy_math import *
from STAcc_v2.analyze.visualizer import *
####################################

#if 'key' not in st.session_state: 
#    st.session_state.key = 1
st.set_page_config(layout="wide")

st.title("STAcc_v2: a star tracker visualization tool")
st.header("welcome to STAcc_v2, a fresh new streamlit app intended to showcase the capabilities of commercial off-the-shelf star trackers utilized on-orbit")
st.write("Loosely inspired by Eliot Aretskin-Hariton's and Aaron J. Swank's Star Tracker ACCuracy tool from their paper titled 'Star Tracker Performance Estimate with IMU' (2015).")

col1, col2 = st.columns(2)

## This column is for setting up your star tracker.
with col1:
    st.subheader("Start by uploading the PDF datasheet of your star tracker!")
    st.write("Ensure that the PDF lists the star tracker's field of view in degrees.")
    
    stckr_option = st.selectbox(
    'Would you like to use the default option or upload your own star tracker datasheet?',
    ('Default', 'Custom Datasheet'), index=None,
    placeholder="Select an option here...")
    if stckr_option == 'Default':
        STckr_default = StarTracker(datasheet="startracker1_datasheet.pdf")
        STckr_default.set_parameter_values()
        if st.checkbox("Show a preview of the datasheet's text"):
            st.write(STckr_default.datasheet_text[0:300])
    if stckr_option == 'Custom Datasheet':
        datasheet = st.file_uploader('Upload the datasheet to your chosen commercial star tracker here, or use the default.', type='pdf', accept_multiple_files=False, label_visibility="visible")
        STckr = StarTracker(datasheet=datasheet)
        STckr.set_parameter_values()
        if st.checkbox("Show a preview of the datasheet's text"):
            st.write(STckr.fov)
            st.write(STckr.datasheet_text[0:300])

if stckr_option != None:
    ## This column is for setting up your resident space object (RSO).
    with col2:
        st.subheader("Next, select an RSO (resident space object) to track!")
        st.write("The default object is the International Space Station, with a NORAD CAT ID of 25544. Utilize the default or select your own!")
        st.link_button("Click here to browse available NORAD IDs", "https://in-the-sky.org/search.php?s=&searchtype=Spacecraft&satorder=0", help=None)
        
        rso_option = st.selectbox('Would you like to use the default option or input your own RSO ID?',
        ('Default', 'Custom ID'), index=None, placeholder="Select an option here...")

        if rso_option == 'Default':
            id = 25544
        if rso_option == 'Custom ID':
            id = st.text_input("Type the NORAD CAT ID of your favorite satellite here...")


        from spacetrack import SpaceTrackClient
        username = st.text_input("Please type your username for Space-Track.org:")
        password = st.text_input("Please type your password for Space-Track.org:", type='password')
        

        st.write("While your plot loads, customize your satellite!")
        ## The following features are simply to make prettier visualizations!
        name_RSO = st.text_input("Input a name for your RSO here:")
        if name_RSO == "":
            name_RSO = "Noah"
        RSO_color = st.color_picker("Choose a color for your RSO's orbit:", value="#2de0ae")

        ## Initializing the RSO with your info:
        Object = RSO(username, password, name=name_RSO, norad_cat_id=id)
        Object.say_hello()

        st.write("In order to produce the orbit below, this package uses what's known as a Two-Line Element set (or TLE).\
                 This object contains data on a satellite's orbital position (including apogee, perigee, etc.) using regularly-updated info from Space-Track.")
        if st.checkbox(f"Display {name_RSO}'s TLE (warning: not easy for humans to digest)"):
            tle = Object.get_tle()
            st.write(tle)




    st.sidebar.title("Customize your visualization here!")
    st.sidebar.subheader("Place the star tracker in a new location around the Earth, while keeping its FOV oriented upwards.")
    xpos = st.sidebar.slider("X Position of Star Tracker", -7000,7000, 0)
    ypos = st.sidebar.slider("Y Position of Star Tracker", -7000,7000, 0)
    zpos = st.sidebar.slider("Z Position of Star Tracker", -7000,8000, 6981)

    st.sidebar.subheader("Adjust the distance outwards the star tracker view cone extends in the visualization.")
    reach = st.sidebar.slider("Height of Star Tracker View Cone", 1000,5000, 1500)

    st.sidebar.subheader("Rotate the star tracker around the Earth at varying angles.")
    xrot = st.sidebar.slider("Rotate Star Tracker Around x-Axis (in rad)", 0.0,2*np.pi, 0.0)
    yrot = st.sidebar.slider("Rotate Star Tracker Around y-Axis (in rad)", 0.0,2*np.pi, 0.0)
    zrot = st.sidebar.slider("Rotate Star Tracker Around z-Axis (in rad)", 0.0,2*np.pi, 0.0)

    st.sidebar.subheader("Rotate the view of the plot.")
    azim = st.sidebar.slider("Azimuth", 0,90, 45)
    elev = st.sidebar.slider("Elevation", 0,90, 10)



    fig = plt.figure(figsize=(6,6))
    ax = fig.add_subplot(111,projection='3d')
    ax = earth_plotter(ax)

    x, y, z = Object.orbit_coords()
    ax = orbit_plotter(ax, x, y, z, color=RSO_color, azim=azim, elev=elev)

    try:
        STckr_default
        Xrot, Yrot, Zrot = STckr_default.fov_frame(tip_position=(xpos, ypos, zpos), height=reach, theta=xrot, phi=yrot, psi=zrot)
        STckr_color = range_calculator(x, y, z, Xrot, Yrot, Zrot)

        ax = fov_plotter(ax, Xrot, Yrot, Zrot, color=STckr_color)
        ax
    except NameError:
        st.write("Not using the default star tracker.")

    try:
        STckr
        Xrot, Yrot, Zrot = STckr.fov_frame(tip_position=(xpos, ypos, zpos), height=reach, theta=xrot, phi=yrot, psi=zrot)
        STckr_color = range_calculator(x, y, z, Xrot, Yrot, Zrot)

        ax = fov_plotter(ax, Xrot, Yrot, Zrot, color=STckr_color)
        ax
    except NameError:
        st.write("The following image includes the *default* star tracker's FOV cone.")

    st.write("The star tracker's FOV cone shows up as red if the satellite does not pass within the field during some part of its orbit. \
             Try adjusting the parameters on the sidebar to relocate your star tracker in order to observe the RSO! If done successfully, \
             the cone will appear green. As an additional tip, try rotating the perspective on the image with the sliders 'Elevation' and 'Azimuth' to get a better angle.")

    st.pyplot(fig)