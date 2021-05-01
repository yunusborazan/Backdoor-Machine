from Crypto.Cipher import AES
from Crypto import Random
import random
import string


def pad(s):
    return s + b"\0" * (AES.block_size - len(s) % AES.block_size)


def encrypt(message, key):
    message = pad(message)
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return iv + cipher.encrypt(message)


def encrypt_file(file, key=None):
    if key is None:
        key = f"{''.join(random.choices(string.ascii_letters + string.digits, k=32))}".encode()
    with open(file, 'rb') as f:
        plaintext = f.read()
    encr = encrypt(plaintext, key)
    with open(file[:-4] + ".enc", 'wb') as f:
        f.write(encr)
    return key.decode()
