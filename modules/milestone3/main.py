from lexical_analyzer import tokenize  
from syntax_analyzer import SyntaxAnalyzer
from semantic_executor import SemanticExecutor

if __name__ == "__main__":
    file = "sample.lol"
    with open(file, "r") as f:
        code = f.read()

    # NOTE: Tokenize (from lexical_analyzer)
    tokens = tokenize(code)
    # NOTE: Generate AST 
    pt = SyntaxAnalyzer(tokens) 
    pt.ASTree.print_tree()
    # NOTE: Execute the program using the generated AST
    print("\n--- EXECUTING PROGRAM ---\n")
    executor = SemanticExecutor(pt.ASTree)
    executor.execute()
    executor.symbol_table.print_table()
