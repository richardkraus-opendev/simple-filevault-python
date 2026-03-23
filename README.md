# FileVault

**FileVault** is a secure and easy-to-use CLI tool for file encryption and decryption using **AES-256-GCM** with password-based key derivation. It ensures both **confidentiality and integrity** of your files.

---

## Features

- AES-256 encryption in **GCM mode** (authenticated encryption)
- Password-based key derivation using **PBKDF2** with SHA-256
- Detects tampering: ensures data integrity
- Simple CLI interface with `encrypt` and `decrypt` commands
- Clean, modular Python architecture

---

## Installation

Clone the repository and install in editable mode:

```bash
git clone https://github.com/richardkraus-opendev/simple-filevault-python.git
cd simple-filevault-python

python3 -m venv venv
source venv/bin/activate

pip install -e .
```
> The -e option installs FileVault in editable mode, so you can run the filevault command directly in the virtual environment.
---

## Usage

 - Encrypt a file:
```bash   
filevault encrypt -f input.txt -p yourpassword
```
 - Decrypt a file:
```bash   
filevault decrypt -f input.txt.enc -p yourpassword
```
### Optional output

Specify a custom output file:
```bash
filevault encrypt -f input.txt -p yourpassword -o secret.enc
```
```bash
filevault decrypt -f secret.enc -p yourpassword -o decrypted.txt
```

---

## Output behavior

Default output if --output is not provided:
 - Encryption: adds .enc extension
 - Decryption:
  - .enc → restores original filename
  - Other → .dec is appended

> **Overwrite warning:** FileVault will warn if the output file already exists or matches the input file.
