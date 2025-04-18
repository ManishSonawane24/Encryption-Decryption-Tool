
# main.py
import os
import sys
import customtkinter as ctk
from tkinter import filedialog
from tkinter import messagebox as msg
from PIL import Image, ImageTk

# Ensure we can import script.py
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
import text.script as script 

class UnifiedApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Universal Encryptor/Decryptor")
        self.geometry(self._center(800, 600))

        # Create a Tab view with two tabs
        self.tabview = ctk.CTkTabview(self, width=780, height=580)
        self.tabview.pack(padx=10, pady=10, fill="both", expand=True)

        # Text‑File Tab
        self.tabview.add("Text Files")
        self._build_text_tab(self.tabview.tab("Text Files"))

        # Image‑File Tab
        self.tabview.add("Images")
        self._build_image_tab(self.tabview.tab("Images"))

    def _center(self, w, h):
        sw, sh = self.winfo_screenwidth(), self.winfo_screenheight()
        x, y = (sw - w) // 2, (sh - h) // 3
        return f"{w}x{h}+{x}+{y}"

    # ─── TEXT FILE TAB ─────────────────────────────────────────────────────────
    # def _build_text_tab(self, parent):
    #     frm = parent

    #     # Generate Key
    #     gen_btn = ctk.CTkButton(frm, text="Generate Key", command=self._gen_key)
    #     gen_btn.pack(pady=(20, 10))

    #     # Secret‑Key Encryption/Decryption
    #     self._make_file_row(frm, "Encrypt (Key)", self._browse_encrypt_key, self._do_encrypt_key)
    #     self._make_file_row(frm, "Decrypt (Key)", self._browse_decrypt_key, self._do_decrypt_key)

    #     # Password‑Based Encryption/Decryption
    #     self._make_file_row(frm, "Encrypt (Password)", self._browse_encrypt_pass, self._do_encrypt_pass)
    #     self._make_file_row(frm, "Decrypt (Password)", self._browse_decrypt_pass, self._do_decrypt_pass)

