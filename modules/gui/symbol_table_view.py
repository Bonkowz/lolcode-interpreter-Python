from tkinter import ttk

class SymbolTableView(ttk.Treeview):
    def __init__(self, parent):
        super().__init__(parent, columns=('value',))
        self.heading('#0', text='Variable')
        self.heading('value', text='Value')
        self.column('value', width=150)

    def update_symbols(self, symbols):
        # Clear old rows
        self.delete(*self.get_children())
        # Add current symbols
        for name, value in symbols.items():
            self.insert("", "end", text=name, values=(value,))
