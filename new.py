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

class WhileLoop(ASTNode):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def __repr__(self):
        return f"WhileLoop(condition={self.condition}, body={self.body})"

class ForLoop(ASTNode):
    def __init__(self, variable, iterable, body):
        self.variable = variable
        self.iterable = iterable
        self.body = body

    def __repr__(self):
        return f"ForLoop(variable={self.variable}, iterable={self.iterable}, body={self.body})"

class Assignment(ASTNode):
    def __init__(self, variable, value):
        self.variable = variable
        self.value = value

    def __repr__(self):
        return f"Assignment(variable={self.variable}, value={self.value})"

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

class Array(ASTNode):
    def __init__(self, elements):
        self.elements = elements

    def __repr__(self):
        return f"Array(elements={self.elements})"

class ArrayAccess(ASTNode):
    def __init__(self, array, index):
        self.array = array
        self.index = index

    def __repr__(self):
        return f"ArrayAccess(array={self.array}, index={self.index})"

# --- Lexer Definition ---
class Lexer:
    tokens = [
        "TT_identifier",
        "TT_int",
        "TT_string",
        "TT_plus",
        "TT_sub",
        "TT_mul",
        "TT_div",
        "TT_equ",
        "TT_dequ",
        "TT_less",
        "TT_greater",
        "TT_leq",
        "TT_geq",
        "TT_lparen",
        "TT_rparen",
        "TT_lbracket",
        "TT_rbracket",
        "TT_comma",
        "TT_colon",
        "TT_if",
        "TT_elif",
        "TT_else",
        "TT_while",
        "TT_for",
        "TT_in",
        "TT_print",
    ]

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
    t_ignore = " \t"

    keywords = {
        "if": "TT_if",
        "elif": "TT_elif",
        "else": "TT_else",
        "while": "TT_while",
        "for": "TT_for",
        "in": "TT_in",
        "print": "TT_print",
    }

    def t_TT_identifier(self, t):
        r"[a-zA-Z_][a-zA-Z0-9_]*"
        t.type = self.keywords.get(t.value, "TT_identifier")
        return t

    def t_TT_int(self, t):
        r"\d+"
        t.value = int(t.value)
        return t

    def t_TT_string(self, t):
        r'"[^"]*"'
        t.value = t.value[1:-1]  # Remove quotes
        return t

    def t_newline(self, t):
        r"\n+"
        t.lexer.lineno += len(t.value)

    def t_singleline_comment(self, t):
        r"\#.*"
        pass  # Ignore single-line comments

    def t_multiline_comment(self, t):
        r"/\*.*?\*/"
        pass  # Ignore multi-line comments

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
        ('nonassoc', 'TT_less', 'TT_greater', 'TT_leq', 'TT_geq', 'TT_dequ'),
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
        """statement : assignment
                     | print_statement
                     | if_statement
                     | while_loop
                     | for_loop"""
        p[0] = p[1]

    def p_assignment(self, p):
        "assignment : TT_identifier TT_equ expression"
        p[0] = Assignment(Variable(p[1]), p[3])

    def p_if_statement(self, p):
        """if_statement : TT_if expression TT_colon statement_list elif_clauses else_clause"""
        p[0] = IfStatement(p[2], p[4], p[5], p[6])

    def p_elif_clauses(self, p):
        """elif_clauses : elif_clauses TT_elif expression TT_colon statement_list
                        | empty"""
        if len(p) == 6:
            p[0] = p[1] + [(p[3], p[5])]
        else:
            p[0] = []

    def p_else_clause(self, p):
        """else_clause : TT_else TT_colon statement_list
                       | empty"""
        if len(p) == 4:
            p[0] = p[3]
        else:
            p[0] = None

    def p_while_loop(self, p):
        "while_loop : TT_while expression TT_colon statement_list"
        p[0] = WhileLoop(p[2], p[4])

    def p_for_loop(self, p):
        "for_loop : TT_for TT_identifier TT_in expression TT_colon statement_list"
        p[0] = ForLoop(Variable(p[2]), p[4], p[6])

    def p_expression(self, p):
        """expression : expression TT_plus expression
                      | expression TT_sub expression
                      | expression TT_mul expression
                      | expression TT_div expression
                      | expression TT_dequ expression
                      | expression TT_less expression
                      | expression TT_greater expression
                      | expression TT_leq expression
                      | expression TT_geq expression
                      | array_access
                      | TT_int
                      | TT_string
                      | TT_identifier
                      | array"""
        if len(p) == 2:
            if isinstance(p[1], int) or isinstance(p[1], str):
                p[0] = Literal(p[1])
            elif isinstance(p[1], list):
                p[0] = Array(p[1])
            else:
                p[0] = p[1]
        else:
            p[0] = BinaryOp(p[2], p[1], p[3])

    def p_array(self, p):
        "array : TT_lbracket elements TT_rbracket"
        p[0] = Array(p[2])

    def p_array_access(self, p):
        "array_access : TT_identifier TT_lbracket expression TT_rbracket"
        p[0] = ArrayAccess(array=Variable(p[1]), index=p[3])

    def p_elements(self, p):
        """elements : elements TT_comma expression
                    | expression
                    | empty"""
        if len(p) == 4:
            p[0] = p[1] + [p[3]]
        elif len(p) == 2 and p[1] is not None:
            p[0] = [p[1]]
        else:
            p[0] = []

    def p_print_statement(self, p):
        "print_statement : TT_print TT_lparen expression TT_rparen"
        p[0] = PrintStatement(p[3])

    def p_empty(self, p):
        "empty :"
        p[0] = None

    def parse(self, data):
        return self.parser.parse(data, lexer=self.lexer.lexer)

# --- IR Generator ---
class IRGenerator:
    def __init__(self):
        self.instructions = []
        self.temp_counter = 0
        self.label_counter = 0

    def new_temp(self):
        temp = f"t{self.temp_counter}"
        self.temp_counter += 1
        return temp

    def new_label(self):
        label = f"L{self.label_counter}"
        self.label_counter += 1
        return label

    def generate(self, node):
        if isinstance(node, Program):
            for statement in node.statements:
                self.generate(statement)
        elif isinstance(node, Assignment):
            temp = self.generate(node.value)
            self.instructions.append(f"STORE {temp}, {node.variable.name}")
        elif isinstance(node, PrintStatement):
            temp = self.generate(node.expression)
            self.instructions.append(f"PRINT {temp}")
        elif isinstance(node, BinaryOp):
            left = self.generate(node.left)
            right = self.generate(node.right)
            temp = self.new_temp()
            self.instructions.append(f"{node.operator.upper()} {left}, {right}, {temp}")
            return temp
        elif isinstance(node, Literal):
            temp = self.new_temp()
            self.instructions.append(f"LOAD {node.value}, {temp}")
            return temp
        elif isinstance(node, Variable):
            return node.name
        else:
            raise Exception(f"Unsupported AST node: {type(node)}")

        return None

    def get_ir(self):
        return "\n".join(self.instructions)

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

        # Run code through parser
        parser = Parser()

        try:
            ast = parser.parse(code)
            ir_gen = IRGenerator()
            ir_gen.generate(ast)
            ir = ir_gen.get_ir()
            self.append_output(f"IR:\n{ir}\n")
        except Exception as e:
            self.append_output(f"Error: {str(e)}\n")

    def run(self):
        self.root.mainloop()

# --- Run the IDE ---
if __name__ == "__main__":
    IDE().run()
