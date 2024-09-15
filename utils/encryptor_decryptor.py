from cryptography.fernet import Fernet
from Crypto.Cipher import Blowfish
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES
import base64
import binascii

# Generate Fernet key
def generate_fernet_key():
    return Fernet.generate_key()

# Encrypt with Fernet
def encrypt_fernet(password):
    key = generate_fernet_key()
    cipher = Fernet(key)
    encrypted_password = cipher.encrypt(password.encode())
    return base64.urlsafe_b64encode(encrypted_password).decode(), key

# Decrypt with Fernet
def decrypt_fernet(encrypted_password, key):
    cipher = Fernet(key)
    encrypted_password = base64.urlsafe_b64decode(encrypted_password)
    return cipher.decrypt(encrypted_password).decode()

# Generate Blowfish key
def generate_blowfish_key():
    return get_random_bytes(16)

# Encrypt with Blowfish
def encrypt_blowfish(password):
    key = generate_blowfish_key()
    cipher = Blowfish.new(key, Blowfish.MODE_CBC)
    padded_password = pad(password.encode(), Blowfish.block_size)
    encrypted_password = cipher.encrypt(padded_password)
    return base64.b64encode(cipher.iv + encrypted_password).decode(), key

# Decrypt with Blowfish
def decrypt_blowfish(encrypted_password, key):
    encrypted_password = base64.b64decode(encrypted_password)
    cipher = Blowfish.new(key, Blowfish.MODE_CBC, iv=encrypted_password[:Blowfish.block_size])
    decrypted_padded = cipher.decrypt(encrypted_password[Blowfish.block_size:])
    return unpad(decrypted_padded, Blowfish.block_size).decode()

# Generate AES key
def generate_aes_key():
    return get_random_bytes(16)

# Encrypt with AES
def encrypt_aes(password):
    key = generate_aes_key()
    cipher = AES.new(key, AES.MODE_CBC)
    padded_password = pad(password.encode(), AES.block_size)
    encrypted_password = cipher.encrypt(padded_password)
    return base64.b64encode(cipher.iv + encrypted_password).decode(), key

# Decrypt with AES
def decrypt_aes(encrypted_password, key):
    encrypted_password = base64.b64decode(encrypted_password)
    cipher = AES.new(key, AES.MODE_CBC, iv=encrypted_password[:AES.block_size])
    decrypted_padded = cipher.decrypt(encrypted_password[AES.block_size:])
    return unpad(decrypted_padded, AES.block_size).decode()

def decrypt_password_auto(encrypted_password, keys):
    for method, (data, key) in keys.items():
        if data is None or key is None:
            continue
        try:
            if method == "Fernet":
                return decrypt_fernet(encrypted_password, key)
            elif method == "Blowfish":
                return decrypt_blowfish(encrypted_password, key)
            elif method == "AES":
                return decrypt_aes(encrypted_password, key)
        except ValueError as e:
            print(f"Decryption failed with {method}: {e}")
        except Exception as e:
            print(f"Unexpected error with {method}: {e}")
    return None

if __name__ == "__main__":
    encrypted_password_store = {}

    while True:
        print("\nOptions:")
        print("1. Encrypt a password")
        print("2. Decrypt a password")
        print("3. Exit")

        option = input("Select an option (1/2/3): ").strip()

        if option == '1':
            # Encrypt a password
            password = input("Enter the password to encrypt: ")

            print("\nChoose an encryption method:")
            print("1. Fernet (AES-based encryption)")
            print("2. Blowfish")
            print("3. AES")

            method_option = input("Select a method (1/2/3): ").strip()

            if method_option == '1':
                encrypted_data, key = encrypt_fernet(password)
                encrypted_password_store["Fernet"] = (encrypted_data, key)
                print("Encrypted password (Fernet): " + encrypted_data)
            elif method_option == '2':
                encrypted_data, key = encrypt_blowfish(password)
                encrypted_password_store["Blowfish"] = (encrypted_data, key)
                print("Encrypted password (Blowfish): " + encrypted_data)
            elif method_option == '3':
                encrypted_data, key = encrypt_aes(password)
                encrypted_password_store["AES"] = (encrypted_data, key)
                print("Encrypted password (AES): " + encrypted_data)
            else:
                print("Invalid option selected. Please choose 1, 2, or 3.")
                continue

        elif option == '2':
            # Decrypt a password
            encrypted_text = input("Enter the encrypted password (base64): ")

            print("Attempting to decrypt the password using all available methods...")

            decrypted = decrypt_password_auto(
                encrypted_text,
                {"Fernet": encrypted_password_store.get("Fernet"),
                 "Blowfish": encrypted_password_store.get("Blowfish"),
                 "AES": encrypted_password_store.get("AES")}
            )

            if decrypted:
                print(f"Decrypted password: {decrypted}")
            else:
                print("Decryption failed. Please verify the encrypted text is valid.")

        elif option == '3':
            # Exit the program
            print("Exiting the program.")
            break

        else:
            print("Invalid option. Please select 1, 2, or 3.")
