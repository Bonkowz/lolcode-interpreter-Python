import tkinter as tk
from tklinenums import TkLineNumbers

class TextEditor:
    def __init__(self, parent):
        self.frame = tk.Frame(parent, bd=2, relief="groove")
        tk.Label(self.frame, text="TEXT EDITOR").pack(anchor="w")

        self.editor = tk.Text(self.frame)
        self.editor.pack(expand=True, fill="both", side = "right")

        # Add line numbers to left side of text editor (buggy ;-;)
        linenums = TkLineNumbers(self.frame, self.editor, justify = "center", colors = ("#505050", "#ffffff"))
        linenums.pack(fill = "y", side = "left")

        # Update line numbers (buggy ;-;)
        self.editor.bind("<<Modified>>", lambda event: self.editor.after_idle(linenums.redraw), add = True)

    def load_text(self, text):
        # delete ther existing text
        self.editor.delete("1.0", tk.END) 
        # insert the new text
        self.editor.insert("1.0", text)
