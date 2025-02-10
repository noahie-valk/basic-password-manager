import tkinter as tk
from tkinter import messagebox, simpledialog
import pyperclip
import time
from storage import add_credential, get_credentials, update_credential, delete_credential, generate_password
from encryption import derive_key
from auth import verify_master_password

# Initialize the main application window
class PasswordManagerApp(tk.Tk):
    def __init__(self, key):
        super().__init__()
        self.key = key
        self.title("Password Manager")
        self.geometry("500x500")
        
        # Create UI Elements
        self.create_widgets()
        self.refresh_credential_list()

    def create_widgets(self):
        # Add Credential Button
        tk.Button(self, text="Add Credential", command=self.add_credential).pack(pady=5)
        
        # Generate Password Button
        tk.Button(self, text="Generate Strong Password", command=self.generate_password).pack(pady=5)
        
        # Credential Listbox
        self.credential_listbox = tk.Listbox(self, width=60)
        self.credential_listbox.pack(pady=10)

        # Update, Delete, and Copy Buttons
        tk.Button(self, text="Update Credential", command=self.update_credential).pack(pady=5)
        tk.Button(self, text="Delete Credential", command=self.delete_credential).pack(pady=5)
        tk.Button(self, text="Copy Password to Clipboard", command=self.copy_password).pack(pady=5)

    def refresh_credential_list(self):
        self.credential_listbox.delete(0, tk.END)
        credentials = get_credentials(self.key)
        for cred in credentials:
            display_text = f"{cred['id']} | {cred['website']} | {cred['username']}"
            self.credential_listbox.insert(tk.END, display_text)

    def add_credential(self):
        website = simpledialog.askstring("Website", "Enter website:")
        username = simpledialog.askstring("Username", "Enter username:")
        password = simpledialog.askstring("Password", "Enter password:")
        if website and username and password:
            add_credential(website, username, password, self.key)
            messagebox.showinfo("Success", "Credential added successfully!")
            self.refresh_credential_list()

    def update_credential(self):
        selected = self.credential_listbox.curselection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a credential to update.")
            return
        
        credential_id = int(self.credential_listbox.get(selected[0]).split('|')[0].strip())
        website = simpledialog.askstring("Website", "Enter new website:")
        username = simpledialog.askstring("Username", "Enter new username:")
        password = simpledialog.askstring("Password", "Enter new password:")
        if website and username and password:
            update_credential(credential_id, website, username, password, self.key)
            messagebox.showinfo("Success", "Credential updated successfully!")
            self.refresh_credential_list()

    def delete_credential(self):
        selected = self.credential_listbox.curselection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a credential to delete.")
            return
        
        credential_id = int(self.credential_listbox.get(selected[0]).split('|')[0].strip())
        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this credential?")
        if confirm:
            delete_credential(credential_id)
            messagebox.showinfo("Deleted", "Credential deleted successfully!")
            self.refresh_credential_list()

    def generate_password(self):
        length = simpledialog.askinteger("Password Length", "Enter desired password length:", minvalue=8, maxvalue=32)
        if length:
            password = generate_password(length)
            messagebox.showinfo("Generated Password", f"Your generated password is:\n{password}")

    def copy_password(self):
        selected = self.credential_listbox.curselection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a credential to copy the password.")
            return
        
        credential_id = int(self.credential_listbox.get(selected[0]).split('|')[0].strip())
        credentials = get_credentials(self.key)
        selected_cred = next((cred for cred in credentials if cred['id'] == credential_id), None)
        
        if selected_cred:
            pyperclip.copy(selected_cred['password'])
            messagebox.showinfo("Copied", "Password copied to clipboard. It will be cleared in 10 seconds.")
            self.after(10000, lambda: pyperclip.copy(''))  # Clear clipboard after 10 seconds
        else:
            messagebox.showerror("Error", "Credential not found.")

if __name__ == '__main__':
    if verify_master_password():
        master_password = simpledialog.askstring("Master Password", "Re-enter your master password to derive encryption key:", show='*')
        salt = b'fixed_salt_value_here'  # Replace with actual stored/retrieved salt for better security
        key = derive_key(master_password, salt)
        
        app = PasswordManagerApp(key)
        app.mainloop()

