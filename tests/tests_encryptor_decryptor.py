# UNIT TESTS FOR THE ENCRYPTOR/DECRYPTOR (Python file)

import unittest
import sys
import os
import base64
import hashlib

# Add parent directory to system path for importing encryptor and decryptor functions
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.encryptor_decryptor import (
    encrypt_fernet,  # Import Fernet encryption function
    decrypt_fernet,  # Import Fernet decryption function
    encrypt_blowfish,  # Import Blowfish encryption function
    decrypt_blowfish,  # Import Blowfish decryption function
    encrypt_aes,  # Import AES encryption function
    decrypt_aes,  # Import AES decryption function
    format_key,  # Import function to format keys for encryption methods
)


# Define test cases for encryption and decryption methods
class TestEncryptionDecryption(unittest.TestCase):
    def setUp(self):
        # Define a sample password and custom keys
        self.password = "test_password_123"
        self.custom_key = "sample_custom_key"

        # Format keys for each encryption method
        self.fernet_key = format_key(self.custom_key, "Fernet")
        self.blowfish_key = format_key(self.custom_key, "Blowfish")
        self.aes_key = format_key(self.custom_key, "AES")

    # Test Fernet encryption and decryption
    def test_fernet_encrypt_decrypt(self):
        encrypted_password = encrypt_fernet(self.password, self.fernet_key)
        decrypted_password = decrypt_fernet(encrypted_password, self.fernet_key)
        self.assertEqual(
            self.password, decrypted_password
        )  # Ensure decryption matches original

    # Test Blowfish encryption and decryption
    def test_blowfish_encrypt_decrypt(self):
        encrypted_password = encrypt_blowfish(self.password, self.blowfish_key)
        decrypted_password = decrypt_blowfish(encrypted_password, self.blowfish_key)
        self.assertEqual(
            self.password, decrypted_password
        )  # Ensure decryption matches original

    # Test AES encryption and decryption
    def test_aes_encrypt_decrypt(self):
        encrypted_password = encrypt_aes(self.password, self.aes_key)
        decrypted_password = decrypt_aes(encrypted_password, self.aes_key)
        self.assertEqual(
            self.password, decrypted_password
        )  # Ensure decryption matches original

    # Test invalid Fernet decryption (e.g., using incorrect key)
    def test_invalid_fernet_decrypt(self):
        invalid_key = base64.urlsafe_b64encode(hashlib.sha256(b"invalid_key").digest())
        encrypted_password = encrypt_fernet(self.password, self.fernet_key)
        with self.assertRaises(Exception):  # Expect an exception for decryption failure
            decrypt_fernet(encrypted_password, invalid_key)

    # Test invalid Blowfish decryption (e.g., using incorrect key)
    def test_invalid_blowfish_decrypt(self):
        invalid_key = os.urandom(16)  # Generate a random key for Blowfish
        encrypted_password = encrypt_blowfish(self.password, self.blowfish_key)
        with self.assertRaises(Exception):  # Expect an exception for decryption failure
            decrypt_blowfish(encrypted_password, invalid_key)

    # Test invalid AES decryption (e.g., using incorrect key)
    def test_invalid_aes_decrypt(self):
        invalid_key = os.urandom(16)  # Generate a random key for AES
        encrypted_password = encrypt_aes(self.password, self.aes_key)
        with self.assertRaises(Exception):  # Expect an exception for decryption failure
            decrypt_aes(encrypted_password, invalid_key)


# Run the unit tests
if __name__ == "__main__":
    unittest.main()