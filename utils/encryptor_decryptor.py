from Crypto.Cipher import Blowfish, AES
from Crypto.Util.Padding import pad, unpad
import base64
from cryptography.fernet import Fernet
import hashlib

# TODO: Implement the encryptor_decryptor back-end to the front-end

# The text encryptor/decryptor uses symmetric encryption methods (the same key is used for both encryption and decryption)
# Algorithms used: Fernet, Blowfish and AES.


# Function to hash the user-provided key for appropriate length (32 bytes for Fernet, 16 bytes for Blowfish and AES)
def format_key(key, method):
    if method == "Fernet":
        # Hash the key and encode it in base64 for Fernet
        return base64.urlsafe_b64encode(hashlib.sha256(key.encode()).digest())
    elif method in ["Blowfish", "AES"]:
        # Hash the key and return the first 16 bytes for Blowfish and AES
        return hashlib.sha256(key.encode()).digest()[:16]


# Encrypt with Fernet
def encrypt_fernet(password, key):
    fernet = Fernet(key) # Create a Fernet key
    encrypted = fernet.encrypt(password.encode()) # Encrypt the password
    return encrypted.decode() # Return the encrypted password as a string


# Decrypt with Fernet
def decrypt_fernet(encrypted_password, key):
    fernet = Fernet(key) # Create a Fernet key
    decrypted = fernet.decrypt(encrypted_password.encode()).decode() # Decrypt the password
    return decrypted # Return the decrypted password as a string


# Encrypt with Blowfish
def encrypt_blowfish(password, key):
    cipher = Blowfish.new(key, Blowfish.MODE_CBC) # Create a Blowfish cipher
    padded_password = pad(password.encode(), Blowfish.block_size) # Pad the password
    iv = cipher.iv # Get the initialization vector
    encrypted = cipher.encrypt(padded_password) # Encrypt the password
    return base64.b64encode(iv + encrypted).decode() # Return the encrypted password as a string


# Decrypt with Blowfish
def decrypt_blowfish(encrypted_password, key):
    encrypted_password = base64.b64decode(encrypted_password.encode()) # Decode the encrypted password
    iv = encrypted_password[: Blowfish.block_size] # Get the initialization vector
    cipher = Blowfish.new(key, Blowfish.MODE_CBC, iv) # Create a Blowfish cipher
    decrypted_padded = cipher.decrypt(encrypted_password[Blowfish.block_size :]) # Decrypt the password
    decrypted = unpad(decrypted_padded, Blowfish.block_size).decode() # Unpad the decrypted password
    return decrypted # Return the decrypted password as a string


# Encrypt with AES
def encrypt_aes(password, key):
    cipher = AES.new(key, AES.MODE_CBC) # Create an AES cipher
    padded_password = pad(password.encode(), AES.block_size) # Pad the password
    iv = cipher.iv # Get the initialization vector
    encrypted = cipher.encrypt(padded_password) # Encrypt the password
    return base64.b64encode(iv + encrypted).decode() # Return the encrypted password as a string


# Decrypt with AES
def decrypt_aes(encrypted_password, key):
    encrypted_password = base64.b64decode(encrypted_password.encode()) # Decode the encrypted password
    iv = encrypted_password[: AES.block_size] # Get the initialization vector
    cipher = AES.new(key, AES.MODE_CBC, iv) # Create an AES cipher
    decrypted_padded = cipher.decrypt(encrypted_password[AES.block_size :]) # Decrypt the password
    decrypted = unpad(decrypted_padded, AES.block_size).decode() # Unpad the decrypted password
    return decrypted # Return the decrypted password as a string


# Main logic
def main():
    while True:
        print("1. Encrypt\n2. Decrypt\n3. Exit")
        option = ""
        while not option:
            option = input("Select an option: ").strip()
            if not option:
                print("Option cannot be empty. Please try again.")

        if option == "1":
            password = ""
            while not password:
                password = input("Enter the password to encrypt: ").strip()
                if not password:
                    print("Password cannot be empty. Please try again.")

            method = ""
            while method not in ["1", "2", "3"]:
                method = input("Choose method: 1. Fernet 2. Blowfish 3. AES: ").strip()
                if method not in ["1", "2", "3"]:
                    print("Invalid method. Please select 1, 2, or 3.")

            user_key = ""
            while not user_key:
                user_key = input("Encrypt with a custom secret key: ").strip()
                if not user_key:
                    print("Key cannot be empty. Please provide a key.")

            if method == "1":
                formatted_key = format_key(user_key, "Fernet")
                encrypted_password = encrypt_fernet(password, formatted_key)
            elif method == "2":
                formatted_key = format_key(user_key, "Blowfish")
                encrypted_password = encrypt_blowfish(password, formatted_key)
            elif method == "3":
                formatted_key = format_key(user_key, "AES")
                encrypted_password = encrypt_aes(password, formatted_key)

            print(f"Encrypted password: {encrypted_password}")

        elif option == "2":
            encrypted_password = ""
            while not encrypted_password:
                encrypted_password = input("Enter the encrypted password: ").strip()
                if not encrypted_password:
                    print("Encrypted password cannot be empty. Please try again.")

            user_key = ""
            while not user_key:
                user_key = input("Decryption requires a custom secret key: ").strip()
                if not user_key:
                    print("Key cannot be empty. Please provide a key.")

            decrypted_password = None

            # Try decryption with Fernet
            try:
                formatted_key = format_key(user_key, "Fernet")
                decrypted_password = decrypt_fernet(encrypted_password, formatted_key)
                print(f"Decrypted password (Fernet): {decrypted_password}")
            except Exception:
                pass

            # If Fernet fails, try Blowfish
            if not decrypted_password:
                try:
                    formatted_key = format_key(user_key, "Blowfish")
                    decrypted_password = decrypt_blowfish(
                        encrypted_password, formatted_key
                    )
                    print(f"Decrypted password (Blowfish): {decrypted_password}")
                except Exception:
                    pass

            # If Blowfish fails, try AES
            if not decrypted_password:
                try:
                    formatted_key = format_key(user_key, "AES")
                    decrypted_password = decrypt_aes(encrypted_password, formatted_key)
                    print(f"Decrypted password (AES): {decrypted_password}")
                except Exception:
                    pass

            # If all methods fail, notify the user
            if not decrypted_password:
                print(
                    "Decryption failed for all methods. Please check the encrypted password and key."
                )

        elif option == "3":
            break
        else:
            print("Invalid option. Please select 1, 2, or 3.")


if __name__ == "__main__":
    main()
