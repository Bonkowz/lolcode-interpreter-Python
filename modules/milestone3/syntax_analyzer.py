import syntax_tree as AST

# TODO: fix comment eol problem 

class SyntaxAnalyzer:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0 
        self.current_token = tokens[0] 
        self.ASTree = AST.AbstractSyntaxTree()
        for i in tokens:
            print(i)
        self.program()

    statement_start = [  
        'VARIABLE_DECLARATION',
        'OUTPUT',
        'INPUT',
        'NOT_OP',
        'STRING_CONCAT',
        'IF_START',
        'SWITCH_START',
        'FUNC_START',
        'FUNC_CALL',
        'TYPECAST',
        'VARIABLE_ASSIGN',
        'IDENTIFIER',
        'VARIABLE_REASSIGN',
        'LOOP_START',
        'FUNC_START',
        'FUNC_CALL'
    ]
    literal_start = [
        'YARN_LITERAL',
        'NUMBAR_LITERAL',
        'NUMBR_LITERAL',
        'TROOF_LITERAL',
        'TYPE_LITERAL'
    ]
    operation_start = [
        'SUM_OP',
        'SUB_OP',
        'MUL_OP',
        'DIV_OP',
        'MOD_OP',
        'MAX_OP',
        'MIN_OP',
        'AND_OP',
        'OR_OP',
        'XOR_OP',
        'NOT_OP',
        'EQUAL_OP',
        'NOT_EQUAL_OP'
    ]
    inf_logic_operation_start = [
        'MULTI_OR_OP',
        'MULTI_AND_OP',
    ]
    starts = []
    starts.extend(statement_start)
    starts.extend(literal_start)
    starts.extend(operation_start)
    starts.extend(inf_logic_operation_start)
    type_literals = [
        "NOOB",
        "TROOF",
        "NUMBAR",
        "NUMBR",
        "YARN",
    ]

    # HELPERS
    def eat(self, token_type):
        current_token_type = self.current_token[1]
        if current_token_type == token_type:
            print("eated", self.current_token)
            self.pos += 1
            if self.pos < len(self.tokens):
                old_token = self.current_token
                self.current_token = self.tokens[self.pos]
                return old_token 
            # TODO: raise exp if oob
        else: 
            raise Exception(f"Expected {token_type}, but got {current_token_type}")

    #! bad eat 
    def eat_any(self):
        print("eated cheat")
        self.pos += 1
        if self.pos < len(self.tokens):
            old_token = self.current_token
            self.current_token = self.tokens[self.pos]
            return old_token 

    def peek_type(self):
        return self.tokens[self.pos][1]
    #! bad peek
    def peek_type_next(self):
        return self.tokens[self.pos+1][1] #! this part will fail if exceeding bounds
    
    # NOTE: GRAMMARS
    def program(self):
        self.ASTree.root = AST.ProgramNode()
        self.eat_eol()
        self.eat("PROGRAM_START")
        self.eat_eol()
        ### 
        self.program_body(self.ASTree.root)
        self.eat("PROGRAM_END")
        self.eat_eol()
        self.eat("EOF")

    def program_body(self, parent_node):
        if self.peek_type() == "BLOCK_START":
            declaration_block_node = self.declaration_block()
            parent_node.add_child(declaration_block_node)
            self.eat_eol()
            self.statement_list(parent_node)
        else:
            self.statement_list(parent_node)

    def declaration_block(self):
        node = AST.DeclarationBlockNode()
        self.eat("BLOCK_START")
        self.eat_eol()
        self.declaration_list(node)
        while self.peek_type() == "EOL":
            self.eat_eol()
        self.eat("BLOCK_END")
        return node

    def declaration_list(self, parent_node):
        if self.peek_type() == "VARIABLE_DECLARATION":
            declaration_node = self.declaration()
            parent_node.add_child(declaration_node)
            self.eat_eol()
            self.declaration_list(parent_node)
        else:
            return

    def statement_list(self, parent_node):
        if self.peek_type() in self.starts:
            statement_node = self.single_statement()
            if statement_node:
                parent_node.add_child(statement_node)
            self.eat_eol()
            self.statement_list(parent_node)
        if self.peek_type() == "EOL":
            self.eat_eol()

    def single_statement(self):
        if self.peek_type() == "VARIABLE_DECLARATION": 
            return self.declaration() 
        elif self.peek_type() == "OUTPUT": 
            return self.output()
        elif self.peek_type() == "INPUT": 
            return self.input()

        # TODO: add if conditions to other operators
        elif self.peek_type() == "NOT_OP":
            return self.not_operation()
        elif self.peek_type() in self.operation_start: 
            operation = self.operation()
            if self.peek_type_next() == "IF_START":
                self.eat_eol()
                return self.conditional_if(operation)
            else: return operation
        elif self.peek_type() in self.inf_logic_operation_start:
            return self.logic_operator_inf()
        elif self.peek_type() == "STRING_CONCAT":
            return self.string_operator()

        elif self.peek_type() == "SWITCH_START":
            return self.conditional_switch()
        elif self.peek_type() == "LOOP_START":
            return self.loop()

        elif self.peek_type() == "FUNC_START":
            return self.function()
        elif self.peek_type() == "FUNC_CALL":
            return self.function_call()
        
        elif self.peek_type() == "IDENTIFIER": 
            return self.assignment()
        elif self.peek_type() == "TYPECAST": 
            return self.typecast()

    def conditional_if(self, operation):
        node = AST.ConditionalNode() 
        node.condition = operation 

        self.eat("IF_START")
        self.eat_eol()

        self.eat("IF_TRUE")
        self.eat_eol()

        true_node = AST.ConditionalBlockNode()
        self.statement_list(true_node)
        node.if_true_block = true_node 
        if true_node.children: node.add_child(true_node)

        # NOTE: else if are (condition, node) tuples 
        # elif_node = AST.ConditionalBlockNode()
        # self.conditional_elif(elif_node)
        # node.else_if_block = elif_node 
        # if elif_node.children: node.add_child(elif_node)

        false_node = AST.ConditionalBlockNode()
        self.conditional_else_block(false_node)
        node.if_false_block = false_node 
        if false_node.children: node.add_child(false_node)

        self.eat("IF_END")
        return node
    def conditional_elif(self, parent_node):
        if self.peek_type() == "IF_ELSE_IF":
            node = AST.ConditionalBlockNode()
            self.eat("IF_ELSE_IF")
            operation = self.operation()
            self.eat_eol()
            self.statement_list(node)
            parent_node.add_child((operation, node))
            self.conditional_elif(parent_node)
    def conditional_else_block(self, parent_node):
        if self.peek_type() == "IF_FALSE":
            self.eat("IF_FALSE")
            self.eat_eol()
            self.statement_list(parent_node)
     # TODO: partition into specific types of operations 
    def operation_type(self):
        #NOTE: cheat eat here vvv
        if self.peek_type() in self.operation_start: 
            return self.eat_any()[1]
    def operation(self):
        op_type = self.operation_type()

        #! stupid temporary fix
        if op_type == "NOT_OP": 
            print("WORKING")
            node = AST.OperationNode("NOT OP")
            self.operand(node)
            return node
        #! end of stupid fix
        
        node = AST.OperationNode(op_type)
        self.operands(node)
        return node
    def not_operation(self):
        node = AST.OperationNode("NOT OP")
        self.eat("NOT_OP")
        self.operand(node)
        return node
    
    def operand(self, parent_node):
        if self.peek_type() in self.operation_start: parent_node.add_child(self.operation())
        else: parent_node.add_child(self.factor())
    def operands(self, parent_node):
        if self.peek_type() in self.operation_start: parent_node.add_child(self.operation())
        else: parent_node.add_child(self.factor())
        self.eat("AN_KEYWORD")
        if self.peek_type() in self.operation_start: parent_node.add_child(self.operation())
        else: parent_node.add_child(self.factor())
    def inf_operands(self, parent_node):
        if self.peek_type() == "AN_KEYWORD":
            self.eat("AN_KEYWORD")
            if self.peek_type() in self.operation_start: parent_node.add_child(self.operation())
            else: parent_node.add_child(self.factor())
            self.inf_operands(parent_node)
    
    def logic_operator_inf(self):
        op_type = self.inf_op_type()
        node = AST.OperationNode(op_type)
        self.operand(node)
        self.inf_operands(node)
        self.eat("EXPR_END")
        return node
    def inf_op_type(self):
        if self.peek_type() == "MULTI_OR_OP": return self.eat("MULTI_OR_OP")[1]
        elif self.peek_type() == "MULTI_AND_OP": return self.eat("MULTI_AND_OP")[1]
    
    def string_operator(self):
        node = AST.StringConcatNode()
        self.eat("STRING_CONCAT")
        node.add_child(self.factor())
        self.string_tail(node)
        return node
    def string_tail(self,parent_node):
        if self.peek_type() == "AN_KEYWORD":
            self.factor_extend(parent_node)

    def factor_extend(self, parent_node):
        self.eat("AN_KEYWORD")
        string = self.factor()
        parent_node.add_child(string)
        self.factor_extend_tail(parent_node)
    def factor_extend_tail(self, parent_node):
        if self.peek_type() == "AN_KEYWORD":
            self.factor_extend(parent_node)

    def output(self):
        node = AST.OutputNode()
        self.eat("OUTPUT")
        if self.peek_type() == "NOT_OP": string = self.not_operation()
        elif self.peek_type() in self.operation_start: string = self.operation()
        elif self.peek_type() == "STRING_CONCAT": string = self.string_operator()
        elif self.peek_type() in self.inf_logic_operation_start: string = self.logic_operator_inf()
        else: string = self.factor()
        node.add_child(string)
        self.print_tail(node)
        return node 
    def print_tail(self, parent_node):
        if self.peek_type() == "AN_KEYWORD":
           self.print_extend(parent_node) 
        else:
            return
    # NOTE: variation here 
    def print_extend(self, parent_node):
        self.eat("AN_KEYWORD")
        if self.peek_type() in self.operation_start: string = self.operation()
        elif self.peek_type() == "STRING_CONCAT": string = self.string_operator()
        elif self.peek_type() in self.inf_logic_operation_start: string = self.logic_operator_inf()
        else: string = self.factor()
        parent_node.add_child(string)
        self.print_tail(parent_node)

    def input(self):
        node = AST.InputNode()
        self.eat("INPUT")
        string = self.factor()
        node.add_child(string)
        self.print_tail(node)
        return node 

    # TODO: Missing operands for declaration here
    def declaration(self):
        self.eat("VARIABLE_DECLARATION")
        var_name = self.eat("IDENTIFIER")[0]
        value_node = self.initialization_opt()
        return AST.DeclarationNode(var_name, value_node)
    def initialization_opt(self):
        if self.peek_type() == "VARIABLE_ASSIGN":
            self.eat("VARIABLE_ASSIGN")
            if self.peek_type() in self.operation_start: return self.operation()
            else: return self.factor()
    
    def assignment(self): 
        var_name = self.eat("IDENTIFIER")[0]
        node = None

        #! stupid temporary fix (move this up later)
        if self.peek_type() == "EOL":
            return self.conditional_switch(var_name)  

        if self.peek_type() == "TYPE_CHANGE":
            self.eat("TYPE_CHANGE")
            value = self.type_literal()
            node = AST.TypecastNode(var_name, value)
            node.identifier = var_name
            node.value = value

        if self.peek_type() == "VARIABLE_REASSIGN":
            self.eat("VARIABLE_REASSIGN")
            if self.peek_type() == "TYPECAST":
                value = self.typecast().value
                node = AST.TypecastNode(var_name, value)
                node.identifier = var_name
                node.value = value
            else:
                args = None
                if self.peek_type() in self.operation_start: args = self.operation()
                elif self.peek_type() == "STRING_CONCAT": args = self.string_operator()
                elif self.peek_type() in self.inf_logic_operation_start: args = self.logic_operator_inf()
                else: args = self.factor()
                node = AST.AssignmentNode(var_name, args)
                node.identifier = var_name
                node.value = args 
        return node
    
    def typecast(self):
        self.eat("TYPECAST")
        name = self.eat("IDENTIFIER")[0]
        value = self.typecast_maek_tail()
        node = AST.TypecastNode(name, value)
        return node 
    def typecast_maek_tail(self):
        value = None
        if self.peek_type() == "TYPE_LITERAL":
            value = self.type_literal()
        elif self.peek_type() == "A_KEYWORD": 
            self.eat("A_KEYWORD")
            value = self.type_literal()
        return value 

    def conditional_switch(self, var_name):
        node = AST.SwitchNode(var_name)
        self.factor()
        self.eat_eol()
        self.eat("SWITCH_START")
        self.eat_eol()
        self.switch_cases(node)
        self.switch_default(node)
        self.eat("IF_END")
        return node
    def switch_cases(self, parent_node):
        if self.peek_type() == "CASE":
            self.eat("CASE")
            condition = self.literal()
            self.eat_eol()
            node = AST.SwitchBlockNode(condition)
            self.statement_list(node)
            if self.peek_type() == "FUNC_EXIT":
                self.eat("FUNC_EXIT")
                self.eat_eol()
                node.stopper = True
            parent_node.add_child(node)
            self.switch_cases(parent_node)
    def switch_default(self, parent_node):
        if self.peek_type() == "DEFAULT_CASE":
            self.eat("DEFAULT_CASE")
            self.eat_eol()
            node = AST.SwitchBlockNode()
            node.stopper = True
            self.statement_list(node)
            parent_node.add_child(node)
        
    def loop(self):
        self.eat("LOOP_START") 
        var_name = self.eat("IDENTIFIER")[0]
        operation = self.loop_operation()
        self.eat("LOOP_VAR")
        counter = self.eat("IDENTIFIER")[0]
        condition_type = self.loop_until()
        condition = self.operation()
        self.eat_eol()

        node = AST.LoopNode(var_name, operation, counter, condition_type, condition)
        self.statement_list(node)
        self.eat("LOOP_END")
        var_name = self.eat("IDENTIFIER") 
        return node
    def loop_operation(self):
        if self.peek_type() == "LOOP_INCREMENT": return self.eat("LOOP_INCREMENT")[0]
        elif self.peek_type() == "LOOP_DECREMENT": return self.eat("LOOP_DECREMENT")[0]
    def loop_until(self):
        if self.peek_type() == "UNTIL_COND": return self.eat("UNTIL_COND")[0]
        elif self.peek_type() == "WHILE_COND": return self.eat("WHILE_COND")[0]
        self.operation()
    
    def function(self):
        self.eat("FUNC_START")
        name = self.eat("IDENTIFIER")
        node = AST.FunctionNode(name)
        args = AST.FunctionArgsNode()
        self.function_args_opt(args)
        self.eat_eol()
        self.statement_list(node)
        ret_expr = self.function_return()
        node.parameters = args
        node.expression = ret_expr
        self.eat_eol()
        self.eat("FUNC_END")
        return node
    def function_args_opt(self, parent_node):
        if self.peek_type() == "LOOP_VAR":
            self.function_arguments(parent_node)
    def function_arguments(self, parent_node):
        self.eat("LOOP_VAR")
        args = None
        if self.peek_type() in self.operation_start: args = self.operation()
        elif self.peek_type() == "STRING_CONCAT": args = self.string_operator()
        elif self.peek_type() in self.inf_logic_operation_start: args = self.logic_operator_inf()
        else: args = self.factor()
        parent_node.add_child(args)
        self.function_arguments_extend(parent_node)
    def function_arguments_extend(self, parent_node):
        if self.peek_type() == "AN_KEYWORD":
            self.eat("AN_KEYWORD")
            self.eat("LOOP_VAR")
            args = None
            if self.peek_type() in self.operation_start: args = self.operation()
            elif self.peek_type() == "STRING_CONCAT": args = self.string_operator()
            elif self.peek_type() in self.inf_logic_operation_start: args = self.logic_operator_inf()
            else: args = self.factor()
            parent_node.add_child(args)
            self.function_arguments_extend(parent_node)
    def function_return(self):
        if self.peek_type() == "FUNC_EXIT":
            self.eat("FUNC_EXIT")
            return None
        if self.peek_type() == "FUNC_RETURN":
            self.eat("FUNC_RETURN")
            args = None
            print("WORKING")
            if self.peek_type() in self.operation_start: args = self.operation()
            elif self.peek_type() == "STRING_CONCAT": args = self.string_operator()
            elif self.peek_type() in self.inf_logic_operation_start: args = self.logic_operator_inf()
            else: args = self.factor()
            return args 
    
    def function_call(self):
        self.eat("FUNC_CALL")
        name = self.eat("IDENTIFIER")
        args = AST.FunctionArgsNode()
        self.function_call_args(args)
        node = AST.FunctionCallNode(name, args)
        self.eat("EXPR_END")
        return node
    def function_call_args(self, parent_node):
        if self.peek_type() == "LOOP_VAR":
            self.eat("LOOP_VAR")
            args = None
            if self.peek_type() in self.operation_start: args = self.operation()
            elif self.peek_type() == "STRING_CONCAT": args = self.string_operator()
            elif self.peek_type() in self.inf_logic_operation_start: args = self.logic_operator_inf()
            else: args = self.factor()
            parent_node.add_child(args)
            self.function_call_args_extend(parent_node)
    def function_call_args_extend(self, parent_node):
        if self.peek_type() == "AN_KEYWORD":
            self.eat("AN_KEYWORD")
            self.eat("LOOP_VAR")
            args = None
            if self.peek_type() in self.operation_start: args = self.operation()
            elif self.peek_type() == "STRING_CONCAT": args = self.string_operator()
            elif self.peek_type() in self.inf_logic_operation_start: args = self.logic_operator_inf()
            else: args = self.factor()
            parent_node.add_child(args)
            self.function_call_args_extend(parent_node)

    def literal(self):
        #NOTE: cheat eat here vvv
        if self.peek_type() in self.literal_start: 
            value = self.eat_any()[0] 
            return AST.LiteralNode(value)
    def type_literal(self):
        #NOTE: cheat eat here vvv
        if self.peek_type() == "TYPE_LITERAL": 
            value = self.eat_any()[0] 
            return AST.LiteralNode(value)
    def identifier(self):
        #NOTE: cheat eat here vvv
        if self.peek_type() == "IDENTIFIER": 
            value = self.eat_any()[0] 
            return AST.IdentifierNode(value)

    # TODO: fix this factor bug
    def factor(self):
        if self.peek_type() == "IDENTIFIER": return self.identifier()
        else: return self.literal()

    def eat_eol(self):
        while self.peek_type() == "EOL":
            self.eat("EOL")