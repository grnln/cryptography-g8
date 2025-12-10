from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

import os

def init_cipher(nonce):
    if os.path.exists('aes.key'):
        with open('aes.key', mode = 'rb') as f:
            key = f.read()
    else:
        key = get_random_bytes(32)
    
        with open('aes.key', mode = 'wb') as f:
            f.write(key)

    return AES.new(key, AES.MODE_GCM, nonce = nonce)

def cipher_text(t):
    nonce = get_random_bytes(16)
    text, tag = init_cipher(nonce).encrypt_and_digest(bytearray(t, encoding = 'utf-8'))
    return nonce + tag + text

def decipher_text(t):
    nonce = t[:16]
    tag = t[16:32]
    text = t[32:]
    return init_cipher(nonce).decrypt_and_verify(text, tag).decode(encoding = 'utf-8')