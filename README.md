# CipherVault — AES-128 CBC Confidential Notes Locker

A secure cryptographic application built using **Python**, **Streamlit**, and the **cryptography** library. This tool implements the Advanced Encryption Standard (AES) in **Cipher Block Chaining (CBC)** mode with **PKCS#7 padding** to encrypt and decrypt confidential text notes.

Developed for **Bahria University Islamabad**, Department of Computer Sciences — *Information Security Assignment #2 (CLO-2)*.

---

## Live Application Demo

Access the live web deployment:  
**https://aesencyption.streamlit.app/**

---

## System Overview

Block ciphers like AES operate on fixed block sizes (128 bits / 16 bytes). Arbitrary text requires both block alignment padding and a chaining mode to protect against identical-block leakage.

### Key Capabilities
* **AES-128 CBC Encryption:** Encrypts variable-length text notes using a 16-byte key and a 16-byte Initialization Vector (IV).
* **PKCS#7 Padding:** Automatically pads data to 16-byte blocks during encryption and strips padding cleanly upon decryption.
* **Payload Bundling:** Concatenates the raw 16-byte IV with the ciphertext and encodes the result in Base64 for safe transport and storage.
* **Strict Validation:** Enforces exact length constraints and validates hexadecimal patterns (`0-9`, `a-f`).

---

## Cryptographic Pipeline

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
```

---

### 2. Decryption Workflow

```text
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
```

---

## Assignment Benchmark Test Vector

| Parameter | Value |
|---|---|
| **Plaintext** | `This is a secret message for my assignment.` (43 bytes) |
| **Secret Key** | `0123456789abcdef` (16 bytes ASCII) |
| **Initialization Vector (IV)** | `3a7f9c2e5b8d1f4a6c0e9d2b7f4a1c8e` (16 bytes / 32 hex characters) |
| **PKCS#7 Padding** | 5 bytes added (`0x05 0x05 0x05 0x05 0x05`) to equal 48 bytes |
| **Combined Binary Output** | 16 bytes IV + 48 bytes ciphertext = 64 bytes total |
| **Base64 Result** | `On+cLluNH0psDp0rf0ocjuuV/wDqI4hFw0v7mPZ+qj/QfR6pmsE4/mR3eA48cZ4OQjD5aR1Q+vR9s+K3I5Y7qQ==` |

---

## Repository Files

```text
aes/
├── app.py              # Main application logic and UI
├── requirements.txt    # Runtime package requirements
└── README.md           # Documentation
```

---

## Local Setup & Run

1. Clone repository:
   ```bash
   git clone [https://github.com/](https://github.com/)<your-username>/aes.git
   cd aes
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run locally:
   ```bash
   streamlit run app.py
   ```

---

## Viva & Conceptual Notes

* **Why does CBC require an IV?**  
  In CBC mode, each plaintext block is XORed with the previous ciphertext block. The first block has no previous ciphertext block, so the IV serves as the initial state, ensuring identical plaintexts yield different ciphertexts.
* **Why can the IV be stored openly?**  
  The IV does not need to be confidential; it only needs to be unique and unpredictable to prevent replay and pattern analysis attacks.
* **How does PKCS#7 padding work?**  
  If $N$ bytes are required to fill the last 16-byte block, $N$ bytes (each carrying the numerical byte value of $N$) are appended. The decryptor inspects the last byte to safely strip the padding.
