import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

####################################
from STAcc_v2.object_info.read_pdf import StarTracker
from STAcc_v2.analyze.orbit_visualizer import *
####################################

#if 'key' not in st.session_state: 
#    st.session_state.key = 1

st.title("STAcc_v2 Attempt")


# @st.cache_data  # caches the result of the function below, not having to read in the data every time it reloads
if st.checkbox("Upload Stuff"):

    datasheet = st.file_uploader('Upload the datasheet to your chosen commercial star tracker here:', type='pdf', accept_multiple_files=False, label_visibility="visible")
   
    STckr = StarTracker(datasheet="startracker1_datasheet.pdf")
    STckr.extract_text_from_pdf()
    STckr.find_word_in_text()
    STckr.set_parameter_values()
    print(STckr.fov)

    # if datasheet is not None:
    #     import PyPDF2
    #     reader = PyPDF2.PdfReader(datasheet)
    #     number_of_pages = len(reader.pages)

    #     pdf_text = ""

    #     for i in range(number_of_pages):
    #         page = reader.pages[i]
    #         pdf_text += page.extract_text()
    #         pdf_text += "\n"
        
    #     st.write(pdf_text)

    st.write('hi')

#@st.cache_data
if st.checkbox("Get TLE"):

    from spacetrack import SpaceTrackClient

    username = st.text_input("Please type your username for Space-Track.org:")
    password = st.text_input("Please type your password for Space-Track.org:", type='password')

    def download_tle(username=username, password=password, norad_cat_id=[25544, 41335]):
        '''
        Uses spacetrack package to query orbit information about any satellite from space-track.org database
        Downloads TLE as .txt file named 'tle.txt' to working directory
        '''
        id = input("Type the ID of the satellite you would like to track with your star tracker. The default is [25544, 41335].")
        stc = SpaceTrackClient(username, password)
        tle = stc.tle_latest(norad_cat_id=id, ordinal=1, format='tle')
        print(type(tle))
        #with open("tle.txt", "w") as text_file:
            #text_file.write(tle)

    download_tle()
    #open('tle.txt', 'r')

        #show_plot()