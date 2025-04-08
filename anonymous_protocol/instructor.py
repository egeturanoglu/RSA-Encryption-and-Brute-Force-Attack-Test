import secrets
import string
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256

class Instructor:
    def __init__(self, student_names, private_key, public_key):
        self.student_names = student_names
        self.private_key = private_key
        self.public_key = public_key
        self.credentials = {}  
    
    def issue_credentials(self):
        for name in self.student_names:
            token = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(16))
            h = SHA256.new(token.encode())
            signature = pkcs1_15.new(self.private_key).sign(h)
            self.credentials[token] = {"name": name, "signature": signature}
        return self.credentials
    
    def verify_credential(self, token, signature):
        try:
            h = SHA256.new(token.encode())
            pkcs1_15.new(self.public_key).verify(h, signature)
            return True
        except (ValueError, TypeError):
            return False
