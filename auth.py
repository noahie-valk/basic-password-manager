import bcrypt
import os

MASTER_PASSWORD_FILE = 'master.hash'

def set_master_password():
    password = input("Set your master password: ").encode('utf-8')
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())
    
    with open(MASTER_PASSWORD_FILE, 'wb') as f:
        f.write(hashed)
    print("Master password set successfully!")

def verify_master_password():
    if not os.path.exists(MASTER_PASSWORD_FILE):
        print("No master password found. Please set one.")
        set_master_password()
        return True

    password = input("Enter your master password: ").encode('utf-8')
    
    with open(MASTER_PASSWORD_FILE, 'rb') as f:
        stored_hash = f.read()
    
    if bcrypt.checkpw(password, stored_hash):
        print("Access granted!")
        return True
    else:
        print("Incorrect password. Access denied.")
        return False

if __name__ == '__main__':
    if verify_master_password():
        print("Welcome to the Password Manager!")

