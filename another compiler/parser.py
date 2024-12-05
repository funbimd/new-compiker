import sys

class Parser:
    """
    A class to parse a list of tokens into an abstract syntax tree (AST).
    """
    def __init__(self, tokens):
        # Initialize the parser with a list of tokens.
        self.tokens = tokens  # List of tokens to parse.
        self.currentPosition = -1  # Current position in the token list.
        self.currentToken = None  # The token currently being processed.
        self.advance()  # Move to the first token.

    def advance(self):
        """
        Advances to the next token in the token stream.
        """
        self.currentPosition += 1  # Increment the position.
        # Update the current token or set it to None if we've reached the end.
        self.currentToken = self.tokens[self.currentPosition] if self.currentPosition < len(self.tokens) else None

    def runParse(self):
        """
        Parses the entire token list into statements until the end of file (EOF).
        """
        statements = []  # List to store parsed statements.

        while self.currentToken.type != "TT_EOF":  # Parse until the end of file token.
            if self.currentToken.type == "TT_NWL":  # Skip newline tokens.
                self.advance()
                continue

            # Parse a statement and append it to the list of statements.
            statement = self.isStatement()
            if statement:
                statements.append(statement)
            else:
                # Exit if the statement is unsupported.
                sys.exit("Unsupported statement.")

            if self.currentToken.type != "TT_NWL":
                # Ensure statements end with a newline.
                sys.exit("Parsing Error: Expected newline.")

        return statements  # Return the parsed statements.

    def isStatement(self):
        """
        Identifies and parses supported statements (e.g., assignments, print statements).
        """
        if self.currentToken.type == "TT_IDENT":  # Check for an identifier (likely an assignment).
            return self.parseAssignment()
        elif self.currentToken.type == "TT_KEYW" and self.currentToken.value == "print":  # Check for a print statement.
            return self.parsePrintStatement()
        else:
            sys.exit("Invalid statement.")  # Exit if the statement is not valid.

    def parseAssignment(self):
        """
        Parses an assignment statement.
        """
        identifier = self.currentToken  # Save the identifier token.
        self.advance()

        if self.currentToken.type != "TT_EQ":  # Ensure the next token is '='.
            sys.exit("Parsing Error: Expected '=' in assignment.")
        
        self.advance()  # Move to the expression part of the assignment.
        expression = self.expression()  # Parse the expression.
        return Assign(identifier, expression)  # Return an Assign node.

    def parsePrintStatement(self):
        """
        Parses a print statement.
        """
        self.advance()  # Skip the 'print' keyword.

        if self.currentToken.type != "TT_LPAREN":  # Ensure the next token is '('.
            sys.exit("Parsing Error: Expected '(' in print statement.")

        self.advance()  # Move past '('.
        expression = self.expression()  # Parse the expression to print.

        if self.currentToken.type != "TT_RPAREN":  # Ensure the next token is ')'.
            sys.exit("Parsing Error: Expected ')' in print statement.")
        
        self.advance()  # Move past ')'.
        return Print(expression)  # Return a Print node.

    def expression(self):
        """
        Parses an expression, handling addition and subtraction.
        """
        # Use binary operation parsing for expressions involving '+' or '-'.
        return self.parseBinaryOperation(self.term, ["TT_PLUS", "TT_MINUS"])

    def term(self):
        """
        Parses a term, handling multiplication and division.
        """
        # Use binary operation parsing for terms involving '*' or '/'.
        return self.parseBinaryOperation(self.exponent, ["TT_MULT", "TT_DIV"])

    def exponent(self):
        """
        Parses an exponentiation expression.
        """
        # Use binary operation parsing for '**' (exponentiation).
        return self.parseBinaryOperation(self.factor, ["TT_POW"])

    def factor(self):
        """
        Parses a factor (numbers, identifiers, parentheses).
        """
        token = self.currentToken  # Get the current token.

        if token.type == "TT_NUMBER":  # Handle numeric literals.
            self.advance()
            return Node(token)  # Return a Node containing the number.
        elif token.type == "TT_IDENT":  # Handle identifiers.
            self.advance()
            return Node(token)  # Return a Node containing the identifier.
        elif token.type == "TT_LPAREN":  # Handle expressions in parentheses.
            self.advance()
            expr = self.expression()  # Parse the expression inside the parentheses.
            if self.currentToken.type != "TT_RPAREN":  # Ensure there's a closing parenthesis.
                sys.exit("Parsing Error: Expected ')'.")
            self.advance()
            return expr  # Return the parsed expression.
        elif token.type == "TT_EOF":  # Handle the end of file token.
            return Node(token)
        else:
            sys.exit(f"Parsing Error: Unexpected token '{token.value}'.")  # Exit for unexpected tokens.

    def parseBinaryOperation(self, parseFunc, operators):
        """
        Parses binary operations using a given parsing function and operator list.
        """
        left = parseFunc()  # Parse the left operand.

        while self.currentToken.type in operators:  # Check if the current token is an operator.
            operator = self.currentToken  # Save the operator token.
            self.advance()
            right = parseFunc()  # Parse the right operand.
            left = BiNode(left, operator, right)  # Create a BiNode for the operation.

        return left  # Return the final expression tree.


class Node:
    """
    Represents a generic node in the abstract syntax tree (AST).
    """
    def __init__(self, token):
        self.token = token  # Store the associated token.

    def __repr__(self):
        # Represent the node using its token value.
        return str(self.token.value)

    def read(self, context):
        """
        Evaluates the node's value based on the token type and context.
        """
        return self.token.read(context)  # Use the token's read method.


class BiNode:
    """
    Represents a binary operation node in the AST.
    """
    def __init__(self, left_node, op_token, right_node):
        self.left_node = left_node  # Left operand.
        self.op_token = op_token  # Operator token.
        self.right_node = right_node  # Right operand.

    def __repr__(self):
        # Represent the binary operation as a string.
        return f'({self.left_node} {self.op_token.value} {self.right_node})'

    def read(self, context):
        """
        Evaluates the binary operation based on the operator.
        """
        left_value = self.left_node.read(context)  # Evaluate the left operand.
        right_value = self.right_node.read(context)  # Evaluate the right operand.

        # Perform the operation based on the operator type.
        if self.op_token.type == "TT_PLUS":
            return left_value + right_value
        elif self.op_token.type == "TT_MINUS":
            return left_value - right_value
        elif self.op_token.type == "TT_MULT":
            return left_value * right_value
        elif self.op_token.type == "TT_DIV":
            return left_value / right_value
        elif self.op_token.type == "TT_POW":
            return left_value ** right_value


class Assign:
    """
    Represents an assignment statement.
    """
    def __init__(self, identifier, value):
        self.variable = identifier.value  # Variable name.
        self.value = value  # Assigned value.

    def __repr__(self):
        # Represent the assignment as a string.
        return f"{self.variable} = {self.value}"

    def read(self, context):
        """
        Executes the assignment, storing the value in the context.
        """
        context.storage[self.variable] = self.value.read(context)  # Store the value in the context.


class Print:
    """
    Represents a print statement.
    """
    def __init__(self, value):
        self.value = value  # Expression to print.

    def __repr__(self):
        # Represent the print statement as a string.
        return f"print({self.value})"

    def read(self, context):
        """
        Executes the print statement, outputting the evaluated value.
        """
        print(self.value.read(context))  # Print the evaluated value.
