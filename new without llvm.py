import tkinter as tk  # Importing tkinter for GUI creation
from tkinter import scrolledtext  # Importing ScrolledText for multi-line text widgets
import ply.lex as lex  # Importing PLY for lexical analysis
import ply.yacc as yacc  # Importing PLY for syntax analysis

# --- AST Node Classes ---
# Base class for all AST nodes
class ASTNode:
    pass

# Represents the entire program as a collection of statements
class Program(ASTNode):
    def __init__(self, statements):
        self.statements = statements  # List of all statements in the program

    def __repr__(self):
        return f"Program(statements={self.statements})"

# Represents an if-elif-else statement in the program
class IfStatement(ASTNode):
    def __init__(self, condition, body, elif_clauses, else_clause):
        self.condition = condition  # Condition for the if clause
        self.body = body  # Body of the if clause
        self.elif_clauses = elif_clauses  # List of (condition, body) tuples for elif clauses
        self.else_clause = else_clause  # Body of the else clause

    def __repr__(self):
        return (f"IfStatement(condition={self.condition}, "
                f"body={self.body}, "
                f"elif_clauses={self.elif_clauses}, "
                f"else_clause={self.else_clause})")

# Represents a while loop
class WhileLoop(ASTNode):
    def __init__(self, condition, body):
        self.condition = condition  # Condition for the loop
        self.body = body  # Body of the loop

    def __repr__(self):
        return f"WhileLoop(condition={self.condition}, body={self.body})"

# Represents a for loop
class ForLoop(ASTNode):
    def __init__(self, variable, iterable, body):
        self.variable = variable  # Loop variable
        self.iterable = iterable  # Iterable object (e.g., array or range)
        self.body = body  # Body of the loop

    def __repr__(self):
        return f"ForLoop(variable={self.variable}, iterable={self.iterable}, body={self.body})"

# Represents a variable assignment
class Assignment(ASTNode):
    def __init__(self, variable, value):
        self.variable = variable  # Variable being assigned to
        self.value = value  # Value being assigned

    def __repr__(self):
        return f"Assignment(variable={self.variable}, value={self.value})"

# Represents a print statement
class PrintStatement(ASTNode):
    def __init__(self, expression):
        self.expression = expression  # Expression to be printed

    def __repr__(self):
        return f"PrintStatement(expression={self.expression})"

# Represents a binary operation (e.g., addition, subtraction)
class BinaryOp(ASTNode):
    def __init__(self, operator, left, right):
        self.operator = operator  # Operator (e.g., +, -, *)
        self.left = left  # Left operand
        self.right = right  # Right operand

    def __repr__(self):
        return f"BinaryOp(operator='{self.operator}', left={self.left}, right={self.right})"

# Represents a literal value (e.g., integer, string)
class Literal(ASTNode):
    def __init__(self, value):
        self.value = value  # Literal value

    def __repr__(self):
        if isinstance(self.value, str):
            return f'"{self.value}"'
        return f"{self.value}"

# Represents a variable
class Variable(ASTNode):
    def __init__(self, name):
        self.name = name  # Name of the variable

    def __repr__(self):
        return f"Variable(name={self.name})"

# Represents an array
class Array(ASTNode):
    def __init__(self, elements):
        self.elements = elements  # List of array elements

    def __repr__(self):
        return f"Array(elements={self.elements})"

# Represents accessing an element of an array
class ArrayAccess(ASTNode):
    def __init__(self, array, index):
        self.array = array  # Array being accessed
        self.index = index  # Index of the element

    def __repr__(self):
        return f"ArrayAccess(array={self.array}, index={self.index})"

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

    # Match integer literals
    def t_TT_int(self, t):
        r"\d+"
        t.value = int(t.value)  # Convert to integer
        return t

    # Match floating-point literals
    def t_TT_float(self, t):
        r"\d+\.\d+"
        t.value = float(t.value)  # Convert to float
        return t
        
    # Match string literals
    def t_TT_string(self, t):
        r'"[^"]*"'
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

