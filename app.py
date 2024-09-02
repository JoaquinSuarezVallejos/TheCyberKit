# PYTHON FILE
# Case types used: snake_case (for functions and variables) and SCREAMING_SNAKE_CASE (for constants)

# Setup for Windows (use PowerShell or the VS Code terminal): 
# 1. Clone the repository from GitHub: git clone https://github.com/JoaquinSuarezVallejos/TheCyberKit.git
# 2. Navigate to the project directory: cd "C:\Users...TheCyberKit" (your directory)
# 3. Create the Flask virtual environment: python -m venv flask_env
# 4. Activate the virtual environment: flask_env\Scripts\activate
# 5. Install dependencies from the requirements.txt file: pip install -r requirements.txt

# Commands to serve Flask project: 1. flask_env\Scripts\activate | 2. python app.py (or python3 app.py)
"""
from flask import Flask, render_template

app = Flask(__name__, static_folder='static', static_url_path='/static')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
"""    
# TODO: Start developing here.

import random
import string

def generate_password(length, use_uppercase, use_lowercase, use_numbers, use_symbols, no_repeats):
    # Ensuring at least one character set is selected
    if not any([use_uppercase, use_lowercase, use_numbers, use_symbols]):
        return None  # Return None if no character set is selected
    
    # Building the character pool
    char_pool = ''
    if use_uppercase:
        char_pool += string.ascii_uppercase  
    if use_lowercase:
        char_pool += string.ascii_lowercase  
    if use_numbers:
        char_pool += string.digits           
    if use_symbols:
        char_pool += string.punctuation

    # If no repeating characters are allowed and the length is greater than the unique characters available
    if no_repeats and length > len(char_pool):
        print("Not enough unique characters available to generate a password of this length without repeats.")
        return None

    # Password generation
    if no_repeats:
        # Generate password with unique characters
        password = ''.join(random.sample(char_pool, length))
    else:
        # Generate password allowing repeats
        password = ''.join(random.choice(char_pool) for i in range(length))
    
    return password

def main():
    print("Password generator")

    # Selecting the length of the password
    while True:
        try:
            length = int(input("Input the length of the password (between 5 and 64): "))
            if 5 <= length <= 64:
                break
            else:
                print("Please enter a number between 5 and 64.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    # Keep prompting until at least one character type is selected
    while True:
        use_uppercase = input("Do you want to include uppercase characters? (y/n): ").lower() == 'y'
        use_lowercase = input("Do you want to include lowercase characters? (y/n): ").lower() == 'y'
        use_numbers = input("Do you want to include numbers? (y/n): ").lower() == 'y'
        use_symbols = input("Do you want to include symbols? (y/n): ").lower() == 'y'

        # Ask if the password should have no repeating characters
        no_repeats = input("Do you want to generate a password with no repeating characters? (y/n): ").lower() == 'y'
        
        # Generate the password
        password = generate_password(length, use_uppercase, use_lowercase, use_numbers, use_symbols, no_repeats)
        
        if password:
            print(f"Generated password: {password}")
            break
        else:
            print("You must select at least one option to create a password and ensure there are enough unique characters if no repeats are selected. Please try again.")

main()