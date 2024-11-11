import sys
import os
import unittest
import string
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.password_generator import (
    generate_passphrase,
    generate_password,
    handle_password_generation_request,
    handle_passphrase_generation_request
)

class TestPasswordGenerator(unittest.TestCase):
    def test_generate_password_with_all_options(self):
        password = generate_password(12, True, True, True, True)
        self.assertEqual(len(password), 12)
        self.assertTrue(any(c.isupper() for c in password))
        self.assertTrue(any(c.islower() for c in password))
        self.assertTrue(any(c.isdigit() for c in password))
        self.assertTrue(any(c in "!@#$%^&*()-_+=" for c in password))

    def test_generate_password_only_uppercase_and_numbers(self):
        password = generate_password(10, True, False, True, False)
        self.assertEqual(len(password), 10)
        self.assertTrue(any(c.isupper() for c in password))
        self.assertTrue(any(c.isdigit() for c in password))
        self.assertFalse(any(c.islower() for c in password))
        self.assertFalse(any(c in string.punctuation for c in password))

    def test_generate_password_minimum_length(self):
        password = generate_password(1, True, False, False, False)
        self.assertEqual(len(password), 1)
        self.assertTrue(any(c.isupper() for c in password))

    def test_handle_password_generation_request_valid(self):
        request_data = {
            'length': 8,
            'use_uppercase': True,
            'use_lowercase': True,
            'use_numbers': True,
            'use_symbols': False
        }
        password = handle_password_generation_request(request_data)
        self.assertIsNotNone(password)
        self.assertEqual(len(password), 8)

    def test_handle_password_generation_request_missing_key(self):
        request_data = {
            'length': 8,
            'use_uppercase': True,
            'use_lowercase': True,
            # Missing 'use_numbers' and 'use_symbols'
        }
        password = handle_password_generation_request(request_data)
        self.assertIsNone(password)

    def test_generate_passphrase_with_capitalize_first(self):
        passphrase = generate_passphrase(4, True, False, False, ' ')
        words = passphrase.split(' ')
        self.assertEqual(len(words), 4)
        self.assertTrue(all(word[0].isupper() for word in words))

    def test_generate_passphrase_with_all_capitalized(self):
        passphrase = generate_passphrase(3, False, True, False, '-')
        words = passphrase.split('-')
        self.assertEqual(len(words), 3)
        self.assertTrue(all(word.isupper() for word in words))

    def test_generate_passphrase_with_numbers(self):
        passphrase = generate_passphrase(5, False, False, True, '-')
        words = passphrase.split('-')
        self.assertEqual(len(words), 5)
        self.assertTrue(all(word[-1].isdigit() for word in words))

    def test_handle_passphrase_generation_request_valid(self):
        request_data = {
            'num_words': 5,
            'capitalize_first': True,
            'capitalize_all': False,
            'add_numbers': False,
            'word_separator': ' '
        }
        passphrase = handle_passphrase_generation_request(request_data)
        self.assertIsNotNone(passphrase)
        self.assertEqual(len(passphrase.split(' ')), 5)

    def test_handle_passphrase_generation_request_invalid_num_words(self):
        request_data = {
            'num_words': 2,  # Out of valid range
            'capitalize_first': False,
            'capitalize_all': False,
            'add_numbers': False,
            'word_separator': '-'
        }
        passphrase = handle_passphrase_generation_request(request_data)
        self.assertIsNone(passphrase)

if __name__ == '__main__':
    unittest.main()
