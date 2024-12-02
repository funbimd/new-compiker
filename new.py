
import tkinter as tk
from tkinter import scrolledtext
import ply.lex as lex
import ply.yacc as yacc

# --- AST Node Classes ---
class ASTNode:
    pass

class Program(ASTNode):
    def __init__(self, statements):
        self.statements = statements

    def __repr__(self):
        return f"Program(statements={self.statements})"

class IfStatement(ASTNode):
    def __init__(self, condition, body, elif_clauses, else_clause):
        self.condition = condition
        self.body = body
        self.elif_clauses = elif_clauses
        self.else_clause = else_clause

    def __repr__(self):
        return (f"IfStatement(condition={self.condition}, "
                f"body={self.body}, "
                f"elif_clauses={self.elif_clauses}, "
                f"else_clause={self.else_clause})")

class PrintStatement(ASTNode):
    def __init__(self, expression):
        self.expression = expression

    def __repr__(self):
        return f"PrintStatement(expression={self.expression})"

class BinaryOp(ASTNode):
    def __init__(self, operator, left, right):
        self.operator = operator
        self.left = left
        self.right = right

    def __repr__(self):
        return f"BinaryOp(operator='{self.operator}', left={self.left}, right={self.right})"

class Literal(ASTNode):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        if isinstance(self.value, str):
            return f'"{self.value}"'
        return f"{self.value}"

class Variable(ASTNode):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Variable(name={self.name})"

# # --- Symbol Table ---
# class SymbolTable:
#     def __init__(self):
#         self.symbols = {}

#     def declare(self, name, value=None):
#         self.symbols[name] = value

#     def assign(self, name, value):
#         self.symbols[name] = value

#     def lookup(self, name):
#         if name not in self.symbols:
#             raise Exception(f"Variable '{name}' not declared.")
#         return self.symbols[name]

#     def __repr__(self):
#         return f"SymbolTable(symbols={self.symbols})"

# # --- Semantic Analyzer ---
# class SemanticAnalyzer:
#     def __init__(self, symbol_table, output_callback):
#         self.symbol_table = symbol_table
#         self.output_callback = output_callback

#     def analyze(self, node):
#         if isinstance(node, Program):
#             for statement in node.statements:
#                 self.analyze(statement)
#         elif isinstance(node, PrintStatement):
#             value = self.evaluate_expression(node.expression)
#             self.output_callback(f"{value}\n")  # Send output to callback
#         elif isinstance(node, BinaryOp):
#             self.analyze(node.left)
#             self.analyze(node.right)
#         elif isinstance(node, Variable):
#             self.symbol_table.lookup(node.name)
#         elif isinstance(node, Literal):
#             pass
#         else:
#             raise Exception(f"Unknown node type: {type(node)}")

#     def evaluate_expression(self, expr):
#         if isinstance(expr, Literal):
#             return expr.value
#         elif isinstance(expr, Variable):
#             return self.symbol_table.lookup(expr.name)
#         elif isinstance(expr, BinaryOp):
#             left = self.evaluate_expression(expr.left)
#             right = self.evaluate_expression(expr.right)
#             if expr.operator == '+':
#                 return left + right
#             elif expr.operator == '-':
#                 return left - right
#             elif expr.operator == '*':
#                 return left * right
#             elif expr.operator == '/':
#                 return left / right
#         else:
#             raise Exception(f"Unknown expression type: {type(expr)}")

