import os
import sys
import customtkinter as ctk
from tkinter import messagebox as msg

# Add the parent directory to sys.path to import script from the parent directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Import the encryption/decryption functionality from script.py
import script

# Initialize the CustomTkinter app
app = ctk.CTk()


def CenterWindowToDisplay(
    Screen: ctk, width: int, height: int, scale_factor: float = 1.0
):
    """
    Centers the application window on the main display/monitor.

    Parameters:
        Screen (ctk): The application window.
        width (int): The width of the window.
        height (int): The height of the window.
        scale_factor (float): Scale factor to adjust the placement.

    Returns:
        str: Geometry for the window with width, height, and position on screen.
    """
    screen_width = Screen.winfo_screenwidth()
    screen_height = Screen.winfo_screenheight()
    x = int(((screen_width / 2) - (width / 2)) * scale_factor)
    y = int(((screen_height / 2) - (height / 1.5)) * scale_factor)
    return f"{width}x{height}+{x}+{y}"


# Set the geometry of the window and the title
app.geometry(CenterWindowToDisplay(app, 650, 400, app._get_window_scaling()))
app.title("Encryption and Decryption")

# Create the heading frame and label
heading_frame = ctk.CTkFrame(app)
heading_frame.pack(anchor=ctk.N, fill=ctk.X)
heading_label = ctk.CTkLabel(
    heading_frame, text="Encryption and Decryption", font=("Helvetica", 30)
)
heading_label.pack(anchor=ctk.CENTER, fill=ctk.X)


# File Browsing functions for Encryption and Decryption


def Encrypt_browse_key():
    """Open a file dialog to select a file for encryption with a secret key."""
    encryptfilename.delete(0, ctk.END)
    filename = ctk.filedialog.askopenfilename(
        filetypes=[("Encryption", "*.txt*"), ("Decryption", "*.decrypted*")]
    )
    encryptfilename.insert(0, filename)


def Decrypt_browse_key():
    """Open a file dialog to select a file for decryption with a secret key."""
    decryptfilename.delete(0, ctk.END)
    filename = ctk.filedialog.askopenfilename(
        filetypes=[("Decryption", "*.encrypted*")]
    )
    decryptfilename.insert(0, filename)


def Encrypt_browse_pass():
    """Open a file dialog to select a file for encryption with a password."""
    try:
        encryptfilenamepass.delete(0, ctk.END)
        filename = ctk.filedialog.askopenfilename(
            filetypes=[("Encryption", "*.txt*"), ("Decryption", "*.decrypted*")]
        )
        encryptfilenamepass.insert(0, filename)
    except TypeError:
        msg.showinfo("INFO", "Use correct password")


def Decrypt_browse_pass():
    """Open a file dialog to select a file for decryption with a password."""
    try:
        decryptfilenamepass.delete(0, ctk.END)
        filename = ctk.filedialog.askopenfilename(
            filetypes=[("Decryption", "*.encrypted*")]
        )
        decryptfilenamepass.insert(0, filename)
    except TypeError:
        msg.showinfo("INFO", "Use correct password")


# Encryption/Decryption functions


def Encrypt_with_SecretKey():
    """
    Calls the encrypt_file function from script.py to encrypt the selected file using a secret key.
    """
    file = encryptfilename.get()
    script.encrypt_file(file, "key", 0, app)


def Decrypt_with_SecretKey():
    """
    Calls the decrypt_file function from script.py to decrypt the selected file using a secret key.
    """
    file = decryptfilename.get()
    script.decrypt_file(file, "key", 0, app)


def Encrypt_with_Password():
    """
    Calls the encrypt_file function from script.py to encrypt the selected file using a password.
    """
    file = encryptfilenamepass.get()
    script.encrypt_file(file, "password", 0, app)


def Decrypt_with_Password():
    """
    Calls the decrypt_file function from script.py to decrypt the selected file using a password.
    """
    file = decryptfilenamepass.get()
    script.decrypt_file(file, "password", 0, app)


# GUI Layout for Encryption and Decryption using Secret Key

key_frame = ctk.CTkFrame(app)
key_frame.pack(anchor=ctk.N, fill=ctk.X)

