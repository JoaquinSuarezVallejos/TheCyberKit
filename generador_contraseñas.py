# TODO password generator
# add passphrase
# fix with pep8
# TODO whole program
# make both the web page and console run the program
# have all functionalities in the same file
import random
import string


def generate_password(length, use_uppercase, use_lowercase, use_numbers,
                      use_symbols, no_repeats):
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

    # If no repeating characters == Y and length > unique characters available
    if no_repeats and length > len(char_pool):
        print("Not enough unique characters available to generate a password.")
        return None

    # Password generation
    if no_repeats:
        # Generate password with unique characters
        password = ''.join(random.sample(char_pool, length))
    else:
        # Generate password allowing repeats
        password = ''.join(random.choice(char_pool) for i in range(length))

    return password


# Helper function to ensure input is 'Y', 'y', 'N', or 'n'
def get_yes_no_input(prompt):
    while True:
        try:
            response = input(prompt).strip().lower()
            if response in ['y', 'n']:
                return response == 'y'
            else:
                print("Invalid input. Please enter 'Y' or 'N'.")
        except Exception as e:
            print(f"An error occurred: {e}. Please try again.")


def main():
    print("Password generator")

    # Selecting the length of the password
    while True:
        try:
            length = int(input("Input the password length (between 5 & 64): "))
            if 5 <= length <= 64:
                break
            else:
                print("Please enter a number between 5 and 64.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    # Keep prompting until at least one character type is selected
    while True:
        use_uppercase = get_yes_no_input("Include uppercase chars? (Y/N): ")
        use_lowercase = get_yes_no_input("Include lowercase chars? (Y/N): ")
        use_numbers = get_yes_no_input("Include numbers? (Y/N): ")
        use_symbols = get_yes_no_input("Include symbols? (Y/N): ")

        # Ask if the password should have no repeating characters
        no_repeats = get_yes_no_input("Enable no repeating chars? (Y/N): ")

        # Generate the password
        password = generate_password(length, use_uppercase, use_lowercase,
                                     use_numbers, use_symbols, no_repeats)

        if password:
            print(f"Generated password: {password}")
            break
        elif not any([use_uppercase, use_lowercase, use_numbers, use_symbols]):
            print("You must select at least one option. Please try again.")
        else:
            print("Not enough unique chars for the desired length. Try again.")

main()