# --- Lexer Definition ---
class Lexer:
    tokens = [
        "TT_identifier",
        "TT_int",
        "TT_plus",
        "TT_sub",
        "TT_mul",
        "TT_div",
        "TT_equ",
        "TT_dequ",
        "TT_less",
        "TT_greater",
        "TT_print",
        "TT_lparen",
        "TT_rparen",
    ]

    t_TT_plus = r"\+"
    t_TT_sub = r"-"
    t_TT_mul = r"\*"
    t_TT_div = r"/"
    t_TT_equ = r"="
    t_TT_dequ = r"=="
    t_TT_less = r"<"
    t_TT_greater = r">"
    t_TT_lparen = r"\("
    t_TT_rparen = r"\)"
    t_ignore = " \t"

    def t_TT_identifier(self, t):
        r"[a-zA-Z_][a-zA-Z0-9_]*"
        keywords = {"print": "TT_print"}
        t.type = keywords.get(t.value, "TT_identifier")
        return t

    def t_TT_int(self, t):
        r"\d+"
        t.value = int(t.value)
        return t

    def t_newline(self, t):
        r"\n+"
        t.lexer.lineno += len(t.value)

    def t_error(self, t):
        print(f"Illegal character '{t.value}'")
        t.lexer.skip(1)

    def __init__(self):
        self.lexer = lex.lex(module=self)

# --- Parser Definition ---
class Parser:
    tokens = Lexer.tokens

    precedence = (
        ('left', 'TT_plus', 'TT_sub'),
        ('left', 'TT_mul', 'TT_div'),
    )

    def __init__(self):
        self.lexer = Lexer()
        self.parser = yacc.yacc(module=self)

    def p_program(self, p):
        "program : statement_list"
        p[0] = Program(p[1])

    def p_statement_list(self, p):
        """statement_list : statement_list statement
                          | statement"""
        if len(p) == 3:
            p[0] = p[1] + [p[2]]
        else:
            p[0] = [p[1]]

    def p_statement(self, p):
        """statement : print_statement"""
        p[0] = p[1]

    def p_print_statement(self, p):
        "print_statement : TT_print TT_lparen expression TT_rparen"
        p[0] = PrintStatement(p[3])

    def p_expression(self, p):
        """expression : expression TT_plus expression
                      | expression TT_sub expression
                      | expression TT_mul expression
                      | expression TT_div expression
                      | TT_int
                      | TT_identifier"""
        if len(p) == 2:
            if isinstance(p[1], int):
                p[0] = Literal(p[1])
            else:
                p[0] = Variable(p[1])
        else:
            p[0] = BinaryOp(p[2], p[1], p[3])

    def parse(self, data):
        return self.parser.parse(data, lexer=self.lexer.lexer)

# --- GUI IDE ---
class IDE:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Custom IDE")
        self.setup_widgets()

    def setup_widgets(self):
        # Editor
        self.editor = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=80, height=20)
        self.editor.pack(fill=tk.BOTH, expand=True)

        # Output Console
        self.output_console = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=80, height=10, state='disabled', bg='black', fg='white')
        self.output_console.pack(fill=tk.BOTH, expand=True)

        # Run Button
        self.run_button = tk.Button(self.root, text="Run", command=self.run_code)
        self.run_button.pack()

    def append_output(self, text):
        self.output_console.configure(state='normal')
        self.output_console.insert(tk.END, text)
        self.output_console.configure(state='disabled')
        self.output_console.see(tk.END)

    def run_code(self):
        # Clear output console
        self.output_console.configure(state='normal')
        self.output_console.delete(1.0, tk.END)
        self.output_console.configure(state='disabled')

        # Retrieve code from editor
        code = self.editor.get(1.0, tk.END)

        # Run code through parser and semantic analyzer
        parser = Parser()
        # symbol_table = SymbolTable()
        # analyzer = SemanticAnalyzer(symbol_table, self.append_output)

        try:

            ast = parser.parse(code)
            self.append_output(f"AST: {ast}\n")
            # self.append_output("Running Semantic Analysis...\n")
            # analyzer.analyze(ast)
            # self.append_output("Semantic analysis completed successfully!\n")
        except Exception as e:
            self.append_output(f"Error: {str(e)}\n")

    def run(self):
        self.root.mainloop()

# --- Run the IDE ---
if __name__ == "__main__":
    IDE().run()