import tkinter as tk
from tkinter import filedialog
import os

class FileExplorer:
    def __init__(self, parent, on_file_select=None):
        # main container frame
        self.frame = tk.Frame(parent, bd=2, relief="groove")

        # title bar
        tk.Label(self.frame, text="FILE EXPLORER", bg="#e6e6e6").pack(fill="x")

        # holding the entry and button
        entry_frame = tk.Frame(self.frame)
        entry_frame.pack(expand=True, fill="x", padx=2, pady=2)

        # Entry to show selected file
        self.file_entry = tk.Entry(entry_frame)
        self.file_entry.pack(side="left", expand=True, fill="x")

        # folder icon to open file dialog
        self.open_button = tk.Button(
            entry_frame,
            text="📁",
            width=3,
            command=self.open_file
        )

        # Internal state: stores the full selected file path
        self.open_button.pack(side="left", padx=2)

        # Callback to notify main GUI when a file is selected
        self.selected_file = None
        self.on_file_select = on_file_select

    def open_file(self):
        file_path = filedialog.askopenfilename(
            parent=self.frame,
            initialdir=".", # open in same directory
            # initialdir=os.path.expanduser("~"),
            title="Select a file",
            filetypes=[("Text Files", "*.lol"), ("All Files", "*.*")]
        )
        if file_path:
            # Save full path internally
            self.selected_file = file_path

            # Display only the filename in the entry
            self.file_entry.delete(0, tk.END)
            self.file_entry.insert(0, os.path.basename(file_path))

            # Trigger callback to update TextEditor
            if self.on_file_select:
                self.on_file_select(file_path)
