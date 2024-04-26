import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

from PyPDF2 import PdfReader
import re

class StarTracker:
    def __init__(self, datasheet='startracker1_datasheet.pdf'):
        '''
        Initalize a StarTracker object using either the default PDF or one input from the user.

        Args:
            self
            datasheet (str): The filepath for your intended star tracker datasheet

        Attributes:
            self.datasheet = The filepath for your intended star tracker datasheet
                (forced to be a string or uploaded Streamlit file type, otherwise uses default)
        '''
        try:
            assert (type(datasheet) == str) | (str(type(datasheet)) == "<class 'streamlit.runtime.uploaded_file_manager.UploadedFile'>"), "Input the filepath to your datasheet; must be a string."
            self.datasheet = datasheet
        except AssertionError as msg:
            self.datasheet = 'startracker1_datasheet.pdf'

    def extract_text_from_pdf(self):
        '''
        Reads all of the text in the datasheet pdf into one long string of searchable characters.
        
        Args:
            self

        Returns/Attributes:
            self.datasheet_text (str): A long string of all the pdf text
        '''
        reader = PdfReader(self.datasheet)
        number_of_pages = len(reader.pages)

        pdf_text = ""

        for i in range(number_of_pages):
            page = reader.pages[i]
            pdf_text += page.extract_text()
            pdf_text += "\n"
        
        self.datasheet_text = pdf_text

        return self.datasheet_text

    def find_word_in_text(self, word, num_characters=15):
        '''
        Find occurrences of a word in a text, then return the word and a defined number of characters 
        following each occurrence.

        Args:
            self
            word (str): The word to search for in the text
            num_characters (int): The number of characters to extract after each occurrence of the word

        Returns/Attributes:
            self.info_set (list): A list of extracted substrings, each containing the word and characters following it
        '''
        info_set = []
        index = 0
        text = self.datasheet_text
        
        while index < len(text):
            found_index = text.find(word, index)  # Looks for a certain substring (word) within a longer string named text
            if found_index == -1:
                break
            
            start_index = found_index + len(word)
            end_index = start_index + num_characters  # num_characters defines how many characters after the word it will look through/present to user
            possible_info = text[start_index-len(word):end_index]  # prints the word you're looking for and the characters after it
            info_set.append(possible_info)  # adds this result to a list
                
            index = end_index  # restarts seraching through the characters following the string it just printed

        self.info_set = info_set

        return self.info_set
    
    def parameter_value(self):
        '''
        From a given set of strings (it's possible that the datasheet listed the words "field of view" multiple times),
        extract the field of view using a regular expression pattern and assign to the attribute self.fov.
        If only one number for the FOV exists, it sets the cone to be circular rather than elliptical.
        
        Args:
            self

        Returns:
            float_values (list): The integers/floats for field of view of the cone in two distinct directions.
        '''
        for value in self.info_set:
            
            st.write(f"Does this text excerpt look like it contains the star tracker's field of view? : {value}")
            
            if 'clicked' not in st.session_state:
                st.session_state.clicked = False

            def click_button():
                st.session_state.clicked = True

            st.button('Yes', on_click=click_button)

            if st.session_state.clicked:
                float_pattern = r'[-+]?\d*\.\d+|\d+'  # This pattern identifies both integer and floating-point numbers
                float_values = re.findall(float_pattern, value)
                
                if float_values:
                    if len(float_values) == 1:                    
                        return float_values*2 # assumes the same degree FOV in both directions if only one number given
                    if len(float_values) == 2:                    
                        return float_values
            if st.button('No'):   
                st.write("No value can be found. Try using the default tracker.")
                return None

    def set_parameter_values(self):
        '''
        Define the attributes of the StarTracker class instance through detection from the input datasheet
        or prompt the user to input star tracker parameters. Basically, this does all of the above functions
        in one step, reducing the number of calls I have to make in streamlit.
        
        Args:
            self
            
        Returns:
            self.fov: field of view of star tracker (in degrees)
        '''
        if self.datasheet:
            self.extract_text_from_pdf()

            # self.find_word_in_text(word="Accuracy")
            # if self.info_set == []:
            #     self.find_word_in_text(word="accuracy")
            #     if self.info_set == []:
            #         st.write("Accuracy could not be found in the provided text. Proofread the pdf to ensure it has the aperture information. If not, upload a new pdf. If it does, please input manually.")
            
            # self.accuracy = self.parameter_value()
            
            self.find_word_in_text(word="Field of View")
            if self.info_set == []:
                self.find_word_in_text(word="Field of view")
                if self.info_set == []:
                    st.write("Field of view could not be found in the provided text. \
                             Proofread the pdf to ensure it has the field of view information. \
                             If not, upload a new pdf. If it does, please input manually.")
            
            self.fov = self.parameter_value()


        if self.datasheet == None:
            #prompt_messages = ["Input the accuracy of your startracker in [units]:", "Input the field of view of your startracker in arcseconds"]
            prompt_messages = ["Input the field of view of your startracker in arcseconds:"]
            values = []
            
            for prompt in prompt_messages:
                while True:
                    user_input = st.text_input(prompt)
                    
                    try:
                        value = float(user_input)  # Try converting input to float
                        if value.is_integer():  # Check if the float is actually an integer
                            value = int(value)  # Convert to int if it's an integer
                        
                        values.append(value)
                        break
                    
                    except ValueError:
                        st.write("Please enter an integer or float for the value of this parameter, in the units requested.")

            self.fov = values

        return self.fov
    
    def fov_frame(self, tip_position=(0,0,0), height=3000, theta=10, phi=60, psi=0):
        '''
        Sets up a meshgrid to define the star tracker's FOV in an oblong cone shape (meaning the cone
        can have two different dimensions).

        Args:
            self
            tip_position (tuple of 3 floats/ints): defines the (x,y,z) positions of the point of the cone/
                the star tracker's actual location
            height (float): the distance outwards that the cone reaches/height of the plotted cone
            theta (float): the rotating angle away from the z axis
            phi (float): the rotating angle away from the y axis
            psi (float): the rotating angle away from the x axis

        Returns:
            Xrot, Yrot, Zrot (meshgrids): the necessary objects with position information to build an ax.plot_wireframe in 3 dimensions
        '''
        a, b, c = tip_position
 
        num_points = 50
        thetap = np.linspace(0, 2*np.pi, num_points)  # goes around azimuthal angle/z-axis
        z = np.linspace(0, height, num_points)  # makes a bunch of z values between 0 and the height

        T, Z = np.meshgrid(thetap, z)

        major_radius = height*np.tan(float(self.fov[0])/2)
        minor_radius = height*np.tan(float(self.fov[1])/2)

        majradius = major_radius * (1 - Z / height)
        minradius = minor_radius * (1 - Z / height)  # these both define the maximum size to which the large part of the cone extends

        X = majradius * np.cos(T) + a
        Y = minradius * np.sin(T) + b
        Z = -Z + c + height  # just orients the cone to start at the north pole

        points = np.array([X.flatten(), Y.flatten(), Z.flatten()])

        Euler_Rotation_Matrix = np.array([[np.cos(theta)*np.cos(psi), 
                    -np.cos(phi)*np.sin(psi) + np.sin(phi)*np.sin(theta)*np.cos(psi), 
                            np.sin(phi)*np.sin(psi) + np.cos(phi)*np.sin(theta)*np.cos(psi)],
                            [np.cos(theta)*np.sin(psi), 
                            np.cos(phi)*np.cos(psi) + np.sin(phi)*np.sin(theta)*np.sin(psi),
                            -np.sin(phi)*np.cos(psi) + np.cos(phi)*np.sin(theta)*np.sin(psi)],
                            [-np.sin(theta),
                            np.sin(phi)*np.cos(theta),
                            np.cos(phi)*np.cos(theta)]])
        
        # This rotation matrix can be applied to the set of X/Y/Z meshgrid points
        # in order to rotate the star tracker around Earth as follows:

        rotated = np.dot(Euler_Rotation_Matrix, points)
        Xrot = rotated[0].reshape(X.shape)
        Yrot = rotated[1].reshape(Y.shape)
        Zrot = rotated[2].reshape(Z.shape)

        return Xrot, Yrot, Zrot
    