# --- Parser Definition ---
# Syntax parser using PLY
class Parser:
    # Define the tokens used
    tokens = Lexer.tokens

    # Operator precedence for arithmetic and comparisons
    precedence = (
        ('left', 'TT_plus', 'TT_sub'),
        ('left', 'TT_mul', 'TT_div'),
        ('nonassoc', 'TT_less', 'TT_greater', 'TT_leq', 'TT_geq', 'TT_dequ'),
    )

    # Initialize the parser and lexer
    def __init__(self):
        self.lexer = Lexer()
        self.parser = yacc.yacc(module=self)

    # Parse the program as a list of statements
    def p_program(self, p):
        "program : statement_list"
        p[0] = Program(p[1])

    # Parse a list of statements
    def p_statement_list(self, p):
        """statement_list : statement_list statement
                          | statement"""
        if len(p) == 3:
            p[0] = p[1] + [p[2]]
        else:
            p[0] = [p[1]]

    # Define a statement
    def p_statement(self, p):
        """statement : assignment
                     | print_statement
                     | if_statement
                     | while_loop
                     | for_loop"""
        p[0] = p[1]

    # Parse an assignment statement
    def p_assignment(self, p):
        "assignment : TT_identifier TT_equ expression"
        p[0] = Assignment(Variable(p[1]), p[3])

    # Parse an if-elif-else statement
    def p_if_statement(self, p):
        """if_statement : TT_if expression TT_colon statement_list elif_clauses else_clause"""
        p[0] = IfStatement(p[2], p[4], p[5], p[6])

    # Parse elif clauses
    def p_elif_clauses(self, p):
        """elif_clauses : elif_clauses TT_elif expression TT_colon statement_list
                        | empty"""
        if len(p) == 6:
            p[0] = p[1] + [(p[3], p[5])]
        else:
            p[0] = []

    # Parse the else clause
    def p_else_clause(self, p):
        """else_clause : TT_else TT_colon statement_list
                       | empty"""
        if len(p) == 4:
            p[0] = p[3]
        else:
            p[0] = None

    # Parse a while loop
    def p_while_loop(self, p):
        "while_loop : TT_while expression TT_colon statement_list"
        p[0] = WhileLoop(p[2], p[4])

    # Parse a for loop
    def p_for_loop(self, p):
        "for_loop : TT_for TT_identifier TT_in expression TT_colon statement_list"
        p[0] = ForLoop(Variable(p[2]), p[4], p[6])

    # Parse an expression
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
                      | TT_float
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

    # Parse an array
    def p_array(self, p):
        "array : TT_lbracket elements TT_rbracket"
        p[0] = Array(p[2])

    # Parse an array access
    def p_array_access(self, p):
        "array_access : TT_identifier TT_lbracket expression TT_rbracket"
        p[0] = ArrayAccess(array=Variable(p[1]), index=p[3])

    # Parse elements of an array
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

    # Parse a print statement
    def p_print_statement(self, p):
        "print_statement : TT_print TT_lparen expression TT_rparen"
        p[0] = PrintStatement(p[3])

    # Parse an empty production
    def p_empty(self, p):
        "empty :"
        p[0] = None

    def p_error(self, p):
        """Handle syntax errors in the input."""
        if p:  # If the parser knows where the error occurred
            error_message = f"Syntax error at token '{p.value}' (type: {p.type}) on line {p.lineno}."
        else:  # If the parser is lost and doesn't know where the error occurred
            error_message = "Syntax error at EOF (end of file)."
        raise SyntaxError(error_message)

    # Parse the input code
    def parse(self, data):
        return self.parser.parse(data, lexer=self.lexer.lexer)

# --- IR Generator ---
class IRGenerator:
    def __init__(self):
        self.instructions = []  # List of IR instructions
        self.temp_counter = 0  # Counter for temporary variables

    def new_temp(self):
        """Generate a new temporary variable."""
        temp = f"t{self.temp_counter}"
        self.temp_counter += 1
        return temp

    def generate(self, node):
        """Generate IR for a given AST node."""
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
            operator = self._map_operator(node.operator)
            self.instructions.append(f"{operator} {left}, {right}, {temp}")
            return temp
        elif isinstance(node, Literal):
            temp = self.new_temp()
            # Generate IR for a literal value
            if isinstance(node.value, str):  # String literals
                self.instructions.append(f"LOAD \"{node.value}\", {temp}")
            else:  # Numeric literals
                self.instructions.append(f"LOAD {node.value}, {temp}")
            return temp
        elif isinstance(node, Variable):
            # Generate IR for loading a variable's value
            return node.name  # Directly use the variable name in IR
        else:
            raise Exception(f"Unsupported AST node: {type(node)}")

    def _map_operator(self, operator):
        """Map operator symbols to IR instruction names."""
        operator_map = {
            "+": "ADD",
            "-": "SUB",
            "*": "MUL",
            "/": "DIV",
        }
        if operator not in operator_map:
            raise Exception(f"Unsupported operator: {operator}")
        return operator_map[operator]

    def get_ir(self):
        """Return the generated IR as a string."""
        return "\n".join(self.instructions)

