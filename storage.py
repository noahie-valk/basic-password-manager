import sqlite3
import os
import secrets
import string
import pyperclip
import time
from encryption import encrypt_data, decrypt_data, derive_key

# Constants
DB_FILE = 'credentials.db'

# Initialize the database
def initialize_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS credentials (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            website TEXT NOT NULL,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    
    conn.commit()
    conn.close()

# Add new credential
def add_credential(website, username, password, key):
    encrypted_password = encrypt_data(password, key)
    
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO credentials (website, username, password) VALUES (?, ?, ?)',
                   (website, username, encrypted_password))
    conn.commit()
    conn.close()
    print(f"Credential for {website} added successfully!")

# Retrieve and decrypt credentials
def get_credentials(key):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT id, website, username, password FROM credentials')
    
    credentials = []
    for id, website, username, encrypted_password in cursor.fetchall():
        decrypted_password = decrypt_data(encrypted_password, key)
        credentials.append({'id': id, 'website': website, 'username': username, 'password': decrypted_password})
    
    conn.close()
    return credentials

# Update existing credential
def update_credential(credential_id, website, username, password, key):
    encrypted_password = encrypt_data(password, key)
    
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE credentials 
        SET website = ?, username = ?, password = ? 
        WHERE id = ?
    ''', (website, username, encrypted_password, credential_id))
    conn.commit()
    conn.close()
    print(f"Credential ID {credential_id} updated successfully!")

# Delete a credential
def delete_credential(credential_id):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM credentials WHERE id = ?', (credential_id,))
    conn.commit()
    conn.close()
    print(f"Credential ID {credential_id} deleted successfully!")

# Generate a strong random password
def generate_password(length=16):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(characters) for _ in range(length))
    return password

# Copy password to clipboard with timeout
def copy_to_clipboard(password, timeout=10):
    pyperclip.copy(password)
    print(f"Password copied to clipboard. It will be cleared in {timeout} seconds.")
    time.sleep(timeout)
    pyperclip.copy('')
    print("Clipboard cleared.")

if __name__ == '__main__':
    from auth import verify_master_password

    if verify_master_password():
        initialize_db()
        
        master_password = input("Re-enter your master password to derive encryption key: ")
        salt = b'fixed_salt_value_here'  # Replace with actual stored/retrieved salt for better security
        key = derive_key(master_password, salt)

        while True:
            print("\nOptions:")
            print("1. Add Credential")
            print("2. View Credentials")
            print("3. Update Credential")
            print("4. Delete Credential")
            print("5. Generate Strong Password")
            print("6. Copy Password to Clipboard")
            print("7. Exit")
            choice = input("Choose an option: ")
            
            if choice == '1':
                website = input("Enter website: ")
                username = input("Enter username: ")
                password = input("Enter password: ")
                add_credential(website, username, password, key)
                
            elif choice == '2':
                credentials = get_credentials(key)
                for cred in credentials:
                    print(f"ID: {cred['id']}, Website: {cred['website']}, Username: {cred['username']}, Password: {cred['password']}")
                
            elif choice == '3':
                credential_id = int(input("Enter the ID of the credential to update: "))
                website = input("Enter new website: ")
                username = input("Enter new username: ")
                password = input("Enter new password: ")
                update_credential(credential_id, website, username, password, key)

            elif choice == '4':
                credential_id = int(input("Enter the ID of the credential to delete: "))
                delete_credential(credential_id)

            elif choice == '5':
                length = int(input("Enter desired password length (default 16): ") or 16)
                strong_password = generate_password(length)
                print(f"Generated Password: {strong_password}")
                
            elif choice == '6':
                credential_id = int(input("Enter the ID of the credential to copy: "))
                credentials = get_credentials(key)
                selected_cred = next((cred for cred in credentials if cred['id'] == credential_id), None)
                if selected_cred:
                    copy_to_clipboard(selected_cred['password'])
                else:
                    print("Credential not found.")
                
            elif choice == '7':
                print("Exiting Password Manager. Goodbye!")
                break
            else:
                print("Invalid option. Please try again.")

