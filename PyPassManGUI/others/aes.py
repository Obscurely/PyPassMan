import os
from Crypto.Cipher import AES
from Crypto import Random

enc_key_dir = 'PyPassMan_Files\\encryption.key'
nonce_key_dir = 'PyPassMan_Files\\nonce_encryption.key'


def load_keys():
    if 'PyPassMan_Files' in os.listdir():
        with open(enc_key_dir, 'rb') as f:
            key = f.read()
        with open(nonce_key_dir, 'rb') as f:
            nonce = f.read()
    else:
        with open('encryption.key', 'rb') as f:
            key = f.read()
        with open('nonce_encryption.key', 'rb') as f:
            nonce = f.read()

    return key, nonce


def gen_keys():
    if 'PyPassMan_Files' in os.listdir():
        key = Random.get_random_bytes(32)
        with open(enc_key_dir, 'wb') as key_file:
            key_file.write(key)
        encryption_cipher = AES.new(key, AES.MODE_EAX)
        with open(nonce_key_dir, 'wb') as nonce_key:
            nonce_key.write(encryption_cipher.nonce)
    else:
        key = Random.get_random_bytes(32)
        with open('encryption.key', 'wb') as key_file:
            key_file.write(key)
        encryption_cipher = AES.new(key, AES.MODE_EAX)
        with open('nonce_encryption.key', 'wb') as nonce_key:
            nonce_key.write(encryption_cipher.nonce)


def encrypt(data):
    key, nonce = load_keys()
    encryption_cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    encrypted_data = encryption_cipher.encrypt(data.encode('utf8'))
    encrypted_data = encrypted_data.hex()
    return encrypted_data


def decrypt(data):
    key, nonce = load_keys()
    decryption_cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    data = bytes.fromhex(data)
    decrypted_data = decryption_cipher.decrypt(data)
    return decrypted_data.decode('utf8')
