import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import ImageTk, Image
import cv2
import numpy as np
import os
from moviepy.editor import ImageClip, concatenate_videoclips

# Global variable to store the selected filename
filename = ""

# Function to start the main application
def start_app():
    start_window.destroy()
    main_app()

# Function to exit the application
def exit_app(window):
    if messagebox.askokcancel("Exit", "Do you want to exit?"):
        window.destroy()

# Function to open file dialog and select a video file
def open_file():
    global filename
    filename = filedialog.askopenfilename(title="Select Video File")
    if filename:
        path_text.delete("1.0", "end")
        path_text.insert("end", filename)

# Function to play a video
def play_video(video_path, window_title):
    cap = cv2.VideoCapture(video_path)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow(window_title, frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

# Function to encrypt the video
def encrypt_video():
    global filename
    if not filename:
        messagebox.showerror("Error", "Please select a video file first.")
        return

    if not os.path.exists('Video_Images'):
        os.makedirs('Video_Images')

    cap = cv2.VideoCapture(filename)
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    frame_count = 0
    encrypted_frames = []

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if frame_count % fps == 0:
            frame_index = frame_count // fps
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            normalized_frame = gray_frame.astype(float) / 255.0
            mu, sigma = 0, 0.1
            key = np.random.normal(mu, sigma, normalized_frame.shape) + np.finfo(float).eps
            encrypted_frame = normalized_frame / key
            encrypted_frame = np.clip(encrypted_frame * 255, 0, 255).astype(np.uint8)
            frame_path = os.path.join('Video_Images', f'frame{frame_index}.jpg')
            cv2.imwrite(frame_path, encrypted_frame)
            encrypted_frames.append(frame_path)
        frame_count += 1

    cap.release()

    # Resize images to the average size
    mean_width = 0
    mean_height = 0
    for file in encrypted_frames:
        img = Image.open(file)
        width, height = img.size
        mean_width += width
        mean_height += height

    mean_width = int(mean_width / len(encrypted_frames))
    mean_height = int(mean_height / len(encrypted_frames))

    for file in encrypted_frames:
        img = Image.open(file)
        img_resized = img.resize((mean_width, mean_height), Image.LANCZOS)
        img_resized.save(file, 'JPEG', quality=95)

    # Generate encrypted video
    video_name = "encrypted_video.avi"
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(video_name, fourcc, 1, (mean_width, mean_height))

    for file in sorted(encrypted_frames):  # ensure proper order
        img = cv2.imread(file)
        img_color = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        out.write(img_color)

    out.release()
    print("Encrypted video created successfully.")
    play_video(video_name, "Encrypted Video")

# Function to decrypt the video (basic grayscale display)
def decrypt_video():
    global filename
    if not filename:
        messagebox.showerror("Error", "Please select a video file first.")
        return

    cap = cv2.VideoCapture(filename)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imshow("Decrypted Video", gray_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

# Function to reset and play the original video
def reset_video():
    global filename
    if not filename:
        messagebox.showerror("Error", "Please select a video file first.")
        return

    play_video(filename, "Original Video")

# Function to create the main application window
def main_app():
    global path_text

    app_window = tk.Tk()
    app_window.title("Video Encryption Decryption")
    app_window.geometry("1000x700")

    title_label = tk.Label(app_window, text="VIDEO ENCRYPTION\nDECRYPTION", font=("Arial", 40, "underline"), fg="magenta")
    title_label.pack(pady=20)

    select_label = tk.Label(app_window, text="Selected Video:", font=("Arial", 20))
    select_label.pack(pady=10)

    path_text = tk.Text(app_window, height=2, width=60, font=("Arial", 12))
    path_text.pack(pady=5)

    select_button = tk.Button(app_window, text="SELECT", command=open_file, font=("Arial", 15), bg="light green")
    select_button.pack(pady=5)

    encrypt_button = tk.Button(app_window, text="ENCRYPT VIDEO", command=encrypt_video, font=("Arial", 15), bg="orange")
    encrypt_button.pack(pady=5)

    decrypt_button = tk.Button(app_window, text="DECRYPT VIDEO", command=decrypt_video, font=("Arial", 15), bg="orange")
    decrypt_button.pack(pady=5)

    reset_button = tk.Button(app_window, text="RESET", command=reset_video, font=("Arial", 15), bg="yellow")
    reset_button.pack(pady=5)

    exit_button = tk.Button(app_window, text="EXIT", command=lambda: exit_app(app_window), font=("Arial", 15), bg="red")
    exit_button.pack(pady=5)

    app_window.protocol("WM_DELETE_WINDOW", lambda: exit_app(app_window))
    app_window.mainloop()

# Create the start window
start_window = tk.Tk()
start_window.title("Video Encryption Decryption")
start_window.geometry("600x400")

start_label = tk.Label(start_window, text="VIDEO ENCRYPTION\nDECRYPTION", font=("Arial", 30, "underline"), fg="magenta")
start_label.pack(pady=50)

start_button = tk.Button(start_window, text="START", command=start_app, font=("Arial", 20), bg="orange")
start_button.pack(pady=20)

exit_button = tk.Button(start_window, text="EXIT", command=lambda: exit_app(start_window), font=("Arial", 20), bg="red")
exit_button.pack(pady=20)

start_window.protocol("WM_DELETE_WINDOW", lambda: exit_app(start_window))
start_window.mainloop()
