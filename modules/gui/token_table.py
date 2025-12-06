import tkinter as tk
from tkinter import ttk

class TokenTable:
    def __init__(self, parent):
        self.frame = tk.Frame(parent, bd=2, relief="groove")

 
        tk.Label(self.frame, text="Lexemes", bg="#e6e6e6").pack(fill="x")

        
        tree_frame = tk.Frame(self.frame)
        tree_frame.pack(expand=True, fill="both")

   
        self.tree = ttk.Treeview(
            tree_frame,
            columns=("Lexeme", "Classification"),
            show="headings",
            height=15
        )
        self.tree.heading("Lexeme", text="Lexeme")
        self.tree.heading("Classification", text="Classification")
        self.tree.pack(side="left", expand=True, fill="both")

    def populate(self, tokens):
        # Clear old entries
        self.tree.delete(*self.tree.get_children())

        for idx, (lexeme, token_type) in enumerate(tokens, start=1):
            self.tree.insert("", "end", values=(lexeme, token_type))