# Encrypt Section (Secret Key)
encryptfileLabel = ctk.CTkLabel(key_frame, text="Encrypt File", font=("Helvetica", 15))
encryptfileLabel.pack(anchor=ctk.NW, padx=(20, 0), pady=(5, 0))

encrypt_frame = ctk.CTkFrame(key_frame)
encrypt_frame.pack(anchor=ctk.NW, padx=20)

# Entry field and browse button for encryption
encryptfilename = ctk.CTkEntry(encrypt_frame, width=450, font=("Helvetica", 15))
encryptfilename.pack(side=ctk.LEFT)

encryptbrowsebutton = ctk.CTkButton(
    encrypt_frame, text="Browse", command=Encrypt_browse_key
)
encryptbrowsebutton.pack(side=ctk.LEFT)

encryptwithkey = ctk.CTkButton(
    key_frame, text="Encrypt", command=Encrypt_with_SecretKey
)
encryptwithkey.pack(anchor=ctk.W, padx=20)

# Decrypt Section (Secret Key)
decryptfileLabel = ctk.CTkLabel(key_frame, text="Decrypt File", font=("Helvetica", 15))
decryptfileLabel.pack(anchor=ctk.NW, padx=(20, 0), pady=(5, 0))

decrypt_frame = ctk.CTkFrame(key_frame)
decrypt_frame.pack(anchor=ctk.NW, padx=20)

# Entry field and browse button for decryption
decryptfilename = ctk.CTkEntry(decrypt_frame, width=450, font=("Helvetica", 15))
decryptfilename.pack(side=ctk.LEFT)

decryptbrowsebutton = ctk.CTkButton(
    decrypt_frame, text="Browse", command=Decrypt_browse_key
)
decryptbrowsebutton.pack(side=ctk.LEFT)

decryptwithkey = ctk.CTkButton(
    key_frame, text="Decrypt", command=Decrypt_with_SecretKey
)
decryptwithkey.pack(anchor=ctk.W, padx=20)

# GUI Layout for Encryption and Decryption using Password

password_frame = ctk.CTkFrame(app)
password_frame.pack(anchor=ctk.N, fill=ctk.X)

# Encrypt Section (Password)
encryptfileLabelpass = ctk.CTkLabel(
    password_frame, text="Encrypt File (Password)", font=("Helvetica", 15)
)
encryptfileLabelpass.pack(anchor=ctk.NW, padx=(20, 0), pady=(5, 0))

encrypt_framepass = ctk.CTkFrame(password_frame)
encrypt_framepass.pack(anchor=ctk.NW, padx=20)

# Entry field and browse button for encryption
encryptfilenamepass = ctk.CTkEntry(encrypt_framepass, width=450, font=("Helvetica", 15))
encryptfilenamepass.pack(side=ctk.LEFT)

encryptbrowsebuttonpass = ctk.CTkButton(
    encrypt_framepass, text="Browse", command=Encrypt_browse_pass
)
encryptbrowsebuttonpass.pack(side=ctk.LEFT)

encryptwithkeypass = ctk.CTkButton(
    password_frame, text="Encrypt with Password", command=Encrypt_with_Password
)
encryptwithkeypass.pack(anchor=ctk.W, padx=20)

# Decrypt Section (Password)
decryptfileLabelpass = ctk.CTkLabel(
    password_frame, text="Decrypt File", font=("Helvetica", 15)
)
decryptfileLabelpass.pack(anchor=ctk.NW, padx=(20, 0), pady=(5, 0))

decrypt_framepass = ctk.CTkFrame(password_frame)
decrypt_framepass.pack(anchor=ctk.NW, padx=20)

# Entry field and browse button for decryption
decryptfilenamepass = ctk.CTkEntry(decrypt_framepass, width=450, font=("Helvetica", 15))
decryptfilenamepass.pack(side=ctk.LEFT)

decryptbrowsebuttonpass = ctk.CTkButton(
    decrypt_framepass, text="Browse", command=Decrypt_browse_pass
)
decryptbrowsebuttonpass.pack(side=ctk.LEFT)

decryptwithkeypass = ctk.CTkButton(
    password_frame, text="Decrypt with Password", command=Decrypt_with_Password
)
decryptwithkeypass.pack(anchor=ctk.W, padx=20)

# Start the app's main event loop
app.mainloop()
