import ply.yacc as yacc  # Importing PLY for syntax analysis
from lexer import Lexer, tokens

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

# --- Parser Definition ---
# Syntax parser using PLY
class Parser:
    # Define the tokens from lexer
    tokens = tokens

    # Operator precedence for arithmetic and comparisons
    precedence = (
        ('left', 'TT_plus', 'TT_sub'),
        ('left', 'TT_mul', 'TT_div'),
        ('right', 'TT_pow'),
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
        """assignment : TT_identifier TT_equ expression
                      | TT_identifier TT_equ TT_float
                      | TT_identifier TT_equ TT_int"""
        if len(p) == 4:
            p[0] = Assignment(Variable(p[1]), p[3])
        else:
            # Direct literal assignment
            p[0] = Assignment(Variable(p[1]), Literal(p[3]))

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
                      | expression TT_pow expression
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
            if isinstance(p[1], (int, float, str)):
                p[0] = Literal(p[1])
            elif isinstance(p[1], str):
                p[0]= Variable(p[1])
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
        """print_statement : TT_print TT_lparen expression TT_rparen
                           | TT_print TT_lparen TT_string TT_rparen
                           | TT_print TT_lparen TT_float TT_rparen
                           | TT_print TT_lparen TT_int TT_rparen
                           | TT_print TT_lparen TT_identifier TT_rparen"""
        if len(p) == 5:
            # Handle different types of print statements
            if isinstance(p[3], (str, int, float)):
                p[0] = PrintStatement(Literal(p[3]))
            elif isinstance(p[3], str):
                p[0]=PrintStatement(Variable(p[3]))
            else:
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

# Export AST node classes for external use
__all__ = [
    "ASTNode", "Program", "IfStatement", "WhileLoop", "ForLoop",
    "Assignment", "PrintStatement", "BinaryOp", "Literal",
    "Variable", "Array", "ArrayAccess",
]