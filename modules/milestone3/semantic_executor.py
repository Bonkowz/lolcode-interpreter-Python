from symbol_table import SymbolTable
import syntax_tree as AST
import tkinter as tk
import tkinter.simpledialog as sd

class SemanticExecutor:
    container_nodes = ["PROGRAM", "DECLARATION_BLOCK"]

    def __init__(self, ast, gui_root, update_symbol_table_callback=None, console_widget=None):
        self.symbol_table = SymbolTable()
        self.syntax_tree = ast
        self.functions = {}
        self.symbol_table.declare("IT", None)

        self.update_symbol_table_callback = update_symbol_table_callback
        self.console_widget = console_widget  # For GUI console
        self.gui_root = gui_root


    def _console_print(self, text):
        if self.console_widget:
            self.console_widget.insert(tk.END, text + "\n")
            self.console_widget.see(tk.END)
        else:
            print(text)

    def execute(self):
        if self.syntax_tree.root:
            self._execute_node(self.syntax_tree.root)

    def _execute_node(self, node):
        node_type = node.kind

        if node_type in self.container_nodes:
            for child in node.children:
                self._execute_node(child)
        elif node_type == "DECLARATION":
            var_name = node.identifier
            initial_value = None
            print(var_name)
            if node.value: initial_value = self._evaluate_expression(node.value)
            self.symbol_table.declare(var_name, initial_value)

            print(f"Executed: Declared variable '{var_name}' with value: {initial_value}")
        elif node_type == "ASSIGN":
            self._reassignment(node)
        elif node_type == "OUTPUT":
            self._output(node)
        elif node_type == "INPUT":
            self._input(node)
        # TODO: add nodetypes for raw operations
        elif node_type == "TYPECAST":
            self._typecast(node)
        elif node_type == "CONDITIONAL":
            self._if_statements(node)
        elif node_type == "SWITCH":
            self._switch_statements(node)
        elif node_type == "LOOP":
            self._loop_statements(node)
        elif node_type == "FUNCTION_BLOCK":
            self._function_declaration(node)
        elif node_type == "FUNCTION_CALL":
            return_value = self._function_call(node)
            self.symbol_table.assign("IT", return_value)

    def _evaluate_expression(self, node):
        result = None
        # arithmetic
        if isinstance(node, AST.LiteralNode): result = self._evaluate_literal(node.value)
        elif isinstance(node, AST.IdentifierNode): result = self.symbol_table.get_value(node.value)
        elif isinstance(node, AST.OperationNode):
            op_type = node.op_type
            # multi operand
            if op_type == "MULTI_AND_OP": result = all(bool(self._evaluate_expression(child)) for child in node.children)
            if op_type == "MULTI_OR_OP":  result = any(bool(self._evaluate_expression(child)) for child in node.children)
            # unary
            if op_type == "NOT OP": 
                result = not bool(self._evaluate_expression(node.children[0]))
                self.symbol_table.assign("IT", result)
                return result
            # arithmetic 
            left = self._evaluate_expression(node.children[0])
            right = self._evaluate_expression(node.children[1])
            # comparison
            if op_type == "EQUAL_OP": result = left == right
            elif op_type == "NOT_EQUAL_OP": result = left != right

            left = self._to_numeric(left)
            right = self._to_numeric(right)
            if isinstance(left, float) or isinstance(right, float):
                left, right = float(left), float(right)

            # print(left, right)
            if op_type == "SUM_OP": result = left + right
            elif op_type == "SUB_OP": result = left - right
            elif op_type == "MUL_OP": result = left * right
            elif op_type == "DIV_OP": 
                if right == 0:
                    raise ValueError(f"Division by zero.")
                result = left / right
            elif op_type == "MOD_OP": result = left % right
            elif op_type == "MAX_OP": result = max(left, right)
            elif op_type == "MIN_OP": result = min(left, right)
        # elif isinstance(node, AST.OperationNode): 

            # boolean 
            left = bool(left)
            right = bool(right)
            if op_type == "AND_OP": result = left and right
            elif op_type == "OR_OP": result = left or right
            elif op_type == "XOR_OP": result = left != right # Boolean XOR is equivalent to !=
        elif isinstance(node, AST.StringConcatNode):
            result = self._concatenation(node)

        self.symbol_table.assign("IT", result)
        return result
    
    def _evaluate_literal(self, literal):
        # TROOF literal
        if literal == "WIN": return True
        if literal == "FAIL": return False
        # YARN literal
        if literal.startswith('"') and literal.endswith('"'): return literal[1:-1]
        # NUMBAR literal (float)
        if '.' in literal: return float(literal)
        # NUMBR literal (int)
        return int(literal)
    
    def _to_numeric(self, value):
        if isinstance(value, (int, float)): return value
        if isinstance(value, str):
            try:
                if '.' in value:
                    return float(value)
                return int(value)
            except ValueError:
                raise ValueError(f"Cannot cast string '{value}' to a number for arithmetic.")
        if isinstance(value, bool):
            return 1 if value else 0
        if value is None:
            return 0
        raise TypeError(f"Unsupported type for arithmetic: {type(value)}")

    def _reassignment(self, node):
        var_name = node.identifier
        new_value = self._evaluate_expression(node.value)
        self.symbol_table.assign(var_name, new_value)
    
    # def _output(self, node):
    #     operands = node.children
    #     for operand in operands:
    #         value = self._evaluate_expression(operand)
    #         value = self._typecast_to_string(value)
    #         print(value, end="")
    #     print("")
    
    def _output(self, node):
        for operand in node.children:
            value = self._evaluate_expression(operand)
            value = self._typecast_to_string(value)
            if self.update_symbol_table_callback:
                self.update_symbol_table_callback(self.symbol_table.dump())
            value = str(value)
            if self.console_widget:
                self.console_widget.insert(tk.END, value)
                self.console_widget.see(tk.END)
            else:
                print(value)
        self.console_widget.insert(tk.END, "\n")
    
    def _typecast_to_string(self, value):
        if value is None: value = "NOOB"
        elif value is True: value = "TROOF"
        elif value is False: value = "FAIL"
        else: value = str(value)
        return value

    def _input(self, node):
        var_name = node.children[0].value
        # GUI input dialog
        # if self.console_widget:
        str_input = sd.askstring("INPUT", f"Enter value for {var_name}:", parent = self.gui_root)
        # else:
            # str_input = input(f"Enter value for {var_name}: ")
        self.symbol_table.assign(var_name, str_input)
        if self.update_symbol_table_callback:
            self.update_symbol_table_callback(self.symbol_table.dump())
        # self._console_print(f"Input -> {var_name} = {str_input}")


    def _concatenation(self, node):
        operands = node.children
        string  = ""
        for operand in operands:
            value = self._evaluate_expression(operand)
            value = self._typecast_to_string(value)
            string += value
        return string
    
    def _typecast(self, node):
        new_type = node.value.value
        var_name = node.identifier
        old_var = self.symbol_table.get_value(var_name)
        new_var = None
        if new_type == "TROOF": new_var = bool(old_var)
        elif new_type == "NUMBAR": new_var = float(old_var) 
        elif new_type == "NUMBR": new_var = int(old_var)
        elif new_type == "YARN": new_var = str(old_var)
        self.symbol_table.assign(var_name, new_var)
        return new_var
    
    def _if_statements(self, node):
        self.symbol_table.assign("IT", self._evaluate_expression(node.condition))
        condition_result = self.symbol_table.get_value("IT")
        if condition_result:
            if node.if_true_block:
                for child in node.if_true_block.children:
                    self._execute_node(child)
        else:
            if node.if_false_block:
                for child in node.if_false_block.children:
                    self._execute_node(child)
    
    def _switch_statements(self, node):
        self.symbol_table.assign("IT", self.symbol_table.get_value(node.variable))
        switch_value = self.symbol_table.get_value("IT")
        
        case_matched = False
        is_executing = False

        for case in node.children:
            if case.condition:
                case_value = self._evaluate_expression(case.condition)
                if not case_matched and switch_value == case_value:
                    case_matched = True
                    is_executing = True
                if is_executing:
                    for child in case.children:
                        self._execute_node(child)
                    if case.stopper:
                        is_executing = False 
            # default case has no condition
            elif not case_matched or is_executing:
                for child in case.children:
                    self._execute_node(child)
                break
            
    def _loop_statements(self, node):
        counter_var = node.counter
        while True:
            condition_result = bool(self._evaluate_expression(node.condition))
            if node.condition_type == "TIL" and condition_result: break  
            if node.condition_type == "WILE" and not condition_result: break  

            for child in node.children:
                self._execute_node(child)

            current_val = self.symbol_table.get_value(counter_var)
            current_val = self._to_numeric(current_val) 
            if node.operation == "UPPIN":
                self.symbol_table.assign(counter_var, current_val + 1)
            elif node.operation == "NERFIN":
                self.symbol_table.assign(counter_var, current_val - 1)

    def _function_declaration(self, node):
        func_name = node.name[0]
        if func_name in self.functions:
            raise Exception(f"Function '{func_name}' already declared.")
        self.functions[func_name] = node
        print(f"Executed: Declared function '{func_name}'")

    def _function_call(self, node):
        func_name = node.name[0]
        if func_name not in self.functions:
            raise Exception(f"Function '{func_name}' is not defined.")

        func_node = self.functions[func_name]
        call_args = node.parameters.children
        func_params = func_node.parameters.children

        if len(call_args) != len(func_params):
            raise Exception(f"Function '{func_name}' expects {len(func_params)} arguments, but got {len(call_args)}.")

        original_symbol_table = self.symbol_table
        local_symbol_table = SymbolTable()
        local_symbol_table.declare("IT", None)

        for param_node, arg_node in zip(func_params, call_args):
            param_name = param_node.value
            arg_value = self._evaluate_expression(arg_node)
            local_symbol_table.declare(param_name, arg_value)
        self.symbol_table = local_symbol_table
        # self.symbol_table.print_table()
        
        for statement in func_node.function_body:
            self._execute_node(statement)


        return_value = None
        if func_node.expression is not None:
            return_value = self._evaluate_expression(func_node.expression)
        self.symbol_table = original_symbol_table

        return return_value