import streamlit as st
from cryptography.fernet import Fernet
import base64
import os

# Helper functions
def generate_key():
    return Fernet.generate_key()

def encrypt_file_with_key(file_bytes, key):
    fernet = Fernet(key)
    return fernet.encrypt(file_bytes)

def decrypt_file_with_key(file_bytes, key):
    fernet = Fernet(key)
    return fernet.decrypt(file_bytes)

# Password-based encryption (basic, not strong – just for demo)
def derive_key_from_password(password: str):
    return base64.urlsafe_b64encode(password.encode("utf-8").ljust(32)[:32])

# Streamlit UI
st.title("🔐 Encryption & Decryption Tool")

tabs = st.tabs(["Text", "Image", "Video"])

with tabs[0]:
    st.subheader("🔤 Text File Encryption/Decryption")

    st.markdown("### 🔑 Using Secret Key")

    uploaded_file_key = st.file_uploader("Upload a file to encrypt/decrypt", key="file_key")

    key_input = st.text_input("Enter your Secret Key (or generate below)", type="password")
    if st.button("Generate Secret Key"):
        generated_key = generate_key()
        st.success(f"Generated Key: `{generated_key.decode()}`")

    col1, col2 = st.columns(2)
    if col1.button("Encrypt with Key"):
        if uploaded_file_key and key_input:
            key = key_input.encode()
            data = uploaded_file_key.read()
            encrypted = encrypt_file_with_key(data, key)
            st.download_button("⬇️ Download Encrypted File", encrypted, file_name="encrypted.txt")
        else:
            st.error("Please upload a file and enter your secret key.")

    if col2.button("Decrypt with Key"):
        if uploaded_file_key and key_input:
            key = key_input.encode()
            try:
                data = uploaded_file_key.read()
                decrypted = decrypt_file_with_key(data, key)
                st.download_button("⬇️ Download Decrypted File", decrypted, file_name="decrypted.txt")
            except Exception as e:
                st.error(f"Decryption failed: {str(e)}")
        else:
            st.error("Please upload a file and enter your secret key.")

    st.markdown("---")
    st.markdown("### 🔐 Using Password")

    uploaded_file_pass = st.file_uploader("Upload a file to encrypt/decrypt (Password)", key="file_pass")

    password_input = st.text_input("Enter your Password", type="password")

    col3, col4 = st.columns(2)
    if col3.button("Encrypt with Password"):
        if uploaded_file_pass and password_input:
            key = derive_key_from_password(password_input)
            data = uploaded_file_pass.read()
            encrypted = encrypt_file_with_key(data, key)
            st.download_button("⬇️ Download Encrypted File", encrypted, file_name="encrypted.txt")
        else:
            st.error("Please upload a file and enter your password.")

    if col4.button("Decrypt with Password"):
        if uploaded_file_pass and password_input:
            key = derive_key_from_password(password_input)
            try:
                data = uploaded_file_pass.read()
                decrypted = decrypt_file_with_key(data, key)
                st.download_button("⬇️ Download Decrypted File", decrypted, file_name="decrypted.txt")
            except Exception as e:
                st.error(f"Decryption failed: {str(e)}")
        else:
            st.error("Please upload a file and enter your password.")
