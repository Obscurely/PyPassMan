# This file is specifically designed for the uses of this application and will not in others if not changed
# This file helps with only one command encrypting a file with AES 256 bits EAX mode and with b64encoding over it
import os
import base64
import platform
from Crypto.Cipher import AES
from Crypto import Random

# Checks the platform and assigns the location values accordingly
if platform.system() == "Windows":
    enc_key_dir = "PyPassMan_Files\\encryption.key"
    nonce_key_dir = "PyPassMan_Files\\nonce_encryption.key"
else:
    enc_key_dir = "PyPassMan_Files/encryption.key"
    nonce_key_dir = "PyPassMan_Files/nonce_encryption.key"


def load_keys():  # Loads the key and nonce and return them
    if "PyPassMan_Files" in os.listdir():
        with open(enc_key_dir, "rb") as f:
            key = f.read()
        with open(nonce_key_dir, "rb") as f:
            nonce = f.read()
    else:
        with open("encryption.key", "rb") as f:
            key = f.read()
        with open("nonce_encryption.key", "rb") as f:
            nonce = f.read()

    return key, nonce


def gen_keys():
    # generates keys based on where the program is executed
    if "PyPassMan_Files" in os.listdir():
        # Random 32 bytes string (256-bits enc key)
        key = Random.get_random_bytes(32)

        with open(enc_key_dir, "wb") as key_file:
            key_file.write(key)
        encryption_cipher = AES.new(key, AES.MODE_EAX)
        with open(nonce_key_dir, "wb") as nonce_key:
            nonce_key.write(encryption_cipher.nonce)
    else:
        # Random 32 bytes string (256-bits enc key)
        key = Random.get_random_bytes(32)

        with open("encryption.key", "wb") as key_file:
            key_file.write(key)
        encryption_cipher = AES.new(key, AES.MODE_EAX)
        with open("nonce_encryption.key", "wb") as nonce_key:
            nonce_key.write(encryption_cipher.nonce)


def b64encode(data: str):
    data = data.encode("ascii")
    encoded_data = base64.b64encode(data)
    encoded_data = encoded_data.decode("ascii")
    return encoded_data


def b64decode(data: str):
    data = data.encode("ascii")
    decoded_data = base64.b64decode(data)
    decoded_data = decoded_data.decode("ascii")
    return decoded_data


def encrypt(data: str):
    key, nonce = load_keys()
    encryption_cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    data = b64encode(data)
    encrypted_data = encryption_cipher.encrypt(data.encode("utf8"))
    encrypted_data = encrypted_data.hex()
    return encrypted_data


def decrypt(data: str):
    key, nonce = load_keys()
    decryption_cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    data = bytes.fromhex(data)
    decrypted_data = decryption_cipher.decrypt(data).decode("utf8")
    decrypted_data = b64decode(decrypted_data)
    return decrypted_data
