import tkinter as tk
from tkinter import ttk
import sys
import os

# Adjust path to access modules
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
MODULES_DIR = os.path.join(CURRENT_DIR, "modules")
GUI_DIR = os.path.join(MODULES_DIR, "gui")
MILESTONE3_DIR = os.path.join(MODULES_DIR, "milestone3")

if GUI_DIR not in sys.path:
    sys.path.append(GUI_DIR)
if MILESTONE3_DIR not in sys.path:
    sys.path.append(MILESTONE3_DIR)

from file_explorer import FileExplorer
from text_editor import TextEditor
from token_table import TokenTable
from lexical_analyzer import tokenize
from syntax_analyzer import SyntaxAnalyzer
from semantic_executor import SemanticExecutor


# main window
root = tk.Tk()
root.title("CMSC 124 Interpreter GUI")
root.geometry("1300x700")

# Title 
top_frame = tk.Frame(root)
top_frame.grid(row=0, column=0, columnspan=3, sticky="nsew")
tk.Label(top_frame, text="HAI 124", font=("Arial", 14, "bold")).pack()

# Text Editor
text_editor = TextEditor(root)
text_editor.frame.grid(row=2, column=0, sticky="nsew")

# File Explorer
def load_file_into_editor(path):
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    text_editor.load_text(content)

file_explorer_component = FileExplorer(root, on_file_select=load_file_into_editor)
file_explorer_component.frame.grid(row=1, column=0, sticky="nsew")

# Token table
tokens_component = TokenTable(root)
tokens_component.frame.grid(row=2, column=1, sticky="nsew")

# symbol table
symbol_frame = tk.Frame(root, bd=2, relief="groove")
symbol_frame.grid(row=2, column=2, sticky="nsew")
tk.Label(symbol_frame, text="SYMBOL TABLE").pack(anchor="w")
symbol_table = ttk.Treeview(symbol_frame, columns=("Ident", "Value"), show="headings")
symbol_table.heading("Ident", text="Identifier")
symbol_table.heading("Value", text="Value")
symbol_table.pack(expand=True, fill="both")


# --- UPDATE SYMBOL TABLE ---
def update_symbol_table_view(symbols):
    symbol_table.delete(*symbol_table.get_children())
    for name, value in symbols.items():
        symbol_table.insert("", "end", values=(name, value))


# RUN / EXECUTE
def execute_code():
    file_path = file_explorer_component.selected_file
    if not file_path:
        console.insert(tk.END, "No file selected!\n")
        return

    console.insert(tk.END, f"\n--- Executing {os.path.basename(file_path)} ---\n")

    try:
        # with open(file_path, "r", encoding="utf-8") as f:
            # code = f.read()

        code = text_editor.editor.get("1.0", "end-1c")

        tokens = tokenize(code)
        tokens_component.populate(tokens)

        ast = SyntaxAnalyzer(tokens).ASTree

        executor = SemanticExecutor(
            ast,
            root,
            update_symbol_table_callback=update_symbol_table_view,
            console_widget=console
        )

        executor.execute()

    except Exception as e:
        console.insert(tk.END, f"Error: {e}\n")


# EXECUTE button
run_frame = tk.Frame(root)
run_frame.grid(row=3, column=0, columnspan=3, pady=5)
run_button = tk.Button(run_frame, text="EXECUTE", width=20, height=2, command=execute_code)
run_button.pack()

# console
console_frame = tk.Frame(root, bd=2, relief="groove")
console_frame.grid(row=4, column=0, columnspan=3, sticky="nsew")
tk.Label(console_frame, text="CONSOLE").pack(anchor="w")
console = tk.Text(console_frame, height=10, bg="black", fg="white")
console.pack(expand=True, fill="both")

# grid weights
root.grid_rowconfigure(2, weight=3)
root.grid_rowconfigure(4, weight=1)

root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)

root.mainloop()
