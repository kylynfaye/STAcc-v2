import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
#from os.path import join
#import pathlib

from analyze import orbit_visualizer

#if 'key' not in st.session_state: 
#    st.session_state.key = 1

st.title("STAcc_v2 Attempt")

#parent_path = pathlib.Path(__file__).parent.parent.resolve()
#data_path = os.path.join(parent_path, "data")


# @st.cache_data  # caches the result of the function below, not having to read in the data every time it reloads
if st.checkbox("Upload Stuff"):
    datasheet = st.file_uploader('Upload the datasheet to your chosen commercial star tracker here.', type='pdf', accept_multiple_files=False, label_visibility="visible")
   

    extract_text_from_pdf(datasheet) # matching this with my StarTracker class read_pdf from object_info?


    st.write('hi')



    #show_plot()