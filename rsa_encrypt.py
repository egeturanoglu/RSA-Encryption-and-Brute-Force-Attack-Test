# rsa_encrypt.py
import random
from Crypto.Util.number import getPrime, inverse
import sys

def generate_rsa_keys(bit_length):
    p = getPrime(bit_length)
    q = getPrime(bit_length)
    n = p * q
    phi = (p - 1) * (q - 1)

    # Use small e for small key sizes
    if bit_length < 16:
        e = 17
    else:
        e = 65537

    while True:
        try:
            d = inverse(e, phi)
            break
        except ValueError:
            e += 2  # Try next odd number
    return (e, n), (d, n)


def str_to_int(message):
    return int.from_bytes(message.encode(), byteorder='big')

def int_to_str(value):
    try:
        length = (value.bit_length() + 7) // 8
        return value.to_bytes(length, byteorder='big').decode()
    except:
        return "<[decode error]>"

def encrypt(message, public_key):
    m = str_to_int(message)
    e, n = public_key
    if m >= n:
        raise ValueError(f"Message integer too large for modulus n={n}.")
    return pow(m, e, n)

def decrypt(ciphertext, private_key):
    d, n = private_key
    m = pow(ciphertext, d, n)
    return int_to_str(m)

if __name__ == "__main__":
    message = "a"
    message_int = str_to_int(message)
    print(f"Message as int: {message_int}")

    for bits in [2, 4, 8, 16, 32]:
        print(f"\n--- {bits}-bit RSA ---")
        public, private = generate_rsa_keys(bits)

        try:
            if message_int >= public[1]:  # if message too big for n
                print(f"⚠️ Skipping {bits}-bit: message too large for modulus n={public[1]}")
                continue

            encrypted = encrypt(message, public)
            decrypted = decrypt(encrypted, private)
            print(f"Public Key: {public}")
            print(f"Private Key: {private}")
            print(f"Encrypted: {encrypted}")
            print(f"Decrypted: {decrypted}")

        except Exception as e:
            print(f"❌ Error at {bits}-bit: {e}")
