# This Python Tool Can Encrypt And Decrypt Images 
# By Kalmux

from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk

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

def open_imgcrypt_file():
    global image, photo, file_path
    file_path = "imgcrypt"  # Ensure this is the correct path to your file

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
            # Read the image file
            with open(file_name, 'rb') as file:
                img = file.read()

            # Encrypt the image data
            img_bytearray = bytearray(img)
            already_encrypted = True

            for index, value in enumerate(img_bytearray):
                new_value = value ^ key
                # Check if the image data is already encrypted
                if new_value != value:
                    already_encrypted = False
                img_bytearray[index] = new_value

            if already_encrypted:
                foot_lable.config(text="Already Encrypted", fg="orange")
            else:
                # Write the encrypted data back to the file
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
            # Read the encrypted image file
            with open(file_name, 'rb') as file:
                img = file.read()

            # Decrypt the image data
            img = bytearray(img)
            for index, value in enumerate(img):
                img[index] = value ^ key

            # Write the decrypted data back to the file
            with open(file_name, 'wb') as file:
                file.write(img)

            # Reload and display the decrypted image
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

base = Tk()

base.geometry("600x460")
base.title("ImgCrypt")
base.config(bg="black")

head_frame = Frame(base)
head_frame.pack(pady=10)

head_lable = Label(head_frame, text="Image Encryption-Decription", font=("Times New Roman", 30, "bold"), bg="black", fg="white")
head_lable.pack()

subhead_frame = Frame(base)
subhead_frame.pack()

subhead_lable = Label(subhead_frame, text="", font=("Times New Roman", 15, "bold"), bg="black", fg="white")
subhead_lable.pack()

file_frame = Frame(base, bg="black")
file_frame.pack(side=TOP, anchor="nw", pady=5, padx=8)

file_lable = Label(file_frame, text="Image Path:", font=("Times New Roman", 15), bg="black", fg="white")
file_lable.grid(row=1, column=0)

path_value = StringVar()
path_value.set("")
path = Entry(file_frame, textvariable=path_value, font=("Times New Roman", 12), width=50)
path.grid(row=1, column=2)

path_button = Button(file_frame, text="Browse", command=filepath, font=("Times New Roman", 10), padx=10)
path_button.grid(row=1, column=3, padx=5)

key_frame = Frame(base, bg="black")
key_frame.pack(side=TOP, anchor="nw")

space_lable = Label(key_frame, text="", padx=30, bg="black")
space_lable.grid(row=0, column=0)

key_lable = Label(key_frame, text="Key:", font=("Times New Roman", 14), bg="black", fg="white")
key_lable.grid(row=0, column=1)

key_value = IntVar()
key = Entry(key_frame, textvariable=key_value, font=("Times New Roman", 12), width=10)
key.grid(row=0, column=2)

space_lable = Label(key_frame, text="", padx=54, bg="black")
space_lable.grid(row=0, column=3)

encrypt_button = Button(key_frame, text="Encrypt", command=encryption, font=("Times New Roman", 11), width=15)
encrypt_button.grid(row=0, column=4, padx=10)
decrypt_button = Button(key_frame, text="Decrypt", command=decryption, font=("Times New Roman", 11), width=15)
decrypt_button.grid(row=0, column=5, padx=5)

space_frame = Frame(base)
space_frame.pack()

space_lable = Label(space_frame, text="", font=("", 5, "bold"), bg="black", fg="white",)
space_lable.pack()

image_frame = Frame(base, borderwidth=3, relief=SUNKEN, height=200, width=200)
image_frame.pack(side=TOP, anchor="center", expand=False, pady=10)

image_display = Label(image_frame, height=200, width=200, text="No Image Selected")
image_display.pack(expand=True)

image_frame.pack_propagate(False)

foot_frame = Frame(base)
foot_frame.pack()

foot_lable = Label(foot_frame, text="", font=("Times New Roman", 15, "bold"), bg="black", fg="lightgreen")
foot_lable.pack(side=TOP, anchor="center")

base.mainloop()
