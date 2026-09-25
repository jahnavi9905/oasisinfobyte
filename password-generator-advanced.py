import tkinter as tk
from tkinter import ttk, messagebox
import random
import string
import pyperclip


class PasswordGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Password Generator")

        # Default settings for the password generator
        self.password_length = tk.IntVar(value=12)
        self.include_letters = tk.BooleanVar(value=True)
        self.include_numbers = tk.BooleanVar(value=True)
        self.include_symbols = tk.BooleanVar(value=True)

        self.create_widgets()

    def create_widgets(self):
        # Main interface
        ttk.Label(self.root, text="Password Length:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        ttk.Entry(self.root, textvariable=self.password_length, width=10).grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(self.root, text="Include Characters:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        ttk.Checkbutton(self.root, text="Letters", variable=self.include_letters).grid(row=1, column=1, sticky="w")
        ttk.Checkbutton(self.root, text="Numbers", variable=self.include_numbers).grid(row=2, column=1, sticky="w")
        ttk.Checkbutton(self.root, text="Symbols", variable=self.include_symbols).grid(row=3, column=1, sticky="w")

        ttk.Button(self.root, text="Generate Password", command=self.generate_password).grid(row=4, column=0, columnspan=2, pady=10)
        self.result_entry = ttk.Entry(self.root, width=30, state="readonly", justify="center")
        self.result_entry.grid(row=5, column=0, columnspan=2, padx=10, pady=5)

        ttk.Button(self.root, text="Copy to Clipboard", command=self.copy_to_clipboard).grid(row=6, column=0, columnspan=2, pady=10)

    def generate_password(self):
        length = self.password_length.get()
        use_letters = self.include_letters.get()
        use_numbers = self.include_numbers.get()
        use_symbols = self.include_symbols.get()

        if length <= 0:
            messagebox.showerror("Error", "Password length must be greater than 0.")
            return

        if not (use_letters or use_numbers or use_symbols):
            messagebox.showerror("Error", "At least one character type must be selected.")
            return

        character_pool = ""
        if use_letters:
            character_pool += string.ascii_letters
        if use_numbers:
            character_pool += string.digits
        if use_symbols:
            character_pool += string.punctuation

        # Generate the password
        password = ''.join(random.choice(character_pool) for _ in range(length))
        self.result_entry.configure(state="normal")
        self.result_entry.delete(0, tk.END)
        self.result_entry.insert(0, password)
        self.result_entry.configure(state="readonly")

    def copy_to_clipboard(self):
        password = self.result_entry.get()
        if password:
            pyperclip.copy(password)
            messagebox.showinfo("Copied", "Password copied to clipboard!")
        else:
            messagebox.showwarning("Error", "No password to copy!")


if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop()
