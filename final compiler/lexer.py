import ply.lex as lex  # Importing PLY for lexical analysis

# --- Lexer Definition ---
# Lexer definition using PLY
class Lexer:
    # List of token types
    tokens = [
        "TT_identifier",  # Variable names or keywords
        "TT_int",  # Integer literals
        "TT_float",  # Floating-point literals
        "TT_string",  # String literals
        "TT_plus", "TT_sub", "TT_mul", "TT_div",  # Arithmetic operators
        "TT_equ", "TT_dequ",  # Assignment and equality operators
        "TT_less", "TT_greater", "TT_leq", "TT_geq",  # Comparison operators
        "TT_lparen", "TT_rparen",  # Parentheses
        "TT_lbracket", "TT_rbracket",  # Brackets
        "TT_comma", "TT_colon",  # Comma and colon
        "TT_pow",
        "TT_if", "TT_elif", "TT_else", "TT_while", "TT_for", "TT_in", "TT_print",  # Keywords
    ]

    # Token regex patterns
    t_TT_plus = r"\+"
    t_TT_sub = r"-"
    t_TT_mul = r"\*"
    t_TT_div = r"/"
    t_TT_equ = r"="
    t_TT_dequ = r"=="
    t_TT_less = r"<"
    t_TT_greater = r">"
    t_TT_leq = r"<="
    t_TT_geq = r">="
    t_TT_lparen = r"\("
    t_TT_rparen = r"\)"
    t_TT_lbracket = r"\["
    t_TT_rbracket = r"\]"
    t_TT_comma = r","
    t_TT_colon = r":"
    t_TT_pow = r"\*\*"
    t_ignore = " \t"  # Ignore spaces and tabs

    # Map keywords to specific token types
    keywords = {
        "if": "TT_if",
        "elif": "TT_elif",
        "else": "TT_else",
        "while": "TT_while",
        "for": "TT_for",
        "in": "TT_in",
        "print": "TT_print",
    }

    # Match identifiers or keywords
    def t_TT_identifier(self, t):
        r"[a-zA-Z_][a-zA-Z0-9_]*"
        t.type = self.keywords.get(t.value, "TT_identifier")  # Check if identifier is a keyword
        return t

    # Match floating-point literals
    def t_TT_float(self, t):
        r"(\d+\.\d+|\d+\.|\.\d+)([eE][-+]?\d+)?"
        t.value = float(t.value)  # Convert to float
        return t

    # Match integer literals
    def t_TT_int(self, t):
        r"\d+"
        t.value = int(t.value)  # Convert to integer
        return t
        
    # Match string literals
    def t_TT_string(self, t):
        r'"([^"\\]*(\\.[^"\\]*)*)"'
        t.value = t.value[1:-1]  # Remove quotes
        return t

    # Track line numbers for better error reporting
    def t_newline(self, t):
        r"\n+"
        t.lexer.lineno += len(t.value)

    # Ignore single-line comments
    def t_singleline_comment(self, t):
        r"\#.*"
        pass

    # Ignore multi-line comments
    def t_multiline_comment(self, t):
        r"/\*.*?\*/"
        pass

    # Handle invalid characters
    def t_error(self, t):
        print(f"Illegal character '{t.value}'")
        t.lexer.skip(1)

    # Initialize the lexer
    def __init__(self):
        self.lexer = lex.lex(module=self)

tokens = Lexer.tokens