from Crypto.PublicKey import RSA

def generate_keys(key_size=2048):
    key = RSA.generate(key_size)
    return key, key.publickey()

def save_keys_to_pem(private_key, public_key, private_filename="instructor_private.pem", public_filename="instructor_public.pem"):
    with open(private_filename, "wb") as f:
        f.write(private_key.export_key(format='PEM'))
    
    with open(public_filename, "wb") as f:
        f.write(public_key.export_key(format='PEM'))
