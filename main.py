from auth import verify_master_password
from encryption import derive_key
from ui import PasswordManagerApp
import tkinter as tk
from tkinter import simpledialog


def main():
    if verify_master_password():
        root = tk.Tk()
        root.withdraw()  # Hide the root window
        master_password = simpledialog.askstring(
            "Master Password",
            "Re-enter your master password to derive encryption key:",
            show='*'
        )
        salt = b'fixed_salt_value_here'  # Replace with actual stored/retrieved salt for better security
        key = derive_key(master_password, salt)

        app = PasswordManagerApp(key)
        app.mainloop()


if __name__ == '__main__':
    main()

