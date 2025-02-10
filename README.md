# Password Manager

A simple, secure password manager built with Python. This project uses encryption to securely store and manage your credentials, featuring a user-friendly GUI for easy interaction.

## Features

- **Master Password Authentication:** Secure access with a master password.
- **AES Encryption:** Credentials are encrypted using advanced encryption standards.
- **Credential Management:** Add, update, delete, and view stored credentials.
- **Password Generator:** Create strong, random passwords.
- **Clipboard Management:** Copy passwords to the clipboard with automatic clearing after 10 seconds.
- **Graphical User Interface:** Simple and intuitive interface built with `tkinter`.

## Download

- [Download for Windows](https://github.com/noahie-valk/basic-password-manager/archive/refs/tags/v1.0.0.zip)

*Note: Ensure you have the necessary permissions to run executables on your system.*

## Installation (For Development)

If you want to run or modify the source code:

### Prerequisites

- Python 3.x
- Virtual Environment (recommended)

### Setup Instructions

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/noahie-valk/basic-password-manager.git
   cd basic-password-manager
   ```

2. **Set Up Virtual Environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application:**
   ```bash
   python main.py
   ```

## Usage

1. **First Run:**
   - You'll be prompted to set a master password. This password is hashed and securely stored.

2. **Credential Management:**
   - Add, view, update, and delete credentials via the GUI.
   - Use the password generator to create strong, random passwords.

3. **Clipboard Management:**
   - Copy passwords to the clipboard with the click of a button. Passwords are automatically cleared from the clipboard after 10 seconds for security.

## Security Considerations

- **Encryption:** All credentials are encrypted using AES encryption.
- **Master Password:** The master password is hashed using `bcrypt` and never stored in plain text.
- **Clipboard Security:** Passwords copied to the clipboard are automatically cleared after a set timeout.

## Contributing

Contributions are welcome! Feel free to fork the repository and submit pull requests.

1. Fork the project.
2. Create your feature branch (`git checkout -b feature/YourFeature`).
3. Commit your changes (`git commit -m 'Add YourFeature'`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Open a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built using Python and `tkinter` for the GUI.
- Encryption powered by the `cryptography` library.

---

*Part of [Project Shark](https://noahie-valk.github.io/project-shark), documenting my journey in learning cybersecurity.*

