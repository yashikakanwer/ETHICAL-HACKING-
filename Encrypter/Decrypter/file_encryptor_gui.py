import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

# Password ke sath key derive karne ka function
def derive_key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=390000,
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))

def generate_key():
    # Random key generate karne ka simple option (optional agar password nahi use kar rahe)
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)
    messagebox.showinfo("Key Generated", "Encryption Key generated and saved as 'secret.key'.")

def encrypt_file_gui():
    filename = msg_file_var.get()
    output_name = output_file_var.get()
    password = password_var.get()
    if not filename or not output_name or not password:
        messagebox.showerror("Error", "Please select file, output and enter password!")
        return

    salt = os.urandom(16)  # 16 bytes random salt
    key = derive_key(password, salt)
    f = Fernet(key)

    try:
        with open(filename, "rb") as file:
            file_data = file.read()
    except Exception as e:
        messagebox.showerror("File Error", f"Could not read input file: {e}")
        return

    encrypted_data = f.encrypt(file_data)
    try:
        with open(output_name, "wb") as file:
            file.write(salt + encrypted_data)  # salt + encrypted data store karo
    except Exception as e:
        messagebox.showerror("File Error", f"Could not write to output file: {e}")
        return

    messagebox.showinfo("Success", "File encrypted and saved!")

def decrypt_file_gui():
    filename = msg_file_var.get()
    output_name = output_file_var.get()
    password = password_var.get()
    if not filename or not output_name or not password:
        messagebox.showerror("Error", "Please select files and enter password!")
        return

    try:
        with open(filename, "rb") as file:
            content = file.read()
    except Exception as e:
        messagebox.showerror("File Error", f"Could not read encrypted file: {e}")
        return

    salt = content[:16]
    encrypted_data = content[16:]

    try:
        key = derive_key(password, salt)
        f = Fernet(key)
        decrypted_data = f.decrypt(encrypted_data)
    except Exception as e:
        messagebox.showerror("Decryption Error", "Wrong password or corrupt file!")
        return

    try:
        with open(output_name, "wb") as file:
            file.write(decrypted_data)
    except Exception as e:
        messagebox.showerror("File Error", f"Could not write to output file: {e}")
        return

    messagebox.showinfo("Success", "File decrypted and saved!")

def pick_msg_file():
    file = filedialog.askopenfilename()
    if file:
        msg_file_var.set(file)

def pick_output_file():
    file = filedialog.asksaveasfilename(defaultextension=".encrypted")
    if file:
        output_file_var.set(file)

# GUI Setup
root = tk.Tk()
root.title("Advanced File Encryptor/Decryptor")
root.geometry("600x350")

notebook = ttk.Notebook(root)
tab1 = ttk.Frame(notebook)
notebook.add(tab1, text="Encrypt / Decrypt File")
notebook.pack(fill='both', expand=True)

title_label = tk.Label(tab1, text="Secure Your Files with Encryption", font=('Arial', 14, 'bold'))
title_label.grid(row=0, column=0, columnspan=3, pady=10)

msg_file_var = tk.StringVar()
tk.Label(tab1, text="Message file:").grid(row=1, column=0, sticky='e', padx=10, pady=5)
tk.Entry(tab1, textvariable=msg_file_var, width=40).grid(row=1, column=1, padx=5)
tk.Button(tab1, text="Browse...", command=pick_msg_file).grid(row=1, column=2, padx=10)

output_file_var = tk.StringVar()
tk.Label(tab1, text="Output file:").grid(row=2, column=0, sticky='e', padx=10, pady=5)
tk.Entry(tab1, textvariable=output_file_var, width=40).grid(row=2, column=1, padx=5)
tk.Button(tab1, text="Save As...", command=pick_output_file).grid(row=2, column=2, padx=10)

tk.Label(tab1, text="Algorithm:").grid(row=3, column=0, sticky='e', padx=10, pady=5)
algo_cb = ttk.Combobox(tab1, values=["AES128 (Standard)"], state="readonly")
algo_cb.set("AES128 (Standard)")
algo_cb.grid(row=3, column=1, sticky='w', pady=5)

password_var = tk.StringVar()
tk.Label(tab1, text="Password:").grid(row=4, column=0, sticky='e', padx=10, pady=5)
tk.Entry(tab1, textvariable=password_var, show="*", width=25).grid(row=4, column=1, sticky='w')

btns_frame = tk.Frame(tab1)
btns_frame.grid(row=5, column=0, columnspan=3, pady=15)

tk.Button(btns_frame, text="Generate Key", command=generate_key, width=16).grid(row=0, column=0, padx=10)
tk.Button(btns_frame, text="Encrypt File", command=encrypt_file_gui, width=16).grid(row=0, column=1, padx=10)
tk.Button(btns_frame, text="Decrypt File", command=decrypt_file_gui, width=16).grid(row=0, column=2, padx=10)

footer = tk.Label(tab1, text="Inspired by OpenStego | Demo - Yashika", font=("Arial", 9), fg="grey")
footer.grid(row=6, column=0, columnspan=3, pady=15)

root.mainloop()
