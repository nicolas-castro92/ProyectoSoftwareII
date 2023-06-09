import string
import random
import hashlib

def generate_random_password(length=29):
    digits = string.digits
    return ''.join(random.choice(digits) for _ in range(length))

def hash_password(password):
    # Aplicar el algoritmo SHA-256 para encriptar la contraseña
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    return hashed_password