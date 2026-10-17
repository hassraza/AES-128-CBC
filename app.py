import base64
import re
import streamlit as st
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend

# -----------------------------------------------------------------------------
# Page Configuration & Clean Styling
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="CipherVault | AES-128 CBC",
    page_icon="🔒",
    layout="centered"
)

# Custom minimal CSS for balanced typography and clean spacing
st.markdown("""
<style>
    div[data-testid="stToolbar"] { visibility: hidden; height: 0%; position: fixed; }
    footer { visibility: hidden; height: 0%; }
    .main-title {
        font-size: 2.1rem;
        font-weight: 700;
        letter-spacing: -0.5px;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        color: #94a3b8;
        font-size: 0.95rem;
        margin-bottom: 1.5rem;
    }
    .badge-box {
        background-color: #1e293b;
        border: 1px solid #334155;
        border-radius: 8px;
        padding: 12px 16px;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">CipherVault — AES Secure Note Locker</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Bahria University Islamabad &bull; Information Security Assignment 2 (CLO-2)</div>', unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Cryptographic Operations
# -----------------------------------------------------------------------------
def run_encryption(plaintext: str, key_bytes: bytes, iv_bytes: bytes) -> str:
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(plaintext.encode("utf-8")) + padder.finalize()

    cipher = Cipher(algorithms.AES(key_bytes), modes.CBC(iv_bytes), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()

    combined = iv_bytes + ciphertext
    return base64.b64encode(combined).decode("utf-8")

def run_decryption(payload_b64: str, key_bytes: bytes) -> str:
    raw_payload = base64.b64decode(payload_b64.strip())
    if len(raw_payload) < 32:
        raise ValueError("Invalid payload: must contain at least 16 bytes IV and 16 bytes of ciphertext.")
    
    iv_bytes = raw_payload[:16]
    ciphertext = raw_payload[16:]

    cipher = Cipher(algorithms.AES(key_bytes), modes.CBC(iv_bytes), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_text = decryptor.update(ciphertext) + decryptor.finalize()

    unpadder = padding.PKCS7(128).unpadder()
    original_bytes = unpadder.update(padded_text) + unpadder.finalize()
    return original_bytes.decode("utf-8")

# -----------------------------------------------------------------------------
# Sidebar: Assignment Test Vector & Helpers
# -----------------------------------------------------------------------------
with st.sidebar:
    st.subheader("Test Vector Preset")
    st.caption("Load required assignment benchmark parameters:")
    
    if st.button("Populate Assignment Values", use_container_width=True):
        st.session_state["f_key"] = "0123456789abcdef"
        st.session_state["f_iv"] = "3a7f9c2e5b8d1f4a6c0e9d2b7f4a1c8e"
        st.session_state["f_pt"] = "This is a secret message for my assignment."
        st.session_state["f_fmt"] = "ASCII String (16 chars)"
        st.rerun()

    st.markdown("---")
    st.markdown("""
    **Rubric Parameters:**
    * **Key:** `0123456789abcdef`
    * **IV:** `3a7f9c2e5b8d1f4a...`
    * **Mode:** CBC with PKCS#7
    """)

# -----------------------------------------------------------------------------
# Tab Interface: 🔒 Encryption / 🔓 Decryption
# -----------------------------------------------------------------------------
tab_encrypt, tab_decrypt = st.tabs(["🔒 Encryption", "🔓 Decryption"])

with tab_encrypt:
    st.markdown("##### 🔒 Encrypt Note")
    
    col_fmt, col_key = st.columns([1, 2])
    with col_fmt:
        key_format = st.selectbox(
            "Key Input Type",
            ["ASCII String (16 chars)", "Hexadecimal (32 chars)"],
            index=0 if st.session_state.get("f_fmt") != "Hexadecimal (32 chars)" else 1,
            key="key_format_select"
        )
    with col_key:
        raw_key_input = st.text_input(
            "Secret Key",
            value=st.session_state.get("f_key", "0123456789abcdef"),
            help="16 ASCII characters or 32 hexadecimal characters (0-9, a-f)."
        )

    iv_hex_input = st.text_input(
        "Initialization Vector (IV in 32-char Hex)",
        value=st.session_state.get("f_iv", "3a7f9c2e5b8d1f4a6c0e9d2b7f4a1c8e"),
        max_chars=32,
        help="16-byte IV represented as 32 hex characters."
    )

    plaintext_input = st.text_area(
        "Plaintext Message",
        value=st.session_state.get("f_pt", "This is a secret message for my assignment."),
        height=90
    )

    if st.button("🔒 Run Encryption", type="primary", use_container_width=True):
        error_flag = False
        key_bytes = b""

        # Key Validation
        if key_format.startswith("ASCII"):
            if len(raw_key_input.encode("utf-8")) != 16:
                st.error("Key Error: ASCII key must be exactly 16 characters long.")
                error_flag = True
            else:
                key_bytes = raw_key_input.encode("utf-8")
        else:
            cleaned_hex = raw_key_input.strip()
            if not re.fullmatch(r"[0-9a-fA-F]{32}", cleaned_hex):
                st.error("Key Error: Hex key must contain exactly 32 hexadecimal characters (0-9, a-f).")
                error_flag = True
            else:
                key_bytes = bytes.fromhex(cleaned_hex)

        # IV Validation
        cleaned_iv = iv_hex_input.strip()
        if not re.fullmatch(r"[0-9a-fA-F]{32}", cleaned_iv):
            st.error("IV Error: IV must be exactly 32 hexadecimal characters (0-9, a-f).")
            error_flag = True
        else:
            iv_bytes = bytes.fromhex(cleaned_iv)

        if not error_flag:
            try:
                encrypted_b64 = run_encryption(plaintext_input, key_bytes, iv_bytes)
                st.success("Message Encrypted Successfully")
                st.markdown("**Base64 Encoded Output (IV + Ciphertext):**")
                st.code(encrypted_b64, language="text")

                # Store into decryption tab automatically for testing convenience
                st.session_state["last_ciphertext"] = encrypted_b64
            except Exception as e:
                st.error(f"Encryption failed: {str(e)}")

with tab_decrypt:
    st.markdown("##### 🔓 Decrypt Note")
    
    col_d_fmt, col_d_key = st.columns([1, 2])
    with col_d_fmt:
        dec_key_format = st.selectbox(
            "Key Input Type",
            ["ASCII String (16 chars)", "Hexadecimal (32 chars)"],
            key="dec_key_format_select"
        )
    with col_d_key:
        dec_key_input = st.text_input(
            "Secret Key for Decryption",
            value=st.session_state.get("f_key", "0123456789abcdef"),
            key="dec_key_field"
        )

    b64_cipher_input = st.text_area(
        "Base64 Encrypted String (IV + Ciphertext)",
        value=st.session_state.get("last_ciphertext", ""),
        placeholder="Paste Base64 payload here...",
        height=90
    )

    if st.button("🔓 Run Decryption", use_container_width=True):
        dec_error = False
        dec_key_bytes = b""

        if dec_key_format.startswith("ASCII"):
            if len(dec_key_input.encode("utf-8")) != 16:
                st.error("Key Error: Key must be exactly 16 characters.")
                dec_error = True
            else:
                dec_key_bytes = dec_key_input.encode("utf-8")
        else:
            cleaned_hex = dec_key_input.strip()
            if not re.fullmatch(r"[0-9a-fA-F]{32}", cleaned_hex):
                st.error("Key Error: Hex key must contain exactly 32 hexadecimal characters (0-9, a-f).")
                dec_error = True
            else:
                dec_key_bytes = bytes.fromhex(cleaned_hex)

        if not dec_error:
            if not b64_cipher_input.strip():
                st.warning("Please paste or generate a Base64 string to decrypt.")
            else:
                try:
                    decrypted_text = run_decryption(b64_cipher_input, dec_key_bytes)
                    st.success("Message Decrypted Successfully")
                    st.markdown("**Recovered Plaintext:**")
                    st.code(decrypted_text, language="text")
                except Exception as e:
                    st.error(f"Decryption failed: {str(e)}. Verify the key matches and padding is intact.")
