from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from PIL import Image, ImageTk

# ========== IMAGE ENCRYPTION ==========

def filepath():
    global image, photo, file_path
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.gif;*.bmp;*.tiff;*.webp;*.heif")])
    if file_path:
        try:
            image = Image.open(file_path)
            image.thumbnail((200, 200), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            image_display.config(image=photo, text="")
            image_display.image = photo
            path_value.set(file_path)
        except Exception as e:
            image_display.config(text="Cannot Display Image \n(Possibly Encrypted)", image=None)
            image_display.image = None
            path_value.set(file_path)

def encryption():
    if path_value.get() and key_value.get():
        file_name = path_value.get()
        key = key_value.get()
        try:
            with open(file_name, 'rb') as file:
                img = file.read()

            img_bytearray = bytearray(img)
            already_encrypted = True

            for index, value in enumerate(img_bytearray):
                new_value = value ^ key
                if new_value != value:
                    already_encrypted = False
                img_bytearray[index] = new_value

            if already_encrypted:
                foot_lable.config(text="Already Encrypted", fg="orange")
            else:
                with open(file_name, 'wb') as file:
                    file.write(img_bytearray)
                foot_lable.config(text=f"Encryption Done\nEncrypted image saved to {file_name}", fg="lightgreen")
                image_display.config(text="Cannot Display Encrypted Image", image=None)
                image_display.image = None

        except Exception as e:
            image_display.config(text="Cannot Display Encrypted Image", image=None, fg="red")
            image_display.image = None
            foot_lable.config(text="Encryption Failed", fg="red")

def decryption():
    if path_value.get() and key_value.get():
        file_name = path_value.get()
        key = key_value.get()
        try:
            with open(file_name, 'rb') as file:
                img = file.read()

            img = bytearray(img)
            for index, value in enumerate(img):
                img[index] = value ^ key

            with open(file_name, 'wb') as file:
                file.write(img)

            image = Image.open(file_name)
            image.thumbnail((200, 200), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            image_display.config(image=photo, text="")
            image_display.image = photo
            foot_lable.config(text=f"Decryption Done\nDecrypted image saved to {file_name}", fg="lightgreen")

        except Exception as e:
            image_display.config(image=None, text="Cannot Display Image", fg="red")
            image_display.image = None
            foot_lable.config(text="Decryption Failed", fg="red")

# ========== TEXT ENCRYPTION ==========

def encrypt_text():
    text = text_input.get("1.0", END).rstrip()
    key = text_key_value.get()
    if text and key:
        encrypted = ''.join(chr(ord(char) ^ key) for char in text)
        text_output.delete("1.0", END)
        text_output.insert("1.0", encrypted)

def decrypt_text():
    text = text_input.get("1.0", END).rstrip()
    key = text_key_value.get()
    if text and key:
        decrypted = ''.join(chr(ord(char) ^ key) for char in text)
        text_output.delete("1.0", END)
        text_output.insert("1.0", decrypted)

# ========== UI SETUP ==========

base = Tk()
base.geometry("650x520")
base.title("ImgCrypt + Text")
base.config(bg="black")

style = ttk.Style()
style.theme_use("default")
style.configure("TNotebook", background="black", foreground="white")
style.configure("TNotebook.Tab", font=("Times New Roman", 12, "bold"), padding=[10, 5])
style.map("TNotebook.Tab", background=[("selected", "#222")], foreground=[("selected", "lightgreen")])

notebook = ttk.Notebook(base)
notebook.pack(expand=True, fill="both", padx=10, pady=10)

# ========== IMAGE TAB ==========

image_tab = Frame(notebook, bg="black")
notebook.add(image_tab, text="Image")

head_lable = Label(image_tab, text="Image Encryption-Decryption", font=("Times New Roman", 20, "bold"), bg="black", fg="white")
head_lable.pack(pady=10)

path_value = StringVar()
path_frame = Frame(image_tab, bg="black")
path_frame.pack()
Label(path_frame, text="Image Path:", font=("Times New Roman", 14), bg="black", fg="white").grid(row=0, column=0)
Entry(path_frame, textvariable=path_value, font=("Times New Roman", 12), width=45).grid(row=0, column=1)
Button(path_frame, text="Browse", command=filepath).grid(row=0, column=2, padx=5)

key_value = IntVar()
key_frame = Frame(image_tab, bg="black")
key_frame.pack(pady=5)
Label(key_frame, text="Key:", font=("Times New Roman", 14), bg="black", fg="white").grid(row=0, column=0)
Entry(key_frame, textvariable=key_value, font=("Times New Roman", 12), width=10).grid(row=0, column=1, padx=5)
Button(key_frame, text="Encrypt", command=encryption, width=15).grid(row=0, column=2, padx=5)
Button(key_frame, text="Decrypt", command=decryption, width=15).grid(row=0, column=3, padx=5)

image_frame = Frame(image_tab, borderwidth=3, relief=SUNKEN, height=200, width=200)
image_frame.pack(pady=15)
image_display = Label(image_frame, text="No Image Selected")
image_display.pack()
image_frame.pack_propagate(False)

foot_lable = Label(image_tab, text="", font=("Times New Roman", 12, "bold"), bg="black", fg="lightgreen")
foot_lable.pack()

# ========== TEXT TAB ==========

text_tab = Frame(notebook, bg="black")
notebook.add(text_tab, text="Text")

Label(text_tab, text="Text Encryption-Decryption", font=("Times New Roman", 20, "bold"), bg="black", fg="white").pack(pady=10)

text_frame = Frame(text_tab, bg="black")
text_frame.pack(pady=5)

Label(text_frame, text="Enter Text:", font=("Times New Roman", 14), bg="black", fg="white").grid(row=0, column=0, sticky="nw")
text_input = Text(text_frame, height=5, width=60, font=("Times New Roman", 12))
text_input.grid(row=1, column=0, padx=5)

Label(text_frame, text="Key (Integer):", font=("Times New Roman", 14), bg="black", fg="white").grid(row=2, column=0, sticky="w", pady=(10, 0))
text_key_value = IntVar()
Entry(text_frame, textvariable=text_key_value, font=("Times New Roman", 12), width=10).grid(row=2, column=0, sticky="e", padx=10)

Button(text_tab, text="Encrypt", command=encrypt_text, width=15).pack(pady=5)
Button(text_tab, text="Decrypt", command=decrypt_text, width=15).pack(pady=5)

Label(text_tab, text="Output:", font=("Times New Roman", 14), bg="black", fg="white").pack(pady=5)
text_output = Text(text_tab, height=5, width=60, font=("Times New Roman", 12))
text_output.pack()

base.mainloop()
