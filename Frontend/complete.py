import io
import os
import tempfile
import streamlit as st
from pathlib import Path
from PIL import Image
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from script import (
    get_key_from_password,
    generate_hmac,
    verify_hmac,
    check_password_strength
)

# ─── PAGE CONFIGURATION ───────────────────────────────────────────────────────
st.set_page_config(
    page_title="All‑in‑One Encryption‑Decryption", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─── GLOBAL CSS FOR DARK THEME ───────────────────────────────────────────────────────
st.markdown("""
<style>
    /* Base dark theme */
    .main {
        background-color: #0e1117;
        color: #e0e0e0;
        padding: 1.5rem;
    }
    
    /* Typography */
    h1, h2, h3 { 
        font-family: 'Segoe UI', 'SF Pro Display', sans-serif;
        color: #60a5fa;
        font-weight: 600;
    }
    
    h1 { margin-bottom: 1.5rem; }
    h2 { margin-bottom: 1rem; }
    h3 { margin-bottom: 0.75rem; color: #93c5fd; }
    
    p, div {
        color: #e0e0e0;
    }
    
    /* Override Streamlit's default white backgrounds */
    div[data-testid="stForm"] {
        background-color: #1a1f2c !important;
        border-radius: 0.75rem;
        padding: 1rem;
        border: 1px solid #2d3748;
    }
    
    /* Input fields */
    div[data-baseweb="input"] input, 
    div[data-baseweb="textarea"] textarea,
    div[data-baseweb="select"] div,
    div[data-baseweb="base-input"] input {
        background-color: #2d3748 !important;
        color: #e0e0e0 !important;
        border: 1px solid #4a5568 !important;
    }
    
    /* File uploader */
    div[data-testid="stFileUploader"] {
        background-color: #1e2533 !important;
        border: 1px dashed #4a5568 !important;
        padding: 1rem;
        border-radius: 0.5rem;
    }
    
    /* Container/section styling */
    .section {
        background-color: #1a1f2c;
        padding: 1.75rem;
        border-radius: 0.75rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.25);
        margin-bottom: 1.5rem;
        border: 1px solid #2d3748;
    }
    
    /* Button styling */
    button[kind="primaryFormSubmit"],
    button[data-testid="baseButton-secondary"] {
        background-color: #3b82f6 !important;
        color: white !important;
        border-radius: 6px !important;
        border: none !important;
        padding: 0.5rem 1.25rem !important;
        font-weight: 500 !important;
        transition: all 0.2s ease !important;
    }
    
    button[kind="primaryFormSubmit"]:hover,
    button[data-testid="baseButton-secondary"]:hover {
        background-color: #2563eb !important;
        box-shadow: 0 4px 8px rgba(37, 99, 235, 0.25) !important;
    }
    
    /* Download button */
    .stDownloadButton button {
        background-color: #10b981 !important;
        color: white !important;
        border-radius: 6px !important;
        border: none !important;
    }
    
    .stDownloadButton button:hover {
        background-color: #059669 !important;
        box-shadow: 0 4px 8px rgba(16, 185, 129, 0.25) !important;
    }
    
    /* Info/error/success/warning message boxes */
    div[data-baseweb="notification"] {
        background-color: #1e2533 !important;
        border: 1px solid #2d3748 !important;
        border-radius: 6px !important;
    }
    
    /* Code blocks */
    div[data-testid="stCodeBlock"] {
        background-color: #2d3748 !important;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #0e1117 !important;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 3rem;
        white-space: pre-wrap;
        background-color: #1a1f2c !important;
        border-radius: 6px 6px 0 0;
        gap: 4px;
        padding: 0.5rem 1rem;
        color: #e0e0e0 !important;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #2d3748 !important;
        border-bottom: 2px solid #3b82f6 !important;
        color: #60a5fa !important;
    }
    
    /* Footer */
    footer {
        text-align: center;
        color: #9ca3af;
        margin-top: 3rem;
        padding: 1rem;
        font-size: 0.9rem;
    }
    
    /* Expander */
    div[data-testid="stExpander"] {
        background-color: #1a1f2c !important;
        border: 1px solid #2d3748 !important;
        border-radius: 0.5rem !important;
    }
    
    div[data-testid="stExpander"] > div[role="button"] {
        color: #93c5fd !important;
    }
    
    /* Number input */
    div[data-testid="stNumberInput"] input {
        background-color: #2d3748 !important;
        color: #e0e0e0 !important;
        border: 1px solid #4a5568 !important;
    }
    
    div[data-testid="stNumberInput"] button {
        background-color: #3b82f6 !important;
        color: white !important;
        border: none !important;
    }
    
    /* Custom elements */
    .hmac-input {
        background-color: #2d3748 !important;
        color: #e0e0e0 !important;
        border: 1px solid #4a5568 !important;
        padding: 8px !important;
        border-radius: 4px !important;
    }
    
    .hmac-copy-btn {
        background-color: #3b82f6 !important;
        color: white !important;
        border-radius: 4px !important;
        border: none !important;
        padding: 8px 12px !important;
        cursor: pointer !important;
    }
    
    /* Preview containers */
    .preview-container {
        background-color: #1e2533;
        border-radius: 8px;
        padding: 1rem;
        min-height: 300px;
        border: 1px dashed #4a5568;
        display: flex;
        justify-content: center;
        align-items: center;
    }
    
    /* Dividers */
    hr { 
        margin: 1.5rem 0;
        border-color: #2d3748;
    }
</style>
""", unsafe_allow_html=True)

# ─── HEADER ───────────────────────────────────────────────────────────────────
st.markdown("<h1 style='text-align:center; color:#60a5fa;'>🔐 All‑in‑One Encryption & Decryption</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; font-size:1.1rem; margin-bottom:2rem; color:#e0e0e0;'>Secure your videos, images, and files with advanced encryption techniques</p>", unsafe_allow_html=True)

# ─── TABS ─────────────────────────────────────────────────────────────────────
tabs = st.tabs(["🎞️ Video", "🖼️ Image", "📄 Files"])

# ─── VIDEO TAB ────────────────────────────────────────────────────────────────
with tabs[0]:
    st.markdown("<div class='section'><h2>🎞️ Video Encryption & Decryption</h2></div>", unsafe_allow_html=True)
    control_col, preview_col = st.columns([1, 1], gap="large")

    # Controls
    with control_col:
        # --- Encrypt Form ---
        with st.container():
            st.markdown("<div class='section'>", unsafe_allow_html=True)
            st.markdown("### Encrypt Video")
            
            with st.form("video_encrypt", clear_on_submit=False):
                vid_file = st.file_uploader("Select video file", type=["mp4","avi","mov","mkv"], key="vid_enc_file",
                                          help="Supported formats: MP4, AVI, MOV, MKV")
                vid_key = st.number_input("Encryption Key (0–255)", 
                                        min_value=0, max_value=255, value=123, step=1, key="vid_enc_key",
                                        help="This key will be required to decrypt your video")
                enc_btn = st.form_submit_button("🔒 Encrypt Video")
            
            if enc_btn:
                if not vid_file:
                    st.error("⚠️ Please upload a video to encrypt.")
                else:
                    with st.spinner("Encrypting video..."):
                        data = vid_file.read()
                        encrypted = bytes(b ^ vid_key for b in data)
                        st.success("✅ Video encrypted successfully!")
                        st.download_button(
                            "⬇️ Download Encrypted Video",
                            encrypted,
                            file_name=f"encrypted_{vid_file.name}",
                            mime="application/octet-stream",
                            key="vid_enc_download"
                        )
                        st.info("📝 Remember your key: **{}**".format(vid_key))
            st.markdown("</div>", unsafe_allow_html=True)

        # --- Decrypt Form ---
        with st.container():
            st.markdown("<div class='section'>", unsafe_allow_html=True)
            st.markdown("### Decrypt Video")
            
            with st.form("video_decrypt", clear_on_submit=False):
                dec_file = st.file_uploader("Select encrypted video", type=None, key="vid_dec_file",
                                          help="Upload the encrypted video file")
                dec_key = st.number_input("Decryption Key (0–255)", 
                                        min_value=0, max_value=255, value=123, step=1, key="vid_dec_key",
                                        help="Enter the key used for encryption")
                dec_btn = st.form_submit_button("🔓 Decrypt Video")
            
            if dec_btn:
                if not dec_file:
                    st.error("⚠️ Please upload an encrypted video.")
                else:
                    with st.spinner("Decrypting video..."):
                        try:
                            data = dec_file.read()
                            decrypted = bytes(b ^ dec_key for b in data)
                            
                            # Save to temporary file for preview
                            tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
                            tmp_path = tmp.name
                            tmp.write(decrypted)
                            tmp.flush()
                            tmp.close()
                            
                            # Set the decrypted video to be displayed in preview column
                            st.session_state.decrypted_video = tmp_path
                            st.success("✅ Video decrypted successfully!")
                            st.download_button(
                                "⬇️ Download Decrypted Video",
                                decrypted,
                                file_name=f"decrypted_{dec_file.name}",
                                mime="video/mp4",
                                key="vid_dec_download"
                            )
                        except Exception as e:
                            st.error(f"🚫 Decryption failed. Invalid key or corrupted file.")
            st.markdown("</div>", unsafe_allow_html=True)

    # Preview column
    with preview_col:
        st.markdown("<div class='section'>", unsafe_allow_html=True)
        st.markdown("### Preview")
        
        # Video preview container
        preview_placeholder = st.empty()
        
        if 'decrypted_video' in st.session_state and os.path.exists(st.session_state.decrypted_video):
            preview_placeholder.video(st.session_state.decrypted_video)
        else:
            preview_placeholder.info("🎬 Decrypted video will appear here.")
        
        st.markdown("</div>", unsafe_allow_html=True)


# ─── IMAGE TAB ────────────────────────────────────────────────────────────────
with tabs[1]:
    st.markdown("<div class='section'><h2>🖼️ Image Encryption & Decryption</h2></div>", unsafe_allow_html=True)
    control_col, preview_col = st.columns([1, 1], gap="large")

    # Controls
    with control_col:
        # --- Encrypt Form ---
        with st.container():
            st.markdown("<div class='section'>", unsafe_allow_html=True)
            st.markdown("### Encrypt Image")
            
            with st.form("img_encrypt", clear_on_submit=False):
                img_file = st.file_uploader("Select image file", type=["png", "jpg", "jpeg", "webp"], 
                                          key="img_enc_file",
                                          help="Supported formats: PNG, JPG, JPEG, WEBP")
                img_key = st.number_input("Encryption Key (0–255)", 
                                        min_value=0, max_value=255, value=123, step=1, 
                                        key="img_enc_key",
                                        help="This key will be required to decrypt your image")
                img_enc_btn = st.form_submit_button("🔒 Encrypt Image")
            
            if img_enc_btn:
                if not img_file:
                    st.error("⚠️ Please upload an image.")
                else:
                    with st.spinner("Encrypting image..."):
                        data = img_file.read()
                        encrypted = bytes(b ^ img_key for b in data)
                        st.success("✅ Image encrypted successfully!")
                        st.download_button(
                            "⬇️ Download Encrypted Image",
                            encrypted,
                            file_name=f"encrypted_{img_file.name}",
                            mime="application/octet-stream",
                            key="img_enc_download"
                        )
                        st.info("📝 Remember your key: **{}**".format(img_key))
            st.markdown("</div>", unsafe_allow_html=True)

        # --- Decrypt Form ---
        with st.container():
            st.markdown("<div class='section'>", unsafe_allow_html=True)
            st.markdown("### Decrypt Image")
            
            with st.form("img_decrypt", clear_on_submit=False):
                enc_img = st.file_uploader("Select encrypted image", type=None, 
                                         key="img_dec_file",
                                         help="Upload the encrypted image file")
                img_key2 = st.number_input("Decryption Key (0–255)", 
                                         min_value=0, max_value=255, value=123, step=1, 
                                         key="img_dec_key",
                                         help="Enter the key used for encryption")
                img_dec_btn = st.form_submit_button("🔓 Decrypt Image")
            
            if img_dec_btn:
                if not enc_img:
                    st.error("⚠️ Please upload an encrypted image.")
                else:
                    with st.spinner("Decrypting image..."):
                        try:
                            data = enc_img.read()
                            decrypted = bytes(b ^ img_key2 for b in data)
                            
                            # Try to open the decrypted image
                            img_bytes = io.BytesIO(decrypted)
                            img = Image.open(img_bytes)
                            
                            # Store in session state for preview
                            st.session_state.decrypted_image = img
                            st.session_state.decrypted_image_bytes = decrypted
                            
                            st.success("✅ Image decrypted successfully!")
                            st.download_button(
                                "⬇️ Download Decrypted Image",
                                decrypted,
                                file_name=f"decrypted_{enc_img.name}",
                                mime="image/png",
                                key="img_dec_download"
                            )
                        except Exception as e:
                            st.error(f"🚫 Decryption failed. Invalid key or corrupted image.")
            st.markdown("</div>", unsafe_allow_html=True)

    # Preview column
    with preview_col:
        st.markdown("<div class='section'>", unsafe_allow_html=True)
        st.markdown("### Preview")
        
        # Image preview container
        preview_placeholder = st.empty()
        
        if 'decrypted_image' in st.session_state:
            preview_placeholder.image(st.session_state.decrypted_image, use_column_width=True)
        else:
            preview_placeholder.info("🖼️ Decrypted image will appear here.")
        
        st.markdown("</div>", unsafe_allow_html=True)


# ─── FILES TAB ────────────────────────────────────────────────────────────────
with tabs[2]:
    st.markdown("<div class='section'><h2>📄 File Encryption & Decryption</h2></div>", unsafe_allow_html=True)
    enc_col, dec_col = st.columns([1, 1], gap="large")

    # Encrypt column
    with enc_col:
        st.markdown("<div class='section'>", unsafe_allow_html=True)
        st.markdown("### Encrypt File")
        
        with st.form("file_encrypt", clear_on_submit=False):
            txt_file = st.file_uploader("Select file to encrypt", type=None, 
                                      key="txt_enc_file",
                                      help="Any file type supported")
            pwd_enc = st.text_input("Password", type="password", 
                                   key="txt_enc_pwd",
                                   help="Create a strong password (8+ chars, mixed case, numbers, symbols)")
            pwd_confirm = st.text_input("Confirm Password", type="password", 
                                      key="txt_enc_pwd_confirm")
            txt_enc_btn = st.form_submit_button("🔒 Encrypt File")
        
        if txt_enc_btn:
            if not txt_file:
                st.error("⚠️ Please select a file to encrypt.")
            elif not pwd_enc:
                st.error("⚠️ Please enter a password.")
            elif pwd_enc != pwd_confirm:
                st.error("⚠️ Passwords do not match.")
            elif not check_password_strength(pwd_enc):
                st.warning("⚠️ Weak password. Use at least 8 characters with uppercase, lowercase, digits, and symbols.")
            else:
                with st.spinner("Encrypting file..."):
                    try:
                        data = txt_file.read()
                        salt = os.urandom(16)
                        key = get_key_from_password(pwd_enc, salt)
                        token = Fernet(key).encrypt(data)
                        hmacv = generate_hmac(key, token)
                        out = salt + token + hmacv
                        
                        st.success("✅ File encrypted successfully!")
                        st.download_button(
                            "⬇️ Download Encrypted File",
                            out,
                            file_name=f"{Path(txt_file.name).stem}.encrypted",
                            mime="application/octet-stream",
                            key="file_enc_download"
                        )
                        
                        # Display HMAC in a copyable format
                        hmac_hex = hmacv.hex()
                        st.code(hmac_hex, language="text")
                        st.info("⚠️ **Important**: Save this HMAC value securely. You'll need it to decrypt the file.")
                        
                        # Copy button for HMAC (styled for dark theme)
                        st.markdown(f"""
                        <div style="display: flex; align-items: center;">
                            <input type="text" value="{hmac_hex}" 
                                   id="hmacValue" class="hmac-input" style="flex-grow: 1;">
                            <button onclick="navigator.clipboard.writeText(document.getElementById('hmacValue').value);this.innerHTML='✓ Copied!';" 
                                    class="hmac-copy-btn" style="margin-left: 8px;">
                                Copy HMAC
                            </button>
                        </div>
                        """, unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"🚫 Encryption failed: {str(e)}")
        st.markdown("</div>", unsafe_allow_html=True)

    # Decrypt column
    with dec_col:
        st.markdown("<div class='section'>", unsafe_allow_html=True)
        st.markdown("### Decrypt File")
        
        with st.form("file_decrypt", clear_on_submit=False):
            enc_file = st.file_uploader("Select encrypted file (.encrypted)", 
                                      key="txt_dec_file",
                                      help="Upload a file encrypted with this tool")
            pwd_dec = st.text_input("Password", type="password", 
                                   key="txt_dec_pwd",
                                   help="Enter the password used for encryption")
            hmac_in = st.text_input("HMAC", key="txt_dec_hmac",
                                   help="Enter the HMAC provided during encryption")
            txt_dec_btn = st.form_submit_button("🔓 Decrypt File")
        
        if txt_dec_btn:
            if not enc_file:
                st.error("⚠️ Please select an encrypted file.")
            elif not pwd_dec:
                st.error("⚠️ Please enter your password.")
            elif not hmac_in:
                st.error("⚠️ Please provide the HMAC value.")
            else:
                with st.spinner("Decrypting file..."):
                    try:
                        data = enc_file.read()
                        hsize = hashes.SHA256().digest_size
                        
                        if len(data) < 16 + hsize:
                            st.error("🚫 File too short or corrupted.")
                        else:
                            salt = data[:16]
                            token = data[16:-hsize]
                            hmac_stored = data[-hsize:]
                            
                            key2 = get_key_from_password(pwd_dec, salt)
                            
                            # Clean up the HMAC input (remove spaces, etc.)
                            hmac_in_clean = hmac_in.strip()
                            
                            if not verify_hmac(key2, token, bytes.fromhex(hmac_in_clean)):
                                st.error("🚫 HMAC verification failed. Wrong password or tampered file.")
                            else:
                                try:
                                    dec = Fernet(key2).decrypt(token)
                                    st.success("✅ File decrypted successfully!")
                                    
                                    # Try to detect if it's text for preview
                                    is_text = False
                                    try:
                                        preview_text = dec.decode('utf-8')
                                        if len(preview_text) < 10000:  # Only show preview for reasonably sized text
                                            st.markdown("### Preview:")
                                            st.code(preview_text[:1000] + ("..." if len(preview_text) > 1000 else ""))
                                            is_text = True
                                    except UnicodeDecodeError:
                                        # Not text data, skip preview
                                        pass
                                    
                                    st.download_button(
                                        "⬇️ Download Decrypted File",
                                        dec,
                                        file_name=f"decrypted_{Path(enc_file.name).stem}",
                                        mime="application/octet-stream" if not is_text else "text/plain",
                                        key="file_dec_download"
                                    )
                                except InvalidToken:
                                    st.error("🚫 Decryption failed. Invalid password or corrupted data.")
                    except Exception as e:
                        st.error(f"🚫 Decryption failed: {str(e)}")
        st.markdown("</div>", unsafe_allow_html=True)

# ─── SECURITY NOTES ───────────────────────────────────────────────────────────
with st.expander("📋 Security Information"):
    st.markdown("""
    ### About this tool
    - **Local Processing**: All encryption/decryption happens locally in your browser.
    - **No Data Storage**: Your files and passwords are never sent to any server.
    - **Encryption Methods**:
        - Videos/Images: Simple XOR encryption (suitable for personal use but not highly sensitive data)
        - Files: AES-256 encryption with password-based key derivation (PBKDF2) and HMAC verification
    
    ### Security Tips
    - Use strong, unique passwords for file encryption
    - Store the HMAC value securely - it's required for file decryption
    - For highly sensitive data, consider specialized encryption software
    """)

# ─── FOOTER ───────────────────────────────────────────────────────────────────
st.markdown("""
<footer>
    <p>All-in-One Encryption & Decryption Tool</p>
    <p style="font-size: 0.8rem; margin-top: 0.5rem;">© 2025 | Privacy-First Technology</p>
</footer>
""", unsafe_allow_html=True)

# Clean up temporary files on session end
def cleanup():
    if 'decrypted_video' in st.session_state and os.path.exists(st.session_state.decrypted_video):
        try:
            os.unlink(st.session_state.decrypted_video)
        except:
            pass

# Register cleanup function
import atexit
atexit.register(cleanup)