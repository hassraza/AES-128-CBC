import base64
import streamlit as st
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend

# Page Configuration
st.set_page_config(page_title="AES-128 CBC Vault", page_icon="🔐", layout="wide")

st.title("🔐 AES-128 CBC Confidential Notes Vault")
st.caption("Bahria University Islamabad | Information Security Assignment #2 (CLO-2)")

# Core Encryption Function
def encrypt_aes_cbc(plaintext: str, key_bytes: bytes, iv_bytes: bytes) -> str:
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(plaintext.encode("utf-8")) + padder.finalize()

    cipher = Cipher(algorithms.AES(key_bytes), modes.CBC(iv_bytes), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()

    combined = iv_bytes + ciphertext
    return base64.b64encode(combined).decode("utf-8")

# Core Decryption Function
def decrypt_aes_cbc(b64_payload: str, key_bytes: bytes) -> str:
    combined = base64.b64decode(b64_payload.strip())
    if len(combined) < 32:
        raise ValueError("Payload must contain at least a 16-byte IV and one 16-byte block.")

    iv_bytes = combined[:16]
    ciphertext = combined[16:]

    cipher = Cipher(algorithms.AES(key_bytes), modes.CBC(iv_bytes), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()

    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    plaintext_bytes = unpadder.update(padded_plaintext) + unpadder.finalize()
    return plaintext_bytes.decode("utf-8")

# Sidebar Test Vector Loader
with st.sidebar:
    st.header("📋 Assignment Test Vector")
    st.markdown("""
    - **Key:** `0123456789abcdef`
    - **IV:** `3a7f9c2e5b8d1f4a6c0e9d2b7f4a1c8e`
    - **Plaintext:** `This is a secret message for my assignment.`
    """)
    if st.button("Load Test Vector Data"):
        st.session_state["pt_input"] = "This is a secret message for my assignment."
        st.session_state["key_input"] = "0123456789abcdef"
        st.session_state["iv_input"] = "3a7f9c2e5b8d1f4a6c0e9d2b7f4a1c8e"
        st.rerun()

# Main Tabs
tab_enc, tab_dec = st.tabs(["🔒 Encryption Module", "🔓 Decryption Module"])

with tab_enc:
    st.subheader("Encrypt Plaintext Note")
    col1, col2 = st.columns(2)
    with col1:
        key_str = st.text_input(
            "Secret Key (16 ASCII characters):",
            value=st.session_state.get("key_input", "0123456789abcdef"),
            max_chars=16,
            key="enc_key"
        )
    with col2:
        iv_hex = st.text_input(
            "Initialization Vector (32 Hex characters = 16 bytes):",
            value=st.session_state.get("iv_input", "3a7f9c2e5b8d1f4a6c0e9d2b7f4a1c8e"),
            max_chars=32,
            key="enc_iv"
        )

    plaintext_str = st.text_area(
        "Plaintext Note:",
        value=st.session_state.get("pt_input", "This is a secret message for my assignment."),
        height=100
    )

    if st.button("🔒 Run Encryption", type="primary"):
        if len(key_str.encode("utf-8")) != 16:
            st.error("Error: Key must be exactly 16 bytes.")
        else:
            try:
                iv_bytes = bytes.fromhex(iv_hex.strip())
                if len(iv_bytes) != 16:
                    st.error("Error: IV must be exactly 16 bytes (32 hex characters).")
                else:
                    key_bytes = key_str.encode("utf-8")
                    result_b64 = encrypt_aes_cbc(plaintext_str, key_bytes, iv_bytes)
                    st.success("Encryption Successful!")
                    st.code(result_b64, language="text")
            except Exception as e:
                st.error(f"Error during encryption: {e}")

with tab_dec:
    st.subheader("Decrypt Stored Note")
    dec_key_str = st.text_input(
        "Secret Key (16 ASCII characters):",
        value=st.session_state.get("key_input", "0123456789abcdef"),
        max_chars=16,
        key="dec_key"
    )
    b64_payload = st.text_area(
        "Stored Payload (Base64 string):",
        value="",
        placeholder="Paste your Base64 encrypted string here..."
    )

    if st.button("🔓 Run Decryption", type="primary"):
        if len(dec_key_str.encode("utf-8")) != 16:
            st.error("Error: Key must be exactly 16 bytes.")
        elif not b64_payload.strip():
            st.warning("Please provide a Base64 payload.")
        else:
            try:
                dec_key_bytes = dec_key_str.encode("utf-8")
                decrypted_text = decrypt_aes_cbc(b64_payload, dec_key_bytes)
                st.success("Decryption Successful!")
                st.code(decrypted_text, language="text")
            except Exception as e:
                st.error(f"Decryption failed: {e}")
