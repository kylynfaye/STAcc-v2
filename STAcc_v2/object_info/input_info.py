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
            