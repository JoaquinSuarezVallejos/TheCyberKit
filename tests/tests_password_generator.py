import sys
import os
import unittest
import string

# Add parent directory to the system path to import the password generator module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.password_generator import (
    generate_passphrase,  # Import function for generating passphrases
    generate_password,  # Import function for generating passwords
    handle_password_generation_request,  # Import function to handle password requests
    handle_passphrase_generation_request,  # Import function to handle passphrase requests
)


class TestPasswordGenerator(unittest.TestCase):
    # Test generating a password with all character options enabled
    def test_generate_password_with_all_options(self):
        password = generate_password(12, True, True, True, True)
        self.assertEqual(len(password), 12)  # Check password length
        self.assertTrue(any(c.isupper() for c in password))  # Check for uppercase
        self.assertTrue(any(c.islower() for c in password))  # Check for lowercase
        self.assertTrue(any(c.isdigit() for c in password))  # Check for digits
        self.assertTrue(
            any(c in string.punctuation for c in password)
        )  # Check for symbols

    # Test generating a password with only uppercase letters and numbers
    def test_generate_password_only_uppercase_and_numbers(self):
        password = generate_password(10, True, False, True, False)
        self.assertEqual(len(password), 10)  # Check password length
        self.assertTrue(any(c.isupper() for c in password))  # Check for uppercase
        self.assertTrue(any(c.isdigit() for c in password))  # Check for digits
        self.assertFalse(any(c.islower() for c in password))  # Ensure no lowercase
        self.assertFalse(
            any(c in string.punctuation for c in password)
        )  # Ensure no symbols

    # Test generating a password with minimum length of 1
    def test_generate_password_minimum_length(self):
        password = generate_password(1, True, False, False, False)
        self.assertEqual(len(password), 1)  # Check password length
        self.assertTrue(any(c.isupper() for c in password))  # Check for uppercase

    # Test handling a valid password generation request
    def test_handle_password_generation_request_valid(self):
        request_data = {
            "length": 8,
            "use_uppercase": True,
            "use_lowercase": True,
            "use_numbers": True,
            "use_symbols": False,
        }
        password = handle_password_generation_request(request_data)
        self.assertIsNotNone(password)  # Ensure password is generated
        self.assertEqual(len(password), 8)  # Check password length

    # Test handling a password generation request with missing keys
    def test_handle_password_generation_request_missing_key(self):
        request_data = {
            "length": 8,
            "use_uppercase": True,
            "use_lowercase": True,
            # Missing 'use_numbers' and 'use_symbols'
        }
        password = handle_password_generation_request(request_data)
        self.assertIsNone(password)  # Expect None due to missing keys

    # Test generating a passphrase with the first letter of each word capitalized
    def test_generate_passphrase_with_capitalize_first(self):
        passphrase = generate_passphrase(4, True, False, False, " ")
        words = passphrase.split(" ")
        self.assertEqual(len(words), 4)  # Check word count
        self.assertTrue(
            all(word[0].isupper() for word in words)
        )  # Check capitalization of first letter

    # Test generating a passphrase with all words in uppercase
    def test_generate_passphrase_with_all_capitalized(self):
        passphrase = generate_passphrase(3, False, True, False, "-")
        words = passphrase.split("-")
        self.assertEqual(len(words), 3)  # Check word count
        self.assertTrue(all(word.isupper() for word in words))  # Check all uppercase

    # Test generating a passphrase with numbers added at the end of each word
    def test_generate_passphrase_with_numbers(self):
        passphrase = generate_passphrase(5, False, False, True, "-")
        words = passphrase.split("-")
        self.assertEqual(len(words), 5)  # Check word count
        self.assertTrue(
            all(word[-1].isdigit() for word in words)
        )  # Check each word ends with a digit

    # Test handling a valid passphrase generation request
    def test_handle_passphrase_generation_request_valid(self):
        request_data = {
            "num_words": 5,
            "capitalize_first": True,
            "capitalize_all": False,
            "add_numbers": False,
            "word_separator": " ",
        }
        passphrase = handle_passphrase_generation_request(request_data)
        self.assertIsNotNone(passphrase)  # Ensure passphrase is generated
        self.assertEqual(len(passphrase.split(" ")), 5)  # Check word count

    # Test handling an invalid passphrase request with an out-of-range word count
    def test_handle_passphrase_generation_request_invalid_num_words(self):
        request_data = {
            "num_words": 2,  # Out of valid range
            "capitalize_first": False,
            "capitalize_all": False,
            "add_numbers": False,
            "word_separator": "-",
        }
        passphrase = handle_passphrase_generation_request(request_data)
        self.assertIsNone(passphrase)  # Expect None due to invalid word count


# Run the unit tests
if __name__ == "__main__":
    unittest.main()
