class AbstractSyntaxTree:
    def __init__(self, root=None):
        self.root = root
    def print_tree(self):
        if self.root:
            print(self.root.title)
            self._print_tree_recursive(self.root, "", True)
        else:
            print("Empty Tree")
    def _print_tree_recursive(self, node, prefix, is_last):
        # Loop through children
        for i, child in enumerate(node.children):
            is_last_child = (i == len(node.children) - 1)
            # Determine the branch symbol
            branch = "└── " if is_last_child else "├── "
            # Print the current child
            print(f"{prefix}{branch}{child.title}")
            # Calculate the prefix for the next level
            # If this was the last child, the vertical bar '│' is not needed for its descendants
            new_prefix = prefix + ("    " if is_last_child else "│   ")
            # Recurse
            self._print_tree_recursive(child, new_prefix, is_last_child)

class ASTNode:
    def __init__(self, kind, title=None):
        self.kind = kind
        self.title = title if title is not None else kind
        self.children = []

    def add_child(self, child):
        self.children.append(child)

class LiteralNode(ASTNode):
    def __init__(self, value):
        super().__init__("LITERAL", f"LITERAL: {value}")
        self.value = value

class IdentifierNode(ASTNode):
    def __init__(self, value):
        super().__init__("IDENTIFIER", f"IDENTIFIER: {value}")
        self.value = value

class ProgramNode(ASTNode): 
    def __init__(self):
        super().__init__("PROGRAM")

class DeclarationBlockNode(ASTNode):
    def __init__(self):
        super().__init__("DECLARATION_BLOCK")

class DeclarationNode(ASTNode):
    def __init__(self, var_name, value_node=None):
        super().__init__("DECLARATION")
        self.title = f"DECLARE: {var_name}"
        self.identifier = var_name 
        self.value = value_node 
        if value_node:
            self.add_child(value_node)


class AssignmentNode(ASTNode):
    def __init__(self, var_name, value_node=None):
        super().__init__("ASSIGN")
        self.title = f"ASSIGN"
        self.identifier = var_name 
        self.value = value_node 
        self.title = f"ASSIGN: {var_name}"
        if value_node:
            self.add_child(value_node)

class OperationNode(ASTNode):
    def __init__(self, op_type):
        super().__init__("OPERATION")
        self.title = f"OPERATION: - {op_type}"
        self.op_type = op_type
        self.operands = self.children

    def getValue(self):
        return

class TypecastNode(ASTNode):
    def __init__(self, var_name, value_node=None):
        super().__init__("TYPECAST")
        self.title = f"TYPECAST"
        self.identifier = var_name 
        self.value = value_node 
        self.title = f"CAST: {var_name}"
        if value_node:
            self.add_child(value_node)

class OutputNode(ASTNode):
    def __init__(self):
        super().__init__("OUTPUT")
        self.title = f"OUTPUT"
        self.strings = self.children

class InputNode(ASTNode):
    def __init__(self):
        super().__init__("INPUT")
        self.title = f"INPUT"
        self.inputs = self.children

class StringConcatNode(ASTNode):
    def __init__(self):
        super().__init__("STR_CONCAT")
        self.title = f"CONCAT"
        self.operands = self.children

class ConditionalBlockNode(ASTNode):
    def __init__(self):
        super().__init__("CONDITIONAL BLOCK")
        self.title = f"CONDITION BLOCK"
        self.condition = None

class ConditionalNode(ASTNode):
    def __init__(self):
        super().__init__("CONDITIONAL")
        self.title = f"CONDITION"
        self.condition = None
        self.if_true_blocks = None
        self.else_if_blocks = None
        self.if_false_block = None

class SwitchNode(ASTNode):
    def __init__(self, variable):
        super().__init__("SWITCH")
        self.variable = variable
        self.title = f"SWITCH"
        self.cases = self.children

class SwitchBlockNode(ASTNode):
    def __init__(self, condition = None):
        super().__init__("SWITCH BlOCK")
        self.title = f"SWITCH BLOCK"
        self.stopper = False
        self.condition = condition 
        self.cases = self.children

class LoopNode(ASTNode):
    def __init__(self, var_name, operation, counter, condition_type, condition):
        super().__init__("LOOP")
        self.title = f"LOOP = {var_name}"
        self.label = var_name
        self.operation = operation
        self.counter = counter
        self.condition_type = condition_type 
        self.condition = condition

class FunctionArgsNode(ASTNode):
    def __init__(self):
        super().__init__("FUNCTION_ARGS")
        self.title = f"FUNCTION_ARGS"

class FunctionNode(ASTNode):
    def __init__(self, name, parameters = None, expression = None):
        super().__init__("FUNCTION_BLOCK")
        self.title = f"FUNCTION"
        self.name = name
        self.parameters = parameters
        self.function_body = self.children 
        self.expression = expression
        self.has_return_value = expression is not None

class FunctionCallNode(ASTNode):
    def __init__(self, name, parameters = None):
        super().__init__("FUNCTION_CALL")
        self.title = f"FUNCTION_CALL"
        self.name = name
        self.parameters = parameters





    
