import io
import streamlit as st
import os
import tempfile
from pathlib import Path
from PIL import Image
from cryptography.fernet import Fernet, InvalidToken
from script import (
    generate_key, load_key, get_key_from_password, generate_hmac,
    verify_hmac, check_password_strength, encrypt_file, decrypt_file
)

st.set_page_config(page_title="All-in-One Encryption-Decryption", layout="wide")

# Define common styling
st.markdown("""
    <style>
    .main { background-color: #f5f7fa; }
    h1, h2, h3, .stButton > button {
        font-family: 'Segoe UI', sans-serif;
    }
    .section {
        background-color: white;
        padding: 1.5em;
        border-radius: 10px;
        box-shadow: 0px 2px 8px rgba(0,0,0,0.1);
        margin-bottom: 2em;
    }
    footer { text-align: center; color: gray; margin-top: 2em; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: #2c3e50;'>🔐 Encryption & Decryption Tool</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Secure your Videos, Images, and Text files – all in one place.</p>", unsafe_allow_html=True)

# Tabs for each section
tabs = st.tabs(["🎞️ Video", "🖼️ Image", "📄 Text"])

# --------- VIDEO ENCRYPTION TAB ----------
# ---------- Functions for video encryption and decryption ----------
def xor_process_video(file_bytes, key):
    byte_array = bytearray(file_bytes)
    for i in range(len(byte_array)):
        byte_array[i] ^= key
    return bytes(byte_array)

# # --------- UI Starts Here ----------
# st.set_page_config(page_title="Video Encryption", layout="centered")

# tabs = st.tabs(["🎞️ Video Encryption"])

# --------- VIDEO ENCRYPTION TAB ----------
with tabs[0]:
    with st.container():
        st.markdown("### 🎞️ Video Encryption & Decryption", unsafe_allow_html=True)

        video_file = st.file_uploader("Upload a video file", type=["mp4", "avi", "mov"], key="vid_up")
        if video_file:
            st.video(video_file)
            st.success(f"Uploaded: {video_file.name}")

        key_vid = st.text_input("Enter a key for encryption (0-255)", key="vid_key")

        if key_vid and not key_vid.isdigit():
            st.error("Key must be a number between 0-255")
        elif key_vid and (int(key_vid) < 0 or int(key_vid) > 255):
            st.error("Key must be in range 0-255")

        col1, col2 = st.columns(2)

        # ---------- Encrypt Video ----------
        with col1:
            if st.button("Encrypt Video") and video_file and key_vid:
                key = int(key_vid)
                video_bytes = video_file.read()
                encrypted_bytes = xor_process_video(video_bytes, key)

                # Save encrypted file temporarily
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_enc_file:
                    temp_enc_file.write(encrypted_bytes)
                    temp_enc_path = temp_enc_file.name

                st.success("🔐 Video encrypted successfully!")
                st.download_button("Download Encrypted Video", data=encrypted_bytes,
                                   file_name=f"encrypted_{video_file.name}",
                                   mime="video/mp4")

        # ---------- Decrypt Video ----------
        with col2:
            dec_video = st.file_uploader("Upload encrypted file to decrypt", type=["mp4", "avi"], key="vid_decrypt")
            if st.button("Decrypt Video") and dec_video and key_vid:
                key = int(key_vid)
                encrypted_bytes = dec_video.read()
                decrypted_bytes = xor_process_video(encrypted_bytes, key)

                # Save decrypted video temporarily for preview
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_dec_file:
                    temp_dec_file.write(decrypted_bytes)
                    temp_dec_path = temp_dec_file.name

                st.success("✅ Decrypted video preview:")
                st.video(temp_dec_path)
                st.download_button("Download Decrypted Video", data=decrypted_bytes,
                                   file_name=f"decrypted_{dec_video.name}",
                                   mime="video/mp4")
                
# --------- IMAGE ENCRYPTION TAB ----------
with tabs[1]:
    with st.container():
        st.markdown("### 🖼️ Image Encryption & Decryption", unsafe_allow_html=True)
        image_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"], key="img_up")
        key_img = st.text_input("Enter a secret key for encryption (number)", key="img_key")

        col1, col2 = st.columns(2)

        # Encrypt Image Section
        with col1:
            if st.button("Encrypt Image"):
                if image_file and key_img:
                    try:
                        key = int(key_img)
                        image_bytes = image_file.read()
                        encrypted_data, already_encrypted = encrypt_image(image_bytes, key)

                        if already_encrypted:
                            st.warning("⚠️ The image appears to be already encrypted.")
                        else:
                            # Save encrypted file
                            encrypted_path = os.path.join(tempfile.gettempdir(), "encrypted_image.png")
                            # salt = os.urandom(16)
                            # # Save salt + encrypted file together (messedup here)
                            # with open(encrypted_path, "wb") as f:
                            #     f.write(salt + encrypted_data)

                            st.success("✅ Image encrypted successfully!")
                            st.download_button("⬇️ Download Encrypted Image", encrypted_data, file_name="encrypted_image.png")
                            # st.image("https://via.placeholder.com/200?text=Encrypted+Image")

                    except ValueError:
                        st.error("Key must be a number.")
                    except Exception as e:
                        st.error(f"Encryption failed: {e}")
                else:
                    st.warning("Please upload an image and enter a key.")

        # Decrypt Image Section
        with col2:
            dec_img_file = st.file_uploader("Upload encrypted image to decrypt", type=["png", "jpg", "jpeg"], key="img_decrypt")
            dec_key_img = st.text_input("Enter the decryption key (number)", key="img_dec_key")

            if st.button("Decrypt Image"):
                if dec_img_file and dec_key_img:
                    try:
                        key = int(dec_key_img)
                        encrypted_bytes = dec_img_file.read()
                        decrypted_data = decrypt_image(encrypted_bytes, key)

                        # Try to open as image to verify
                        try:
                            image = Image.open(io.BytesIO(decrypted_data))
                            st.success("✅ Decrypted image preview:")
                            st.image(image)
                            st.download_button("⬇️ Download Decrypted Image", decrypted_data, file_name="decrypted_image.png")
                        except Exception:
                            st.error("🚫 Decryption failed: Invalid key or corrupted image.")

                    except ValueError:
                        st.error("Key must be a number.")
                    except Exception as e:
                        st.error(f"Decryption failed: {e}")
                else:
                    st.warning("Please upload an encrypted image and enter a key.")


# --------- TEXT ENCRYPTION TAB ----------
with tabs[2]:
    with st.container():
        st.markdown("### 🔐 Text/File Encryption & Decryption", unsafe_allow_html=True)
        file_to_encrypt = st.file_uploader("Upload a file to encrypt (e.g. .txt, .pdf)", key="file_encrypt")
        password = st.text_input("Enter a strong password for encryption", type="password", key="enc_pwd")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Encrypt File"):
                if file_to_encrypt and password:
                    if not check_password_strength(password):
                        st.warning("⚠️ Password is too weak. Use at least 8 characters, mix of upper/lowercase, numbers, symbols.")
                    else:
                        try:
                            # Save uploaded file temporarily
                            with tempfile.NamedTemporaryFile(delete=False) as tmp_in:
                                tmp_in.write(file_to_encrypt.read())
                                tmp_in_path = tmp_in.name

                            # Use password-based encryption
                            salt = os.urandom(16)
                            key = get_key_from_password(password, salt)

                            # Read original file content
                            with open(tmp_in_path, "rb") as f:
                                original = f.read()

                            fernet = Fernet(key)
                            encrypted = fernet.encrypt(original)
                            hmac_value = generate_hmac(key, encrypted)

                            encrypted_path = tmp_in_path + ".encrypted"

                            # Save encrypted file with salt + encrypted + hmac
                            with open(encrypted_path, "wb") as encrypted_file:
                                encrypted_file.write(salt)         # Store salt
                                encrypted_file.write(encrypted)    # Store encrypted data
                                encrypted_file.write(hmac_value)   # Store HMAC

                            # Prepare download
                            with open(encrypted_path, "rb") as f:
                                encrypted_bytes = f.read()

                            st.success("✅ File encrypted successfully!")
                            st.download_button(
                                label="⬇️ Download Encrypted File",
                                data=encrypted_bytes,
                                file_name=os.path.basename(encrypted_path),
                            )
                            st.code(f"HMAC (save this to verify): {hmac_value.hex()[:64]}...", language="text")

                        except Exception as e:
                            st.error(f"Encryption failed: {e}")
                else:
                    st.warning("Upload a file and enter a password.")

        # Decrypt File
        with col2:
            file_to_decrypt = st.file_uploader("Upload encrypted file (.encrypted)", key="file_decrypt")
            dec_password = st.text_input("Enter password for decryption", type="password", key="dec_pwd")
            hmac_input = st.text_input("Enter original HMAC for verification", key="hmac_input")

            if st.button("Decrypt File"):
                if file_to_decrypt and dec_password and hmac_input:
                    try:
                        # Save encrypted file temporarily
                        with tempfile.NamedTemporaryFile(delete=False) as tmp_enc:
                            tmp_enc.write(file_to_decrypt.read())
                            tmp_enc_path = tmp_enc.name

                        key = get_key_from_password(dec_password, salt)
                        with open(tmp_enc_path, "rb") as f:
                            file_data = f.read()

                        salt = file_data[:16]  # Extract salt (first 16 bytes)
                        enc_content = file_data[16:]

                        # Save enc_content to a new temp file
                        with open(tmp_enc_path, "wb") as f:
                            f.write(enc_content)

                        key = get_key_from_password(dec_password, salt)

                        # Verify HMAC
                        if not verify_hmac(tmp_enc_path, key, bytes.fromhex(hmac_input)):
                            st.error("🚫 HMAC verification failed. File may be tampered with or wrong password.")
                        else:
                            dec_path = tmp_enc_path + ".dec"
                            decrypt_file(tmp_enc_path, dec_path, key)

                            # Read decrypted content
                            with open(dec_path, "rb") as f:
                                decrypted_bytes = f.read()

                            st.success("✅ File decrypted and verified successfully!")
                            st.download_button(
                                label="⬇️ Download Decrypted File",
                                data=decrypted_bytes,
                                file_name="decrypted_output",
                            )
                    except Exception as e:
                        st.error(f"Decryption failed: {e}")
                else:
                    st.warning("Upload encrypted file, enter password, and HMAC to proceed.")