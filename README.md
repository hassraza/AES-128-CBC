# 🔐 AES-128 CBC Confidential Notes Locker

A lightweight, secure cryptographic web application built with **Python**, **Streamlit**, and the **Python Cryptography Hazmat API**. The application implements the Advanced Encryption Standard (AES) in **Cipher Block Chaining (CBC)** mode with **PKCS#7 padding** to securely store and retrieve confidential text notes.

Developed for **Bahria University Islamabad**, Department of Computer Sciences — *Information Security Assignment #2 (CLO-2)*.

---

## 🌐 Live Application Demo

Test and run the live deployment directly in your browser:
**[https://aesencyption.streamlit.app/](https://aesencyption.streamlit.app/)**

---

## 📌 Project Overview & Objectives

In modern cryptographic systems, raw block ciphers encrypt fixed blocks of data (128 bits / 16 bytes for AES). To safely encrypt arbitrary-length messages and avoid pattern leakage inherent in Electronic Codebook (ECB) mode, **Cipher Block Chaining (CBC)** mode is used along with **PKCS#7 padding**.

### Core Requirements Implemented
1. **AES-128 CBC Encryption:** Accepts arbitrary plaintext and a 16-byte secret key.
2. **Deterministic & Randomized IV Support:** Employs a 16-byte Initialization Vector (IV).
3. **PKCS#7 Block Padding:** Dynamically pads input messages to multiples of the 16-byte AES block size.
4. **Ciphertext Concatenation:** Prepends the 16-byte raw IV directly before the raw ciphertext (`IV + Ciphertext`).
5. **Base64 Encoding/Decoding:** Encodes the concatenated byte payload into clean Base64 for persistent text storage.
6. **Decryption & Unpadding:** Decodes Base64, splits the initial 16 bytes as the IV, decrypts the remaining payload, and cleanly removes PKCS#7 padding.
7. **Strict Input Validation:** Enforces valid 16-byte ASCII strings or 32-character hexadecimal keys/IVs using regex guards.

---
## 🔬 How It Works (Cryptographic Pipeline)

### 1. Encryption Workflow

```text
Plaintext String ("This is a secret message for my assignment.")
   │ (43 bytes)
   ▼
UTF-8 Encode ➔ Apply PKCS#7 Padding (+5 bytes of 0x05)
   │
   ▼
Padded Data Block (48 bytes total / 3 blocks of 16 bytes)
   │
   ▼
AES-128 CBC Encryptor (Key: 16 bytes, IV: 16 bytes)
   │
   ▼
Raw Ciphertext (48 bytes)
   │
   ▼
Concatenate: [ 16 bytes IV ] + [ 48 bytes Ciphertext ] = 64 bytes total
   │
   ▼
Base64 Encode
   │
   ▼
Final Storage Payload (88 ASCII characters)

**### 2. Decryption Workflow**

Base64 Storage Payload
   │
   ▼
Base64 Decode ➔ 64 bytes combined binary data
   │
   ├───────────────────────────────┬───────────────────────────────┐
   │ (First 16 bytes)              │ (Remaining 48 bytes)
   ▼                               ▼
Extracted IV (16 bytes)         Raw Ciphertext (48 bytes)
   │                               │
   └───────────────┬───────────────┘
                   ▼
       AES-128 CBC Decryptor (Key: 16 bytes + Extracted IV)
                   ▼
         Padded Plaintext Bytes (48 bytes)
                   ▼
       PKCS#7 Unpadding (Removes trailing 5 padding bytes)
                   ▼
         Original Plaintext Bytes (43 bytes)
                   ▼
              UTF-8 Decode
                   ▼
       Recovered Plaintext Note ("This is a secret...")
## 🧪 Assignment Benchmark Test Vector

The implementation strictly validates against the assigned reference vector:

| Parameter | Value |
|---|---|
| **Plaintext** | `This is a secret message for my assignment.` (43 bytes) |
| **Secret Key** | `0123456789abcdef` (16 bytes ASCII) |
| **Initialization Vector (IV)** | `3a7f9c2e5b8d1f4a6c0e9d2b7f4a1c8e` (16 bytes / 32 hex chars) |
| **PKCS#7 Padding** | 5 bytes (`0x05 0x05 0x05 0x05 0x05`) to reach 48 bytes |
| **Raw Payload** | 16 bytes IV + 48 bytes ciphertext = 64 bytes total |
| **Final Base64 Payload** | `On+cLluNH0psDp0rf0ocjuuV/wDqI4hFw0v7mPZ+qj/QfR6pmsE4/mR3eA48cZ4OQjD5aR1Q+vR9s+K3I5Y7qQ==` |

---

## 📂 Project Structure

```text
aes-encryption-app/
├── .streamlit/
│   └── config.toml          # Custom dark UI vault theme (60-30-10 palette)
├── app.py                   # Main Streamlit dashboard and cryptographic functions
├── requirements.txt         # Production dependencies
└── README.md                # Project documentation
