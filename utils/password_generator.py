# PASSWORD GENERATOR (Python file)
# Case types used: snake_case (for functions and variables)
# and SCREAMING_SNAKE_CASE (for constants)

# TODO: Implement the password tester functionality


# Importing the necessary libraries and modules
import random
import string
from english_words import get_english_words_set


def generate_passphrase(
    num_words,
    capitalize_first,
    capitalize_all,
    add_numbers,
    word_separator,
):
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
):
    # Building the character pools
    char_types = []
    if use_uppercase:
        char_types.append(string.ascii_uppercase)
    if use_lowercase:
        char_types.append(string.ascii_lowercase)
    if use_numbers:
        char_types.append(string.digits)
    if use_symbols:
        char_types.append(string.punctuation)

    # Ensure there is at least one character from each selected type
    password = [random.choice(char_type) for char_type in char_types]

    # Generate the remaining characters randomly from the selected types
    while len(password) < length:
        # Randomly choose one of the selected character types, then pick a random character from that type
        char_type = random.choice(char_types)
        password.append(random.choice(char_type))

    # Shuffle to avoid having the characters from selected types appear in a predictable order
    random.shuffle(password)

    return ''.join(password)  # Return password as a string


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

    Returns:
        The generated password if successful, or None if there's an error.
    """

    try:
        length = int(request_data["length"])
        use_uppercase = request_data["use_uppercase"]
        use_lowercase = request_data["use_lowercase"]
        use_numbers = request_data["use_numbers"]
        use_symbols = request_data["use_symbols"]

        if not any([use_uppercase, use_lowercase, use_numbers, use_symbols]):
            return None

        password = generate_password(
            length, use_uppercase, use_lowercase, use_numbers, use_symbols
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
            - 'num_words':
            The number of words in the passphrase (int)

            - 'capitalize_first':
            Whether to capitalize the first letter of each word (bool)

            - 'capitalize_all':
            Whether to capitalize all letters (bool)

            - 'word_separator':
            The separator character (str) to use between words

            - 'add_numbers':
            Whether to add a number to the end of each word (bool)

    Returns:
        The generated passphrase if successful, or None if there's an error
    """

    try:
        # Define word_separator as None
        # to handle missing key in request_data
        word_separator = None

        print(
            "Received request data:", request_data
        )  # Print the entire request data for inspection

        # Extract parameters, ensuring 'word_separator' is a string
        num_words = int(request_data["num_words"])
        capitalize_first = request_data["capitalize_first"]
        capitalize_all = request_data["capitalize_all"]
        add_numbers = request_data["add_numbers"]

        # Get word_separator from request_data, or default to "-"
        word_separator = str(request_data.get("word_separator") or "-")

        print(f"num_words type: {type(num_words)}")
        print(f"capitalize_first type: {type(capitalize_first)}")
        print(f"capitalize_all type: {type(capitalize_all)}")
        print(f"add_numbers type: {type(add_numbers)}")
        print(f"word_separator type: {type(word_separator)}")

        # Validate num_words
        if not (3 <= num_words <= 12):
            return None

        passphrase = generate_passphrase(
            num_words, capitalize_first, capitalize_all,
            add_numbers, word_separator
        )

        return passphrase

    except (ValueError, KeyError) as e:
        print(f"Error handling passphrase generation request: {e}")
        return None
