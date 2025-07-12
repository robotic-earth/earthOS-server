import hashlib
import os 

def hash_password(password):
    salt = os.urandom(16)
    hashed = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 1000)
    return salt + hashed



def verify_password(stored, input_password):
    salt = stored[:16]
    stored_hash = stored[16:]
    input_hash = hashlib.pbkdf2_hmac('sha256', input_password.encode(), salt, 1000)
    return stored_hash == input_hash
