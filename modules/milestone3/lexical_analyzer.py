import re

TOKEN_PATTERNS = [
    # NOTE: KEYWORDS
    # Program structure
    (r'\bHAI\b', 'PROGRAM_START'),
    (r'\bKTHXBYE\b', 'PROGRAM_END'),
    (r'\bWAZZUP\b', 'BLOCK_START'),
    (r'\bBUHBYE\b', 'BLOCK_END'),

    # Comments
    (r'\bBTW.*', 'COMMENT'),
    # does not work with curr implement
    (r'\bOBTW\b.*?\bTLDR\b', 'MULTI_COMMENT'),

    # Variable declaration
    (r'\bI HAS A\b', 'VARIABLE_DECLARATION'),
    (r'\bITZ\b', 'VARIABLE_ASSIGN'),
    (r'\bR\b', 'VARIABLE_REASSIGN'),

    # Arithmetic operators
    (r'\bSUM OF\b', 'SUM_OP'),
    (r'\bDIFF OF\b', 'SUB_OP'),
    (r'\bPRODUKT OF\b', 'MUL_OP'),
    (r'\bQUOSHUNT OF\b', 'DIV_OP'),
    (r'\bMOD OF\b', 'MOD_OP'),
    (r'\bBIGGR OF\b', 'MAX_OP'),
    (r'\bSMALLR OF\b', 'MIN_OP'),

    # Logical Operator
    (r'\bBOTH OF\b', 'AND_OP'),
    (r'\bEITHER OF\b', 'OR_OP'),
    (r'\bWON OF\b', 'XOR_OP'),
    (r'\bNOT\b', 'NOT_OP'),
    (r'\bANY OF\b', 'MULTI_OR_OP'),
    (r'\bALL OF\b', 'MULTI_AND_OP'),

    (r'\bBOTH SAEM\b', 'EQUAL_OP'),
    (r'\bDIFFRINT\b', 'NOT_EQUAL_OP'),

    # Concatenation and Typecast
    (r'\bSMOOSH\b', 'STRING_CONCAT'),
    (r'\bMAEK\b', 'TYPECAST'),
    (r'\bA\b', 'A_KEYWORD'),
    (r'\bAN\b', 'AN_KEYWORD'),
    (r'\+', 'AN_KEYWORD'),
    (r'\bIS NOW A\b', 'TYPE_CHANGE'),

    # Output
    (r'\bVISIBLE\b', 'OUTPUT'),

    # Input
    (r'\bGIMMEH\b', 'INPUT'),

    # Conditionals
    (r'\bO RLY\?(?=\s*$)', 'IF_START'),
    (r'\bYA RLY\b', 'IF_TRUE'),
    (r'\bMEBBE\b', 'IF_ELSE_IF'),
    (r'\bNO WAI\b', 'IF_FALSE'),
    (r'\bOIC\b', 'IF_END'),

    # Switch Case
    (r'\bWTF\?(?=\s*$)', 'SWITCH_START'),
    (r'\bOMG\b', 'CASE'),
    (r'\bOMGWTF\b', 'DEFAULT_CASE'),

    # Loop
    (r'\bIM IN YR\b', 'LOOP_START'),
    (r'\bUPPIN\b', 'LOOP_INCREMENT'),
    (r'\bNERFIN\b', 'LOOP_DECREMENT'),
    (r'\bYR\b', 'LOOP_VAR'),
    (r'\bTIL\b', 'UNTIL_COND'),
    (r'\bWILE\b', 'WHILE_COND'),
    (r'\bIM OUTTA YR\b', 'LOOP_END'),

    # Function
    (r'\bHOW IZ I\b', 'FUNC_START'),
    (r'\bIF U SAY SO\b', 'FUNC_END'),
    (r'\bGTFO\b', 'FUNC_EXIT'),
    (r'\bFOUND YR\b', 'FUNC_RETURN'),
    (r'\bI IZ\b', 'FUNC_CALL'),
    (r'\bMKAY\b', 'EXPR_END'),

    # LITERALS
    (r'"[^"]*"', 'YARN_LITERAL'),
    (r'-?(0|[1-9][0-9]*)\.[0-9]+', 'NUMBAR_LITERAL'),
    (r'-?(0|[1-9][0-9]*)', 'NUMBR_LITERAL'),
    (r'\b(WIN|FAIL)\b', 'TROOF_LITERAL'),
    (r'\b(NUMBR|NUMBAR|YARN|TROOF|NOOB)\b', 'TYPE_LITERAL'),

    # IDENTIFIERS
    (r'\b[a-zA-Z][a-zA-Z0-9_]*\b', 'IDENTIFIER'),
    (r'\b[a-zA-Z][a-zA-Z0-9_]*\b', 'IDENTIFIER'),
]

line_count = 1
# FUNCTIONS
def tokenize(codeLines):
    codeLines = codeLines.split("\n")
    codeLines = [i for i in codeLines if not i.isspace()]
    # print(codeLines)

    tokens = []
    for line_num, code in enumerate(codeLines):
        skipping = False
        if re.search(r'OBTW',code):
            print("working")
            skipping = True
        if re.search(r'TLDR',code):
            skipping = True
            continue
        if skipping:
            continue
        i = 0
        while i < len(code):
            # Skip whitespace
            if code[i].isspace():
                i += 1
                global line_count
                line_count += 1
                continue

            match_found = False
            for pattern, token_type in TOKEN_PATTERNS:
                # --- FIX APPLIED HERE ---
                flags = 0
                # Only apply re.DOTALL (re.S) for the multiline comment pattern
                if token_type == 'MULTI_COMMENT': flags = re.DOTALL
                regex = re.compile(pattern, flags) # Compile with flags
                # ------------------------
                match = regex.match(code, i)
                if match:
                    lexeme = match.group(0)
                    i = match.end()
                    match_found = True
                    if token_type in ["MULTI_COMMENT", "COMMENT"]:
                        break
                    tokens.append((lexeme, token_type))
                    break
            if not match_found:
                tokens.append((code, "ERROR"))
                raise Exception(f"Syntax Error at line {line_num+1}")
        tokens.append((line_num+1,"EOL"))  
    tokens.append((line_num+1,"EOF"))
    return tokens
# end of tokenize

def print_token_info(token_num, lexeme, token_type):
    print(f"Token No : {token_num:02d}  |  {lexeme:15}  ------->  |  {token_type}")
# end of print_token_info

# main
def main():
    # name = input("Enter file: ")
    # filename = f"testcases/{name}.lol"
    filename = f"sample.lol"

    print("\n************************** PROCESSING SOURCE CODE... **************************\n")
    try:
        with open(filename, "r") as src:
            token_num = 1
            token_counts = {}
            code = src.read()

            tokens = tokenize(code)
            for lexeme, token_type in tokens:
                if token_type == "ERROR":
                    print(f"ERROR AT LINE: {line_count}")
                    break
                else:
                    print_token_info(token_num, lexeme, token_type)
                token_counts[token_type] = token_counts.get(token_type, 0) + 1
                token_num += 1

            print("\n================ TOKEN TYPE SUMMARY ================\n")
            for token_type, count in token_counts.items():
                print(f"{token_type:<15} : {count}")

            print("\nProcessing complete!\n")

    except FileNotFoundError:
        print(f"Error: {filename} not found.")
# end of main

# RUN
if __name__ == "__main__":
    main()