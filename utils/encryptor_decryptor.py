# ENCRYPTOR/DECRYPTOR (Python file)

from flask import Flask, request, jsonify
from Crypto.Cipher import Blowfish, AES
from Crypto.Util.Padding import pad, unpad
import base64
from cryptography.fernet import Fernet
import hashlib

# The text encryptor/decryptor uses symmetric encryption methods (the same key is used for both encryption and decryption)
# Algorithms used: Fernet, Blowfish and AES.

app = Flask(__name__)

# Function to hash the user-provided key for appropriate length (32 bytes for Fernet, 16 bytes for Blowfish and AES)
def format_key(key, method):
    if method == "Fernet":
        # Hash the key and encode it in base64 for Fernet
        return base64.urlsafe_b64encode(hashlib.sha256(key.encode()).digest())
    elif method in ["Blowfish", "AES"]:
        # Hash the key and return the first 16 bytes for Blowfish and AES
        return hashlib.sha256(key.encode()).digest()[:16]


# Encryption route
@app.route('/encrypt', methods=['POST'])
def encrypt():
    try:
        data = request.json
        text = data['text']
        key = data['key']
        method = data['method']

        formatted_key = format_key(key, method)

        if method == "Fernet":
            encrypted_text = Fernet(formatted_key).encrypt(text.encode()).decode()
        elif method == "Blowfish":
            cipher = Blowfish.new(formatted_key, Blowfish.MODE_CBC)
            iv = cipher.iv
            encrypted_text = base64.b64encode(iv + cipher.encrypt(pad(text.encode(), Blowfish.block_size))).decode()
        elif method == "AES":
            cipher = AES.new(formatted_key, AES.MODE_CBC)
            iv = cipher.iv
            encrypted_text = base64.b64encode(iv + cipher.encrypt(pad(text.encode(), AES.block_size))).decode()
        else:
            return jsonify({"error": "Invalid encryption method"}), 400

        return jsonify({"encrypted_text": encrypted_text}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Decryption route
@app.route('/decrypt', methods=['POST'])
def decrypt():
    try:
        data = request.json
        text = data['text']
        key = data['key']
        method = data['method']

        formatted_key = format_key(key, method)

        if method == "Fernet":
            decrypted_text = Fernet(formatted_key).decrypt(text.encode()).decode()
        elif method == "Blowfish":
            encrypted_data = base64.b64decode(text)
            iv = encrypted_data[:Blowfish.block_size]
            cipher = Blowfish.new(formatted_key, Blowfish.MODE_CBC, iv)
            decrypted_text = unpad(cipher.decrypt(encrypted_data[Blowfish.block_size:]), Blowfish.block_size).decode()
        elif method == "AES":
            encrypted_data = base64.b64decode(text)
            iv = encrypted_data[:AES.block_size]
            cipher = AES.new(formatted_key, AES.MODE_CBC, iv)
            decrypted_text = unpad(cipher.decrypt(encrypted_data[AES.block_size:]), AES.block_size).decode()
        else:
            return jsonify({"error": "Invalid decryption method"}), 400

        return jsonify({"decrypted_text": decrypted_text}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)