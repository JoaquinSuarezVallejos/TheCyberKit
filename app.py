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

import random
import string
from english_words import english_words_set

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

def generate_passphrase(num_words, capitalize_first, capitalize_all, word_separator, add_numbers):
    # Ensuring valid word count
    if not (3 <= num_words <= 15):
        print("The number of words must be between 3 and 15.")
        return None

    # Convert dictionary words set to a list
    word_list = list(english_words_set)
    
    # Generating the list of words
    words = [random.choice(word_list) for i in range(num_words)]
    
    # Apply capitalization options
    if capitalize_all:
        words = [word.upper() for word in words]
    elif capitalize_first:
        words = [word.capitalize() for word in words]

    # Add numbers to each word if requested
    if add_numbers:
        words = [f"{word}{random.randint(0, 9)}" for word in words]
    
    # Join the words using the chosen separator
    passphrase = word_separator.join(words)
    
    return passphrase

def main():
    print("Welcome to the Password and Passphrase Generator")

    while True:
        option = input("Would you like to generate a (p)assword or a (ph)rase? (p/ph): ").lower()

        if option == 'p':
            # Generate a password
            print("Generating a random password...")
            
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
            break

        elif option == 'ph':
            # Generate a passphrase
            print("Generating a passphrase...")
            
            while True:
                try:
                    num_words = int(input("Input the number of words for the passphrase (between 3 and 15): "))
                    if 3 <= num_words <= 15:
                        break
                    else:
                        print("Please enter a number between 3 and 15.")
                except ValueError:
                    print("Invalid input. Please enter a valid number.")

            capitalize_first = input("Do you want to capitalize the first letter of each word? (y/n): ").lower() == 'y'
            capitalize_all = input("Do you want to capitalize all letters? (y/n): ").lower() == 'y'
            word_separator = input("Enter a single character to use as a word separator (default is space): ") or ' '
            add_numbers = input("Do you want to add a number to each word? (y/n): ").lower() == 'y'

            # Generate the passphrase
            passphrase = generate_passphrase(num_words, capitalize_first, capitalize_all, word_separator, add_numbers)

            if passphrase:
                print(f"Generated passphrase: {passphrase}")
            else:
                print("Could not generate a passphrase with the given parameters. Please try again.")
            break

        else:
            print("Invalid option. Please choose 'p' for password or 'ph' for passphrase.")
    
main()