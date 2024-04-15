import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
#from os.path import join
#import pathlib

####################################
#from analyze import orbit_visualizer
####################################

#if 'key' not in st.session_state: 
#    st.session_state.key = 1

st.title("STAcc_v2 Attempt")

#parent_path = pathlib.Path(__file__).parent.parent.resolve()
#data_path = os.path.join(parent_path, "data")


# @st.cache_data  # caches the result of the function below, not having to read in the data every time it reloads
if st.checkbox("Upload Stuff"):
    datasheet = st.file_uploader('Upload the datasheet to your chosen commercial star tracker here:', type='pdf', accept_multiple_files=False, label_visibility="visible")
   

    #extract_text_from_pdf(datasheet) # matching this with my StarTracker class read_pdf from object_info?

    if datasheet is not None:
        import PyPDF2
        reader = PyPDF2.PdfReader(datasheet)
        number_of_pages = len(reader.pages)

        pdf_text = ""

        for i in range(number_of_pages):
            page = reader.pages[i]
            pdf_text += page.extract_text()
            pdf_text += "\n"
        
        st.write(pdf_text)

    st.write('hi')


from spacetrack import SpaceTrackClient

def download_tle(username='kylyn.smith@yale.edu', password='kFs29ceil80*!*!', norad_cat_id=[25544, 41335]):
    '''
    Uses spacetrack package to query orbit information about any satellite from space-track.org database
    Downloads TLE as .txt file named 'tle.txt' to working directory
    '''
    stc = SpaceTrackClient(username, password)
    tle = stc.tle_latest(norad_cat_id=norad_cat_id, ordinal=1, format='tle')
    with open("tle.txt", "w") as text_file:
        text_file.write(tle)

    download_tle()

    #show_plot()