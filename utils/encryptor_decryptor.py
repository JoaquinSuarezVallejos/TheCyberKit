from Crypto.Cipher import Blowfish, AES
from Crypto.Util.Padding import pad, unpad
import base64
from cryptography.fernet import Fernet
import os

# Generate keys for encryption methods
def generate_keys():
    fernet_key = Fernet.generate_key()
    blowfish_key = os.urandom(16)  # Blowfish requires a key of 4 to 56 bytes
    aes_key = os.urandom(16)  # AES key size can be 16, 24, or 32 bytes
    return fernet_key, blowfish_key, aes_key

# Encrypt with Fernet
def encrypt_fernet(password, key):
    fernet = Fernet(key)
    encrypted = fernet.encrypt(password.encode())
    return encrypted.decode()  # Decode bytes to string

# Decrypt with Fernet
def decrypt_fernet(encrypted_password, key):
    fernet = Fernet(key)
    decrypted = fernet.decrypt(encrypted_password.encode()).decode()  # Convert string back to bytes and then decode
    return decrypted

# Encrypt with Blowfish
def encrypt_blowfish(password, key):
    cipher = Blowfish.new(key, Blowfish.MODE_CBC)
    padded_password = pad(password.encode(), Blowfish.block_size)
    iv = cipher.iv
    encrypted = cipher.encrypt(padded_password)
    return base64.b64encode(iv + encrypted).decode()

# Decrypt with Blowfish
def decrypt_blowfish(encrypted_password, key):
    encrypted_password = base64.b64decode(encrypted_password.encode())
    iv = encrypted_password[:Blowfish.block_size]
    cipher = Blowfish.new(key, Blowfish.MODE_CBC, iv)
    decrypted_padded = cipher.decrypt(encrypted_password[Blowfish.block_size:])
    decrypted = unpad(decrypted_padded, Blowfish.block_size).decode()
    return decrypted

# Encrypt with AES
def encrypt_aes(password, key):
    cipher = AES.new(key, AES.MODE_CBC)
    padded_password = pad(password.encode(), AES.block_size)
    iv = cipher.iv
    encrypted = cipher.encrypt(padded_password)
    return base64.b64encode(iv + encrypted).decode()

# Decrypt with AES
def decrypt_aes(encrypted_password, key):
    encrypted_password = base64.b64decode(encrypted_password.encode())
    iv = encrypted_password[:AES.block_size]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_padded = cipher.decrypt(encrypted_password[AES.block_size:])
    decrypted = unpad(decrypted_padded, AES.block_size).decode()
    return decrypted

# Main logic
def main():
    fernet_key, blowfish_key, aes_key = generate_keys()
    store = {
        "fernet": {"key": fernet_key},
        "blowfish": {"key": blowfish_key},
        "aes": {"key": aes_key}
    }
    
    while True:
        print("1. Encrypt\n2. Decrypt\n3. Exit")
        option = input("Select an option: ")

        if option == '1':
            password = ""
            while not password:
                password = input("Enter the password to encrypt: ").strip()
                if not password:
                    print("Password cannot be empty. Please try again.")
            method = input("Choose method: 1. Fernet 2. Blowfish 3. AES: ")
            if method == '1':
                encrypted_password = encrypt_fernet(password, store["fernet"]["key"])
            elif method == '2':
                encrypted_password = encrypt_blowfish(password, store["blowfish"]["key"])
            elif method == '3':
                encrypted_password = encrypt_aes(password, store["aes"]["key"])
            else:
                print("Invalid method.")
                continue
            print(f"Encrypted password: {encrypted_password}")
        
        elif option == '2':
            encrypted_password = input("Enter the encrypted password: ")
            decrypted_password = None

            # Attempt to decrypt with Fernet
            try:
                decrypted_password = decrypt_fernet(encrypted_password, store["fernet"]["key"])
                print(f"Decrypted password (Fernet): {decrypted_password}")
            except Exception:
                pass
            
            if not decrypted_password:
                # Attempt to decrypt with Blowfish
                try:
                    decrypted_password = decrypt_blowfish(encrypted_password, store["blowfish"]["key"])
                    print(f"Decrypted password (Blowfish): {decrypted_password}")
                except Exception:
                    pass

            if not decrypted_password:
                # Attempt to decrypt with AES
                try:
                    decrypted_password = decrypt_aes(encrypted_password, store["aes"]["key"])
                    print(f"Decrypted password (AES): {decrypted_password}")
                except Exception:
                    pass

            # If all methods fail, notify the user
            if not decrypted_password:
                print("Decryption failed for all methods. Please check if the input was correct.")

        elif option == '3':
            break
        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()
