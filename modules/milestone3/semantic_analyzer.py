from symbol_table import SymbolTable

# track var declarations
# track var ass
# symbol table
# convert raw lexeme into proper values (in python)

class SemanticAnalyzer:

    # initialize the semantic analyzer and create symbol table
    def __init__(self):
        self.symbol_table = SymbolTable()
        self.symbol_table = SyntaxTree()
        # to implement implicit IT variable
        self.symbol_table.declare("IT", None)

    # Convert token list into semantic
    # Declare, Assign, Updates IT
    def process_tokens2(self, tokens):
        i = 0
        while i < len(tokens):
            lexeme, token_type = tokens[i]
            # NOTE: declaration block 
            if token_type == "BLOCK_START":
                block_node = SyntaxNode("DECLARE_BLOCK")
                

    def process_tokens(self, tokens):
        processed_tokens = []
        i = 0
        while i < len(tokens):
            lexeme, token_type = tokens[i]

            # ==== VARIABLE_DECLARATION
            if token_type == "VARIABLE_DECLARATION":
                # Next token must be IDENTIFIER
                if i + 1 < len(tokens) and tokens[i+1][1] == "IDENTIFIER":
                    var_name = tokens[i+1][0]

                    # Check if next-next token is ITZ - I HAS A var ITZ value
                    if i + 2 < len(tokens) and tokens[i+2][1] == "VARIABLE_ASSIGN":
                        # to ensure that it has value to read
                        if i + 3 < len(tokens):
                            value_lex, value_type = tokens[i+3]

                            # convert lexeme into python val
                            try:
                                value = int(value_lex)
                            except ValueError:
                                value = value_lex
                            
                            # record declaration
                            processed_tokens.append(("DECLARE", var_name))

                            # assign value to variable
                            processed_tokens.append(("ASSIGN", var_name, value))

                            # update IT var with the same val
                            processed_tokens.append(("ASSIGN", "IT", value))
                            i += 4
                            continue

                    # declaration only - I HAS A var
                    processed_tokens.append(("DECLARE", var_name))
                    i += 2
                    continue

            # === OUTPUT
            elif token_type == "OUTPUT":
                # must be followed by a value/toke
                if i + 1 < len(tokens):
                    value_lex, value_type = tokens[i+1]

                    # clean literal - remove quotes
                    try:
                        value = self._clean_literal(value_lex)
                    except ValueError:
                        value = value_lex

                    # VISIBLE updates IT
                    processed_tokens.append(("ASSIGN", "IT", value))
                    i += 2
                    continue

            # === VARIABLE_ASSIGN
            elif token_type == "VARIABLE_ASSIGN":
                # check the previous token for <identifier>
                if i > 0 and tokens[i-1][1] == "IDENTIFIER" and i + 1 < len(tokens):
                    var_name = tokens[i-1][0]
                    value_lex, value_type = tokens[i+1]
                    
                    try:
                        value = int(value_lex)
                    except ValueError:
                        value = value_lex
                    processed_tokens.append(("ASSIGN", var_name, value))
                    processed_tokens.append(("ASSIGN", "IT", value))
                    i += 2
                    continue
            
            # no matching rule -> move to next token
            i += 1

        # apply it to the symbol table
        for token in processed_tokens:
            
            # declaration - add new var to the table
            if token[0] == "DECLARE": 
                self.symbol_table.declare(token[1])
            # assignment - update var value
            elif token[0] == "ASSIGN":
                self.symbol_table.assign(token[1], token[2])

    #NOTE: HELPER FUNCTIONS 
    # print the symbol table
    def print_symbol_table(self):
        self.symbol_table.print_table()
    # convert raw lexeme into proper values (in python) - str, bool, int, float
    def _clean_literal(self, value_lex):
        # str - remove surrounding quotes for string literal
        if (len(value_lex) >= 2) and (
            (value_lex.startswith('"') and value_lex.endswith('"')) or
            (value_lex.startswith("'") and value_lex.endswith("'"))
        ):
            return value_lex[1:-1]   # strip quotes
        # bool -  convert WIN/FAIL
        if value_lex == "WIN":
            return True
        if value_lex == "FAIL":
            return False
        # int
        try:
            return int(value_lex)
        except ValueError:
            pass
        # float
        try:
            return float(value_lex)
        except ValueError:
            pass
        # keep as identifier / raw value
        return value_lex
    

