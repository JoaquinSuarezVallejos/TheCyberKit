# TODO password generator
# add passphrase
# fix y/n answers so as to not skip to the next question if the input is not y/n
# fix the pep8
# TODO whole program
# make both the web pag and console run the program
# have all functionalities in the same file
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
        password = ''.join(random.choice(char_pool) for _ in range(length))
    
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