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
    words = [random.choice(word_list) for _ in range(num_words)]

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
            random.choice(char_pool) for _ in range(length)
        )

    return password


# Helper function to ensure input is 'Y', 'y', 'N', or 'n'
def get_yes_no_input(prompt):
    while True:
        try:
            response = input(prompt).strip().lower()
            if response in ["y", "n"]:
                return response == "y"
            else:
                print("Invalid input. Please enter 'Y' or 'N'.")
        except Exception as e:
            print(f"An error occurred: {e}. Please try again.")


def handle_password_generation():
    # Handle password generation process
    while True:
        try:
            length = int(
                input("Input the password length (between 5 & 64): ")
            )
            if 5 <= length <= 64:
                break
            else:
                print("Please enter a number between 5 and 64.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    while True:
        use_uppercase = get_yes_no_input(
            "Include uppercase chars? (Y/N): "
        )
        use_lowercase = get_yes_no_input(
            "Include lowercase chars? (Y/N): "
        )
        use_numbers = get_yes_no_input("Include numbers? (Y/N): ")
        use_symbols = get_yes_no_input("Include symbols? (Y/N): ")
        no_repeats = get_yes_no_input(
            "Enable no repeating chars? (Y/N): "
        )

        if any(
            [use_uppercase, use_lowercase, use_numbers, use_symbols]
        ):
            password = generate_password(
                length,
                use_uppercase,
                use_lowercase,
                use_numbers,
                use_symbols,
                no_repeats,
            )
            if password:
                print(f"Generated password: {password}")
                break
            else:
                print("Not enough unique chars. Try again.")
        else:
            print(
                "You must select at least one option. Please try again."
            )


def handle_passphrase_generation():
    # Handle passphrase generation process
    while True:
        try:
            num_words = int(
                input(
                    "Input the number of words (between 3 and 15): "
                )
            )
            if 3 <= num_words <= 15:
                break
            else:
                print("Please enter a number between 3 and 15.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    capitalize_all = get_yes_no_input(
        "Capitalize all letters? (Y/N): "
    )
    capitalize_first = not capitalize_all and get_yes_no_input(
        "Capitalize the first letter of each word? (Y/N): "
    )

    while True:
        word_separator = input(
            "Enter a character to use as a separator (default is space): "
        )
        if word_separator or word_separator == " ":
            word_separator = word_separator or " "
            break
        else:
            print("Invalid input. Please enter a valid character.")

    add_numbers = get_yes_no_input(
        "Add a number to each word? (Y/N): "
    )

    passphrase = generate_passphrase(
        num_words,
        capitalize_first,
        capitalize_all,
        word_separator,
        add_numbers,
    )
    if passphrase:
        print(f"Generated passphrase: {passphrase}")
    else:
        print("Could not generate a passphrase. Please try again.")


def main():
    print("Password/Passphrase Generator")

    while True:
        option = get_valid_option()

        if option == "p":
            handle_password_generation()
        elif option == "ph":
            handle_passphrase_generation()

        if not get_yes_no_input("Generate another? (Y/N): "):
            print(
                "Thank you for using the Password/Passphrase Generator. "
                "Goodbye!"
            )
            break


def get_valid_option():
    # Ensure a valid option is provided
    while True:
        option = (
            input("Generate password or passphrase? (P/PH): ")
            .strip()
            .lower()
        )
        if option in ["p", "ph"]:
            return option
        print(
            "Invalid option. Please choose either 'P'" +
            "(password) or 'PH' (passphrase)."
        )


main()
