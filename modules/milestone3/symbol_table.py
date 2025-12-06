# Symbol table for storing variables and their values
class SymbolTable:
    def __init__(self):
        # initializes an empty symbol table
        self.table = {} # dictionary storing var names as keys and their values

    # declares a new variable in the symbol table
    def declare(self, name, value=None):
        # name - name of var to declare
        # value (optional) - initial value of the var
        if name in self.table: # If the var has been declared
            raise Exception(f"Variable '{name}' already declared.")
        self.table[name] = value

    # assigns a value to an already declared var
    def assign(self, name, value):
        if name not in self.table:
            raise Exception(f"Variable '{name}' not declared.")
        self.table[name] = value

    # retrieves the value of a declared var
    def get_value(self, name):
        if name not in self.table:
            raise Exception(f"Variable '{name}' not declared.")
        return self.table[name] # returns the the value of var

    # for printing only
    def print_table(self):
        print("\n================ SYMBOL TABLE ================")
        print(f"{'Identifier':<15} | {'Value':<20}")
        print("----------------------------------------------")
        for name, value in self.table.items():
            print(f"{name:<15} | {str(value):<20}")
        print("==============================================\n")

    def dump(self):
        # return a copy of the internal dictionary
        return self.table.copy()