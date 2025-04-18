import streamlit as st
import os
import tempfile
import cv2
from pathlib import Path
from PIL import Image
import shutil

# Valid video extensions
VALID_EXTENSIONS = ['.mp4', '.avi', '.mov']

st.set_page_config(page_title="Video Encryptor/Decryptor", layout="wide")

# Helper function to validate video file
def is_valid_video(filename):
    return Path(filename).suffix.lower() in VALID_EXTENSIONS

# Encrypt video - dummy logic: extract frames
def encrypt_video(video_path, output_dir):
    cap = cv2.VideoCapture(video_path)
    count = 0
    frames = []
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frame_path = os.path.join(output_dir, f"frame_{count}.jpg")
        cv2.imwrite(frame_path, frame)
        frames.append(frame_path)
        count += 1
    cap.release()
    return frames

# Decrypt video - dummy logic: combine frames into video
def decrypt_video(frames_folder, output_video):
    frame_files = sorted(Path(frames_folder).glob("*.jpg"))
    if not frame_files:
        return None
    frame = cv2.imread(str(frame_files[0]))
    height, width, _ = frame.shape
    out = cv2.VideoWriter(output_video, cv2.VideoWriter_fourcc(*'mp4v'), 20.0, (width, height))
    for file in frame_files:
        frame = cv2.imread(str(file))
        out.write(frame)
    out.release()
    return output_video

st.markdown("<h1 style='text-align: center; color: #4CAF50;'>🔐 Video Encryption & Decryption Tool</h1>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    uploaded_video = st.file_uploader("📥 Upload a Video File", type=["mp4", "avi", "mov"])

    if uploaded_video:
        st.success(f"✅ Uploaded: {uploaded_video.name}")
        temp_video_path = os.path.join(tempfile.gettempdir(), uploaded_video.name)
        with open(temp_video_path, "wb") as f:
            f.write(uploaded_video.read())

        if is_valid_video(temp_video_path):
            st.video(temp_video_path, format="video/mp4")
        else:
            st.error("❌ Invalid video file format!")

with col2:
    decrypt_video_file = st.file_uploader("🔓 Upload Encrypted Video Frames (.jpgs in a ZIP)", type=["zip"])

st.markdown("---")
encrypt_col, decrypt_col = st.columns(2)

with encrypt_col:
    st.subheader("🔐 Encrypt Video")
    if uploaded_video and is_valid_video(temp_video_path):
        if st.button("Encrypt Now"):
            output_dir = os.path.join(tempfile.gettempdir(), "encrypted_frames")
            if os.path.exists(output_dir):
                shutil.rmtree(output_dir)
            os.makedirs(output_dir, exist_ok=True)
            frames = encrypt_video(temp_video_path, output_dir)
            st.success(f"✅ Encrypted {len(frames)} frames.")
            st.markdown("### 🔍 Frame Preview")
            cols = st.columns(5)
            for i, frame_path in enumerate(frames[:10]):
                cols[i % 5].image(Image.open(frame_path), use_column_width=True, caption=f"Frame {i}")

with decrypt_col:
    st.subheader("🔓 Decrypt Video")
    if decrypt_video_file and decrypt_video_file.name.endswith(".zip"):
        import zipfile
        zip_path = os.path.join(tempfile.gettempdir(), decrypt_video_file.name)
        with open(zip_path, "wb") as f:
            f.write(decrypt_video_file.read())

        unzip_dir = os.path.join(tempfile.gettempdir(), "decrypted_frames")
        if os.path.exists(unzip_dir):
            shutil.rmtree(unzip_dir)
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(unzip_dir)

        if st.button("Decrypt and Preview"):
            decrypted_video_path = os.path.join(tempfile.gettempdir(), "decrypted_output.mp4")
            result = decrypt_video(unzip_dir, decrypted_video_path)
            if result:
                st.success("✅ Decryption completed!")
                st.video(decrypted_video_path)
            else:
                st.error("❌ Failed to reconstruct video.")

st.markdown("---")
st.info("💡 *Tip: Encryption here means extracting and storing frames as images. You can replace this with your actual encryption logic!*")

st.markdown("<footer style='text-align: center; color: gray;'>Made with ❤️ by Anisha</footer>", unsafe_allow_html=True)
