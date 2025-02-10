from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os
import base64

# Constants
SALT_SIZE = 16  # Size of the salt
KEY_SIZE = 32   # AES-256 requires a 32-byte key
ITERATIONS = 100000  # Number of iterations for PBKDF2

# Generate a key from the master password
def derive_key(master_password, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=KEY_SIZE,
        salt=salt,
        iterations=ITERATIONS,
        backend=default_backend()
    )
    return kdf.derive(master_password.encode())

# Encrypt plaintext data
def encrypt_data(plain_text, key):
    iv = os.urandom(16)  # Initialization vector for AES
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    
    encrypted_data = encryptor.update(plain_text.encode()) + encryptor.finalize()
    
    # Combine IV and encrypted data, then encode to base64 for storage
    return base64.b64encode(iv + encrypted_data).decode('utf-8')

# Decrypt encrypted data
def decrypt_data(encrypted_data, key):
    encrypted_data = base64.b64decode(encrypted_data.encode('utf-8'))
    iv = encrypted_data[:16]  # Extract IV from the beginning
    cipher_text = encrypted_data[16:]  # The rest is the cipher text
    
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    
    decrypted_data = decryptor.update(cipher_text) + decryptor.finalize()
    return decrypted_data.decode('utf-8')

if __name__ == '__main__':
    # Example usage
    master_password = input("Enter your master password: ")
    salt = os.urandom(SALT_SIZE)
    key = derive_key(master_password, salt)

    text_to_encrypt = "MySecretPassword123"
    encrypted = encrypt_data(text_to_encrypt, key)
    print(f"Encrypted: {encrypted}")

    decrypted = decrypt_data(encrypted, key)
    print(f"Decrypted: {decrypted}")

