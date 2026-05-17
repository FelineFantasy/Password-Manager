# 🔐 Password Manager by FelineFantasy

[![Python Version](https://img.shields.io/badge/python-3.x-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

A secure console-based password manager with encryption, password generator, and strength checker.

## 📋 Table of Contents
- [Description](#description)
- [How to Use](#how-to-use)
- [Installation](#installation)
- [Features](#features)
- [Security](#security)
- [Project Files](#project-files)
- [Author](#author)

## 📝 Description

**Password Manager** is a console utility for securely storing your passwords. All passwords are encrypted using **Fernet (cryptography library)** and stored locally. The program also includes a password generator and a strength checker.

### Features:
- 🔒 **Encryption** — Passwords are stored in encrypted form
- 🔑 **Key-based access** — A unique key is generated on first launch
- 🗑️ **Delete password** — Remove stored passwords you no longer need
- 🎲 **Password generator** — Create strong random passwords
- 📊 **Strength checker** — Evaluate password reliability
- 💾 **Local storage** — All data stays on your computer

## 🎮 How to Use

1. Run the program
2. Choose an action from the menu:
   - Save a new password
   - Delete a password
   - View all saved passwords
   - Generate a random password
   - Check password strength
3. To exit, select `0`

**Important:** On first launch, the program creates a `secret.key` file — **do not lose it!** Without this key, you won't be able to decrypt your passwords.

## ⚙️ Installation

### Option 1: Download ZIP
1. Click the green **"Code"** button on this page
2. Select **"Download ZIP"**
3. Extract the archive
4. Install dependencies: `pip install -r requirements.txt`
5. Run the program: `python password_manager.py`

### Option 2: Clone repository
```bash
git clone https://github.com/FelineFantasy/password-manager.git
cd password-manager
pip install -r requirements.txt
python password_manager.py
```

## 🛡️ Features

### Save Password
- Enter the app name and password
- Password is encrypted and saved to `password.txt`

### Delete Password
- Enter the app name
- The password entry is permanently removed from the file

### View Passwords
- Displays all saved passwords in decrypted form

### Generate Password
- Specify the desired length
- Generates a random password using letters, numbers, and special characters

### Check Strength
Analyzes password based on 5 criteria:
- Length ≥ 8 characters
- Contains digits
- Contains uppercase letters
- Contains lowercase letters
- Contains special characters (!@#\$%^&*)

## 🔐 Security

- **Encryption algorithm:** Fernet (symmetric encryption)
- **Key storage:** Separate `secret.key` file
- **Password storage:** `password.txt` with encrypted data only

⚠️ **Important:** 
- Never share your `secret.key` file
- Back up the key file if you don't want to lose access to your passwords
- Keep `password.txt` and `secret.key` in a safe place

## 📁 Project Files
```text
password-manager/
├── password_manager.py     # Main program file
├── requirements.txt        # Dependencies
├── password.txt            # Encrypted passwords (auto-created)
├── secret.key              # Encryption key (auto-created)
└── README.md               # Documentation
```

## 📋 Requirements

- Python 3.8+
- cryptography

## 👤 Author

**FelineFantasy**

License: MIT
