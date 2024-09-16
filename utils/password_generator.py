# PASSWORD GENERATOR (Python file)
# Case types used: snake_case (for functions and variables) and SCREAMING_SNAKE_CASE (for constants)

# Importing the necessary libraries and modules
import random
import string
from english_words import get_english_words_set

def generate_passphrase(
    num_words,
    capitalize_first,
    capitalize_all,
    word_separator,
    add_numbers,
):
    # Ensuring valid word count
    if not (3 <= num_words <= 15):
        print("The number of words must be between 3 and 15.")
        return None

    # Fetch the English words set from the available source
    word_list = list(get_english_words_set(["web2"]))

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


def generate_password(
    length,
    use_uppercase,
    use_lowercase,
    use_numbers,
    use_symbols,
    no_repeats,
):
    # Ensuring at least one character set is selected
    if not any(
        [use_uppercase, use_lowercase, use_numbers, use_symbols]
    ):
        return None  # Return None if no character set is selected

    # Building the character pool
    char_pool = ""
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
        print(
            "Not enough unique characters available to generate a password."
        )
        return None

    # Password generation
    if no_repeats:
        # Generate password with unique characters
        password = "".join(random.sample(char_pool, length))
    else:
        # Generate password allowing repeats
        password = "".join(
            random.choice(char_pool) for i in range(length)
        )

    return password

def handle_password_generation_request(request_data):
    """
    Handles password generation based on request data from the frontend.

    Args:
        request_data (dict): A dictionary containing the following keys:
            - 'length': The desired password length (int).
            - 'use_uppercase': Whether to include uppercase letters (bool).
            - 'use_lowercase': Whether to include lowercase letters (bool).
            - 'use_numbers': Whether to include numbers (bool).
            - 'use_symbols': Whether to include symbols (bool).
            - 'no_repeats': Whether to avoid repeating characters (bool).

    Returns:
        str or None: The generated password if successful, or None if there's an error.
    """

    try:
        length = int(request_data['length'])
        use_uppercase = request_data['use_uppercase']
        use_lowercase = request_data['use_lowercase']
        use_numbers = request_data['use_numbers']
        use_symbols = request_data['use_symbols']
        no_repeats = request_data['no_repeats']

        if not any([use_uppercase, use_lowercase, use_numbers, use_symbols]):
            return None 

        password = generate_password(
            length, use_uppercase, use_lowercase, use_numbers, use_symbols, no_repeats
        )
        
        return password

    except (ValueError, KeyError) as e:
        print(f"Error handling password generation request: {e}")
        return None


def handle_passphrase_generation_request(request_data):
    """
    Handles passphrase generation based on request data from the frontend

    Args:
        request_data (dict): A dictionary containing the following keys:
            - 'num_words': The number of words in the passphrase (int)
            - 'capitalize_first': Whether to capitalize the first letter of each word (bool)
            - 'capitalize_all': Whether to capitalize all letters (bool)
            - 'word_separator': The separator character between words (str)
            - 'add_numbers': Whether to add a number to the end of each word (bool)

    Returns:
        str or None - The generated passphrase if successful, or None if there's an error
    """

    try:
        num_words = int(request_data['num_words'])
        capitalize_first = request_data['capitalize_first']
        capitalize_all = request_data['capitalize_all']
        word_separator = request_data['word_separator'] or " " # Default to space if not provided
        add_numbers = request_data['add_numbers']

        if not (3 <= num_words <= 15):
            return None 

        passphrase = generate_passphrase(
            num_words, capitalize_first, capitalize_all, word_separator, add_numbers
        )

        return passphrase 

    except (ValueError, KeyError) as e:
        print(f"Error handling passphrase generation request: {e}")
        return None
    
# TODO: format the code with black