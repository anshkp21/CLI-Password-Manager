# 🔐 CLI Password Manager

A secure, command-line interface (CLI) password manager built with Python. This tool allows users to securely store, generate, and manage passwords locally using industry-standard encryption.

## ✨ Features

- **User Authentication:** Secure registration and login using `bcrypt` password hashing.
- **Encryption:** All stored passwords are encrypted using `cryptography.fernet` (AES symmetric encryption).
- **Password Generation:** Built-in generator for strong, random passwords (16 characters).
- **Password Strength Validator:** Ensures all saved passwords meet security criteria (length, uppercase, lowercase, numbers, symbols).
- **Expiry Tracking:** Set expiration dates for passwords to enforce regular rotation.
- **Local Storage:** Data is stored locally in a SQLite database (`passwords.db`).
- **Menu-Driven Interface:** Easy-to-use CLI menu for managing credentials.

## 🛠️ Tech Stack

- **Language:** Python 3
- **Database:** SQLite
- **Security Libraries:** 
  - `bcrypt` (Password Hashing)
  - `cryptography` (Encryption)
- **Interface:** CLI (Command Line Interface)

## 🚀 Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   cd YOUR_REPO_NAME