# ─── TEXT TAB WITH DIRECT TEXT ENTRY ──────────────────────────────────────────
    def _build_text_tab(self, parent):
        frm = parent

        # Input Text Area
        ctk.CTkLabel(frm, text="Input Text:").pack(pady=(10, 2))
        self.input_textbox = ctk.CTkTextbox(frm, height=120, wrap="word")
        self.input_textbox.pack(fill="both", padx=20)

        # Method Selection: Key or Password
        method_frame = ctk.CTkFrame(frm)
        method_frame.pack(pady=10)
        ctk.CTkLabel(method_frame, text="Method:").pack(side="left", padx=5)
        self.method_var = ctk.StringVar(value="key")
        ctk.CTkRadioButton(method_frame, text="Key", variable=self.method_var, value="key").pack(side="left", padx=5)
        ctk.CTkRadioButton(method_frame, text="Password", variable=self.method_var, value="password").pack(side="left", padx=5)

        # Action Buttons
        action_frame = ctk.CTkFrame(frm)
        action_frame.pack(pady=5)
        ctk.CTkButton(action_frame, text="Encrypt", command=self._encrypt_text).pack(side="left", padx=10)
        ctk.CTkButton(action_frame, text="Decrypt", command=self._decrypt_text).pack(side="left", padx=10)

        # Output Text Area
        ctk.CTkLabel(frm, text="Output:").pack(pady=(10, 2))
        self.output_textbox = ctk.CTkTextbox(frm, height=120, wrap="word", state="normal")
        self.output_textbox.pack(fill="both", padx=20)

    def _encrypt_text(self):
        raw_text = self.input_textbox.get("1.0", "end").strip()
        if not raw_text:
            msg.showwarning("Input Missing", "Please enter some text to encrypt.")
            return
        method = self.method_var.get()
        try:
            result = script.encrypt_text(raw_text, method)
            self.output_textbox.configure(state="normal")
            self.output_textbox.delete("1.0", "end")
            self.output_textbox.insert("1.0", result)
        except Exception as e:
            msg.showerror("Encryption Failed", str(e))

    def _decrypt_text(self):
        raw_text = self.input_textbox.get("1.0", "end").strip()
        if not raw_text:
            msg.showwarning("Input Missing", "Please enter some text to decrypt.")
            return
        method = self.method_var.get()
        try:
            result = script.decrypt_text(raw_text, method)
            self.output_textbox.configure(state="normal")
            self.output_textbox.delete("1.0", "end")
            self.output_textbox.insert("1.0", result)
        except Exception as e:
            msg.showerror("Decryption Failed", str(e))


    def _make_file_row(self, parent, label, browse_cmd, action_cmd):
        row = ctk.CTkFrame(parent)
        row.pack(fill="x", padx=20, pady=5)
        ctk.CTkLabel(row, text=label, width=160, anchor="w").pack(side="left")
        entry = ctk.CTkEntry(row, width=400)
        entry.pack(side="left", padx=5)
        btn_b = ctk.CTkButton(row, text="Browse", width=80, command=lambda e=entry, c=browse_cmd: c(e))
        btn_b.pack(side="left", padx=5)
        btn_a = ctk.CTkButton(row, text=label.split()[0], width=80, command=lambda e=entry, c=action_cmd: c(e))
        btn_a.pack(side="left", padx=5)

    def _gen_key(self):
        script.generate_key()

    def _browse_encrypt_key(self, entry):
        path = filedialog.askopenfilename(filetypes=[("All Files","*.*")])
        entry.delete(0, "end"); entry.insert(0, path)
    def _browse_decrypt_key(self, entry):
        path = filedialog.askopenfilename(filetypes=[("*.encrypted","*.encrypted")])
        entry.delete(0, "end"); entry.insert(0, path)

    def _browse_encrypt_pass(self, entry):
        path = filedialog.askopenfilename(filetypes=[("All Files","*.*")])
        entry.delete(0, "end"); entry.insert(0, path)
    def _browse_decrypt_pass(self, entry):
        path = filedialog.askopenfilename(filetypes=[("*.encrypted","*.encrypted")])
        entry.delete(0, "end"); entry.insert(0, path)

    def _do_encrypt_key(self, entry):
        fn = entry.get()
        if fn: script.encrypt_file(fn, "key", 0, self)
    def _do_decrypt_key(self, entry):
        fn = entry.get()
        if fn: script.decrypt_file(fn, "key", 0, self)

    def _do_encrypt_pass(self, entry):
        fn = entry.get()
        if fn: script.encrypt_file(fn, "password", 0, self)
    def _do_decrypt_pass(self, entry):
        fn = entry.get()
        if fn: script.decrypt_file(fn, "password", 0, self)

    # ─── IMAGE FILE TAB ────────────────────────────────────────────────────────
    def _build_image_tab(self, parent):
        frm = parent

        # Path + Browse
        top = ctk.CTkFrame(frm)
        top.pack(fill="x", padx=20, pady=10)
        ctk.CTkLabel(top, text="Image File:", width=100, anchor="w").pack(side="left")
        self.img_path = ctk.CTkEntry(top)
        self.img_path.pack(side="left", fill="x", expand=True, padx=5)
        ctk.CTkButton(top, text="Browse", command=self._img_browse).pack(side="left")

        # XOR Key entry (plain text)
        mid = ctk.CTkFrame(frm)
        mid.pack(pady=5)
        ctk.CTkLabel(mid, text="XOR Key (0–255):").pack(side="left", padx=(0,5))
        self.img_key_entry = ctk.CTkEntry(mid, width=60)
        self.img_key_entry.insert(0, "0")
        self.img_key_entry.pack(side="left")

        # Encrypt / Decrypt buttons
        btnframe = ctk.CTkFrame(frm)
        btnframe.pack(pady=10)
        ctk.CTkButton(btnframe, text="Encrypt Image", command=self._img_encrypt).pack(side="left", padx=10)
        ctk.CTkButton(btnframe, text="Decrypt Image", command=self._img_decrypt).pack(side="left", padx=10)

        # Preview & status
        self.preview = ctk.CTkLabel(frm, text="No Image", width=200, height=200, fg_color="gray20")
        self.preview.pack(pady=10)
        self.status  = ctk.CTkLabel(frm, text="", height=30)
        self.status.pack()

    def _img_browse(self):
        p = filedialog.askopenfilename(
            filetypes=[("Image","*.png;*.jpg;*.jpeg;*.bmp;*.gif;*.tiff")])
        if p:
            self.img_path.delete(0,"end")
            self.img_path.insert(0,p)
            self._show_image(p)

    def _show_image(self, path):
        try:
            img = Image.open(path)
            img.thumbnail((200,200), Image.Resampling.LANCZOS)
            self.tkimg = ImageTk.PhotoImage(img)
            self.preview.configure(image=self.tkimg, text="")
        except Exception:
            self.preview.configure(image=None, text="Cannot display")

    def _img_encrypt(self):
        path = self.img_path.get().strip()
        # Parse & validate key
        try:
            k = int(self.img_key_entry.get().strip())
            if not (0 <= k <= 255):
                raise ValueError
        except ValueError:
            self.status.configure(text="Invalid key: enter 0–255", fg_color="red")
            return

        # Perform XOR encryption
        try:
            data = bytearray(open(path, "rb").read())
            already = True
            for i, v in enumerate(data):
                nv = v ^ k
                if nv != v:
                    already = False
                data[i] = nv

            if already:
                self.status.configure(text="Already Encrypted", fg_color="orange")
            else:
                open(path, "wb").write(data)
                self.status.configure(text="Encryption Done", fg_color="green")
                self.preview.configure(image=None, text="Encrypted")
        except Exception as e:
            self.status.configure(text="Encrypt Failed", fg_color="red")

    def _img_decrypt(self):
        path = self.img_path.get().strip()
        # Parse & validate key
        try:
            k = int(self.img_key_entry.get().strip())
            if not (0 <= k <= 255):
                raise ValueError
        except ValueError:
            self.status.configure(text="Invalid key: enter 0–255", fg_color="red")
            return

        # Perform XOR decryption
        try:
            data = bytearray(open(path, "rb").read())
            for i in range(len(data)):
                data[i] ^= k
            open(path, "wb").write(data)

            self.status.configure(text="Decryption Done", fg_color="green")
            self._show_image(path)
        except Exception as e:
            self.status.configure(text="Decryption Done", fg_color="green")



if __name__ == "__main__":
    ctk.set_appearance_mode("Dark")   # or "Light"
    ctk.set_default_color_theme("blue")
    UnifiedApp().mainloop()
