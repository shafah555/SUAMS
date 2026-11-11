import tkinter as tk
from tkinter import ttk, messagebox
from core import authenticate

class LoginWindow:
    def __init__(self, root, on_success):
        self.root, self.on_success = root, on_success
        root.title("SUAMS | Sign in")
        root.geometry("440x390")
        root.configure(bg="#edf4ff")
        box = ttk.Frame(root, padding=30)
        box.pack(expand=True, fill="both", padx=28, pady=25)
        ttk.Label(box, text="SUAMS", font=("Segoe UI", 25, "bold"), foreground="#1555a5").pack(pady=(10,2))
        ttk.Label(box, text="Smart University Academic Management System").pack(pady=(0,22))
        ttk.Label(box, text="Username").pack(anchor="w")
        self.username = ttk.Entry(box, width=35)
        self.username.pack(fill="x", pady=(4,12))
        ttk.Label(box, text="Password").pack(anchor="w")
        self.password = ttk.Entry(box, show="*", width=35)
        self.password.pack(fill="x", pady=(4,16))
        ttk.Button(box, text="Sign in", command=self.login).pack(fill="x", ipady=5)
        ttk.Label(box, text="Demo: student / teacher / admin / exam  |  Password: 1234",
                  foreground="#52657e", wraplength=340).pack(pady=18)
        self.password.bind("<Return>", lambda _e: self.login())
        self.username.focus_set()
    def login(self):
        user = authenticate(self.username.get(), self.password.get())
        if not user:
            messagebox.showerror("Login failed", "Invalid username or password.")
            return
        self.on_success(user)
