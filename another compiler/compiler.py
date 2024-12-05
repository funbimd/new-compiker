import sys
from lexer import Lexer  # Importing the lexer for lexical analysis
from parser_1 import Parser  # Importing the parser for syntactic analysis
from Interpreter import Interpreter  # Importing the interpreter for executing the AST

def main():
    """
    Entry point of the script. Handles the end-to-end process of interpreting a source code file.
    """
    if len(sys.argv) < 2:
        print("Usage: python script.py <source_file>")
        sys.exit(1)

    source_file = sys.argv[1]

    # Load the source code from the specified file
    try:
        with open(source_file, 'r') as file:
            source_code = file.read()
    except FileNotFoundError:
        print(f"Error: File '{source_file}' not found.")
        sys.exit(1)

    # Lexical Analysis: Tokenize the source code
    lexer = Lexer(source_code)
    tokens = lexer.getTokens()

    # Parsing: Generate Abstract Syntax Trees (ASTs)
    parser = Parser(tokens)
    asts = parser.runParse()

    # Interpretation: Execute the ASTs
    interpreter = Interpreter(asts)
    interpreter.execute()

if __name__ == "__main__":
    main()
