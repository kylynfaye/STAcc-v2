from PyPDF2 import PdfReader
import re


def extract_text_from_pdf(file_path: str):
    '''
    TODO: write docstring
    '''
    reader = PdfReader(file_path)
    number_of_pages = len(reader.pages)

    pdf_text = ""

    for i in range(number_of_pages):
        page = reader.pages[i]
        pdf_text += page.extract_text()
        pdf_text += "\n"

    return pdf_text


def find_word_in_text(word, text: str, num_characters=15):
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
    
    while index < len(text):
        found_index = text.find(word, index)  # Looks for a certain substring (word) within a longer string named text
        if found_index == -1:
            break
        
        start_index = found_index + len(word)
        end_index = start_index + num_characters  # num_characters defines how many characters after the word it will look through/present to user
        possible_info = text[start_index-len(word):end_index]  # prints the word you're looking for and the characters after it
        info_set.append(possible_info)  # adds this result to a list
        
        index = end_index  # starts looking after the string it just printed

    if info_set == []:
        info_set = "No occurences of this word could be found in the provided text. Try checking your capitalization."
    
    return info_set


def input_boolean_converter(prompt_message):
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


def parameter_value(info_set: list):
    '''
    TODO: docstring
    '''
    for value in info_set:
        
        print(value)
        user_input = input_boolean_converter("Does this text look like it contains the proper value for your chosen parameter?")
        
        if user_input:  # user_input is True if user entered yes
            float_pattern = r'[-+]?\d*\.\d+|\d+'  # This pattern identifies both integer and floating-point numbers
            float_values = re.findall(float_pattern, value)
            
            if float_values:
                float_number = float(float_values[0])  # Convert the first matched value to a float
                
                return float_number  # Return the extracted float number
                
    return "No value was found. Try inputting your specifications manually."


def input_parameter_values(prompt_messages):
    '''
    Prompt the user for star tracker parameters from given prompts.
    
    Args:
        prompt_messages (list of str): List of prompts for user input.
        
    Returns:
        list: List of valid parameter values (integers or floats).
    '''
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
    
    return values
        