from PyPDF2 import PdfReader
import re

class StarTracker:
    def __init__(self, datasheet=None):
        try:
            assert (type(datasheet) == str) | (datasheet == None), "Input the filepath to your datasheet; must be a string."
            self.datasheet = datasheet
        except AssertionError as msg:
            print(msg)
        #try:
            # check if path to file exists
            #self.datasheet = 

    def extract_text_from_pdf(self):
        '''
        TODO: write docstring
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
            word (str): The word to search for in the text
            text (str): The text in which to search for the word
            num_characters (int): The number of characters to extract after each occurrence of the word

        Returns:
            info_set (list): A list of extracted substrings, each containing the word and characters following it
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
                
            index = end_index  # starts looking after the string it just printed

        self.info_set = info_set

        return self.info_set
    
    def input_boolean_converter(self, prompt_message):
        '''
        TODO: docstring
        '''
        while True:
            user_input = input(prompt_message).strip().lower()  # get user's input from prompt message
            
            if user_input == 'yes':
                return True
            elif user_input == 'no':
                return False
            else:
                print("Please enter 'yes' or 'no'.")

    #result = input_boolean_converter("Enter 'yes' or 'no': ")
    #print("You entered:", result)


    def parameter_value(self):
        '''
        TODO: docstring
        '''
        for value in self.info_set:
            
            print(value)
            user_input = self.input_boolean_converter(f'Does this text look like it contains the proper information for a certain parameter? : {value}')
            
            if user_input:  # user_input is True if user entered yes
                float_pattern = r'[-+]?\d*\.\d+|\d+'  # This pattern identifies both integer and floating-point numbers
                float_values = re.findall(float_pattern, value)
                
                if float_values:
                #    float_number = float(float_values[0])  # Convert the first matched value to a float
                    
                    return float_values  # Return the extracted float number
                    
        return "No value can be found. Try inputting your specifications manually."


    def set_parameter_values(self):
        '''
        Define the attributes of the StarTracker class instance through detection from the input datasheet
        or prompt the user to input star tracker parameters.
        
        Args:
            self
            
        Returns: tuple of valid parameter values (integer or floats)
            self.accuracy: accuracy of star tracker (in [units])
            self.fov: field of view of star tracker (in arcseconds)
        '''
        if self.datasheet:
            self.extract_text_from_pdf()

            self.find_word_in_text(word="accuracy")
            if self.info_set == []:
                self.find_word_in_text(word="Accuracy")
                if self.info_set == []:
                    print("Accuracy could not be found in the provided text. Proofread the pdf to ensure it has the aperture information. If not, upload a new pdf. If it does, please input manually.")
            
            self.accuracy = self.parameter_value()
            
            self.find_word_in_text(word="field of view")
            if self.info_set == []:
                self.find_word_in_text(word="Field of View")
                if self.info_set == []:
                    print("Field of view could not be found in the provided text. Proofread the pdf to ensure it has the field of view information. If not, upload a new pdf. If it does, please input manually.")
            
            self.fov = self.parameter_value()

# is this how to do this without pdf??
        if self.datasheet == None:
            prompt_messages = ["Input the accuracy of your startracker in [units]:", "Input the field of view of your startracker in arcseconds"]
            values = []
            
            for prompt in prompt_messages:
                while True:
                    user_input = input(prompt)
                    
                    try:
                        value = float(user_input)  # Try converting input to float
                        if value.is_integer():  # Check if the float is actually an integer
                            value = int(value)  # Convert to int if it's an integer
                        
                        values.append(value)
                        break
                    
                    except ValueError:
                        print("Please enter an integer or float for the value of this parameter, in the units requested.")
            
            self.accuracy, self.fov = values

        return self.accuracy, self.fov