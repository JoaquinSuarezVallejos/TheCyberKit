# PASSWORD GENERATOR (Python file)
# Case types used: snake_case (for functions and variables)
# and SCREAMING_SNAKE_CASE (for constants)

# Importing the necessary libraries and modules
import random
import string
from english_words import get_english_words_set

# english_words: A Python package that provides a set of English words


# Function to generate a passphrase
def generate_passphrase(
    num_words,
    # Number of words in the passphrase (int)
    capitalize_first,
    # Whether to capitalize the first letter of each word (bool)
    capitalize_all,
    # Whether to capitalize all letters (bool)
    add_numbers,
    # Whether to add a number to the end of each word (bool)
    word_separator,
    # The separator character to use between words (str)
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
    # The desired password length (int)
    use_uppercase,
    # Whether to include uppercase letters (bool)
    use_lowercase,
    # Whether to include lowercase letters (bool)
    use_numbers,
    # Whether to include numbers (bool)
    use_symbols,
    # Whether to include symbols (bool)
):
    # Initialize an empty list to store the selected
    # character types for the password
    char_types = []

    # Add the selected character types to the list
    if use_uppercase:
        # Add all uppercase letters
        char_types.append(string.ascii_uppercase)
    if use_lowercase:
        # Add all lowercase letters
        char_types.append(string.ascii_lowercase)
    if use_numbers:
        # Add all digits
        char_types.append(string.digits)
    if use_symbols:
        # Add all punctuation/special characters
        char_types.append(string.punctuation)

    # Generate the first characters randomly from the selected types
    password = [random.choice(char_type) for char_type in char_types]

    # Continue adding random characters until
    # the password reaches the desired length
    while len(password) < length:
        # Randomly select a character type from the list
        char_type = random.choice(char_types)

        # Append a random character from the selected type to the password
        password.append(random.choice(char_type))

    # Shuffle to avoid having the characters from
    # selected types appear in a predictable order
    random.shuffle(password)

    # Return the password as a string
    return "".join(password)


def handle_password_generation_request(request_data):
    # Handle password generation based on request data from the front-end
    try:
        # Extract parameters from the request data (JSON)
        length = int(request_data["length"])
        use_uppercase = request_data["use_uppercase"]
        use_lowercase = request_data["use_lowercase"]
        use_numbers = request_data["use_numbers"]
        use_symbols = request_data["use_symbols"]

        # Ensure at least one character type is selected
        if not any([use_uppercase, use_lowercase, use_numbers, use_symbols]):
            return None

        # Generate the password based on the provided parameters
        password = generate_password(
            length,
            use_uppercase,
            use_lowercase,
            use_numbers,
            use_symbols
        )

        return password

    except (ValueError, KeyError) as e:
        # Handle exceptions related to missing or invalid data
        print(f"Error handling password generation request: {e}")
        return None


def handle_passphrase_generation_request(request_data):
    # Handle passphrase generation based on request data from the front-end
    try:
        # Default word-separator is None
        word_separator = None

        # Print the request data for debugging
        print("Received request data:", request_data)

        # Extract parameters from the request data (JSON)
        num_words = int(request_data["num_words"])
        capitalize_first = request_data["capitalize_first"]
        capitalize_all = request_data["capitalize_all"]
        add_numbers = request_data["add_numbers"]
        word_separator = str(request_data.get("word_separator") or "-")
        # Get the word separator or use "-" as the default separator

        # Ensure the number of words is within the valid range (3-12)
        if not (3 <= num_words <= 12):
            return None

        # Generate the passphrase based on the provided parameters
        passphrase = generate_passphrase(
            num_words,
            capitalize_first,
            capitalize_all,
            add_numbers,
            word_separator
        )

        return passphrase

    except (ValueError, KeyError) as e:
        # Handle exceptions related to missing or invalid data
        print(f"Error handling passphrase generation request: {e}")
        return None