# --- IR Executor ---
class IRExecutor:
    def __init__(self):
        self.variables = {}  # Named variable storage
        self.temp_table = {}  # Temporary variable storage

    def execute(self, instructions):
        """Execute the generated IR instructions."""
        output = []  # Store execution results
        for idx, instr in enumerate(instructions):
            parts = instr.split()
            op = parts[0]

            try:
                if op == "LOAD":
                    # Load a literal or variable value into a temporary variable
                    value = parts[1].strip(",")
                    temp = parts[2]
                    if value.isdigit():  # Integer literal
                        self.temp_table[temp] = int(value)
                    elif value.startswith("\"") and value.endswith("\""):  # String literal
                        self.temp_table[temp] = value.strip("\"")
                    elif value in self.variables:  # Named variable
                        self.temp_table[temp] = self.variables[value]
                    else:
                        raise Exception(f"LOAD: Undefined variable or value: {value}")
                elif op == "STORE":
                    # Store the value of a temporary variable into a named variable
                    temp = parts[1].strip(",")
                    var_name = parts[2]
                    if temp in self.temp_table:
                        self.variables[var_name] = self.temp_table[temp]
                    else:
                        raise Exception(f"STORE: Undefined temporary variable: {temp}")
                elif op == "PRINT":
                    # Print the value of a variable or temporary variable
                    key = parts[1]
                    value = self._resolve_value(key)
                    output.append(str(value))
                elif op in {"ADD", "SUB", "MUL", "DIV"}:
                    # Perform arithmetic operations
                    left = self._resolve_value(parts[1].strip(","))
                    right = self._resolve_value(parts[2].strip(","))
                    result = self._perform_operation(op, left, right)
                    self.temp_table[parts[3]] = result
                else:
                    raise Exception(f"Unsupported operation: {op}")
            except Exception as e:
                raise Exception(f"Error at instruction {idx}: {instr}\n{e}")

        return "\n".join(output)

    def _resolve_value(self, key):
        """Resolve the value of a variable or temporary variable."""
        if key in self.temp_table:
            return self.temp_table[key]
        elif key in self.variables:
            return self.variables[key]
        else:
            raise Exception(f"Undefined variable or temp: {key}")

    def _perform_operation(self, op, left, right):
        """Perform arithmetic operations."""
        if op == "ADD":
            return left + right
        elif op == "SUB":
            return left - right
        elif op == "MUL":
            return left * right
        elif op == "DIV":
            if right == 0:
                raise Exception("Division by zero")
            return left // right

# --- GUI IDE ---
class IDE:
    def __init__(self):
        self.root = tk.Tk()  # Create the main window
        self.root.title("Custom IDE")  # Set window title
        self.setup_widgets()  # Initialize widgets

    # Setup the widgets in the IDE
    def setup_widgets(self):
        # Editor for writing code
        self.editor = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=80, height=20)
        self.editor.pack(fill=tk.BOTH, expand=True)

        # Output console for displaying results
        self.output_console = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=80, height=10, state='disabled', bg='black', fg='white')
        self.output_console.pack(fill=tk.BOTH, expand=True)

        # Button to run the code
        self.run_button = tk.Button(self.root, text="Run", command=self.run_code)
        self.run_button.pack()

    # Append text to the output console
    def append_output(self, text):
        self.output_console.configure(state='normal')
        self.output_console.insert(tk.END, text)
        self.output_console.configure(state='disabled')
        self.output_console.see(tk.END)

    # Run the code from the editor
    def run_code(self):
        # Clear output console
        self.output_console.configure(state='normal')
        self.output_console.delete(1.0, tk.END)
        self.output_console.configure(state='disabled')

        # Retrieve code from the editor
        code = self.editor.get(1.0, tk.END)

        # Parse the code and generate IR
        parser = Parser()
        try:
            ast = parser.parse(code)  # Generate AST
            ir_gen = IRGenerator()  # Create IR generator
            ir_gen.generate(ast)  # Generate IR from AST
            ir = ir_gen.get_ir()  # Get IR as a string
            self.append_output(f"IR:\n{ir}\n")  # Display IR in the console

            # Execute the IR and display the output
            executor = IRExecutor()
            execution_output = executor.execute(ir_gen.instructions)
            self.append_output(f"Execution Output:\n{execution_output}\n")
        except Exception as e:
            self.append_output(f"Error: {str(e)}\n")  # Display errors

    # Start the main event loop
    def run(self):
        self.root.mainloop()

# --- Run the IDE ---
if __name__ == "__main__":
    IDE().run()  # Launch the IDE
