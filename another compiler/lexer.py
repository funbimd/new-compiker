import sys

class Token:
    """
    Represents a lexical token with type, value, and positional information.
    """
    def __init__(self, type_, value=None, start=None, end=None):
        # Initialize the token with its type, optional value, and positional details.
        self.type = type_
        self.value = value
        self.start = start
        self.end = end

    def __repr__(self):
        # Provide a string representation of the token for debugging.
        return f'{self.type}:"{self.value}"' if self.value else f'{self.type}'

    def read(self, context):
        """
        Interprets the token value. For numbers, returns float; for others, resolves identifiers.
        """
        if self.type == "TT_NUMBER":
            # Convert numeric token values to float.
            return float(self.value)
        return self.value  # Return the value as is for other token types.


class IdentToken(Token):
    """
    Specialized token class for identifiers.
    """
    def read(self, context):
        """
        Resolves the identifier's value from a provided context storage.
        """
        try:
            # Attempt to retrieve the value of the identifier from the context.
            return context.storage[self.value]
        except KeyError:
            # If the identifier does not exist, terminate with an error.
            sys.exit(f"'{self.value}' does not exist in the current context.")


class Lexer:
    """
    Responsible for tokenizing source code into a list of tokens.
    """
    # Define a set of reserved keywords in the language.
    KEYWORDS = {"print"}

    def __init__(self, source):
        # Initialize the lexer with the source code.
        self.source = source
        self.curChar = ''  # Current character being processed.
        self.curPos = -1  # Current position in the source.
        self.tokenList = []  # List to store tokens.
        self.error = None  # Placeholder for potential errors.
        self.nextChar()  # Load the first character.

    def nextChar(self):
        """
        Advances to the next character in the source code.
        """
        self.curPos += 1  # Move to the next position.
        # Update the current character, or set to null character if at the end.
        self.curChar = self.source[self.curPos] if self.curPos < len(self.source) else '\0'

    def peek(self):
        """
        Returns the next character without consuming it.
        """
        # Look ahead one character in the source, or null character if out of bounds.
        return self.source[self.curPos + 1] if self.curPos + 1 < len(self.source) else '\0'

    def abort(self, message):
        """
        Terminates execution with an error message.
        """
        sys.exit(f"Lexing error: {message}")  # Exit with the provided error message.

    def skipWhitespace(self):
        """
        Skips whitespace characters.
        """
        while self.curChar in {' ', '\r'}:  # Ignore spaces and carriage returns.
            self.nextChar()  # Advance to the next character.

    def skipComment(self):
        """
        Skips comments starting with '#'.
        """
        if self.curChar == '#':  # Check if the current character starts a comment.
            while self.curChar != '\n' and self.curChar != '\0':
                # Skip characters until a newline or end of file is reached.
                self.nextChar()

    def addToken(self, type_, value=None, start=None, end=None):
        """
        Adds a token to the token list.
        """
        # Create and append a new token to the token list.
        self.tokenList.append(Token(type_, value, start, end))

    def getTokens(self):
        """
        Tokenizes the source code into a list of tokens.
        """
        while self.curChar != '\0':  # Process until the end of the source is reached.
            self.skipWhitespace()  # Skip over any whitespace.
            self.skipComment()  # Skip over any comments.
            token_start = self.curPos  # Record the starting position of the current token.

            # Handle various token types based on the current character.
            if self.curChar == '+':
                self.addToken("TT_PLUS", self.curChar, token_start)
            elif self.curChar == '-':
                self.addToken("TT_MINUS", self.curChar, token_start)
            elif self.curChar == '*':
                if self.peek() == '*':  # Check for '**' (exponentiation operator).
                    self.nextChar()
                    self.addToken("TT_POW", '**', token_start, self.curPos)
                else:
                    self.addToken("TT_MULT", self.curChar, token_start)
            elif self.curChar == '/':
                self.addToken("TT_DIV", self.curChar, token_start)
            elif self.curChar == '=':
                if self.peek() == '=':  # Check for '==' (equality operator).
                    self.nextChar()
                    self.addToken("TT_EQEQ", '==', token_start, self.curPos)
                else:
                    self.addToken("TT_EQ", self.curChar, token_start)
            elif self.curChar in {'>', '<'}:
                # Handle '>', '<', '>=', and '<=' operators.
                operator = self.curChar
                if self.peek() == '=':
                    self.nextChar()
                    operator += '='
                    token_type = "TT_GTEQ" if self.curChar == '>' else "TT_LTEQ"
                else:
                    token_type = "TT_GT" if self.curChar == '>' else "TT_LT"
                self.addToken(token_type, operator, token_start, self.curPos)
            elif self.curChar == '!':
                # Handle '!=' operator.
                if self.peek() == '=':
                    self.nextChar()
                    self.addToken("TT_NTEQ", '!=', token_start, self.curPos)
                else:
                    self.abort("Expected '!=', found '!'")
            elif self.curChar in {'"', "'"}:
                # Tokenize string literals.
                self.tokenizeString(self.curChar)
            elif self.curChar.isdigit():
                # Tokenize numeric literals.
                self.tokenizeNumber()
            elif self.curChar.isalpha():
                # Tokenize identifiers or keywords.
                self.tokenizeIdentifierOrKeyword()
            elif self.curChar in {'(', ')', '[', ']', ':', ','}:
                # Tokenize single-character symbols.
                token_map = {'(': "TT_LPAREN", ')': "TT_RPAREN", 
                             '[': "TT_LSQPAREN", ']': "TT_RSQPAREN", 
                             ':': "TT_COLON", ',': "TT_COMMA"}
                self.addToken(token_map[self.curChar], self.curChar, token_start)
            elif self.curChar == '\n':
                # Handle newline characters.
                self.addToken("TT_NWL", '', token_start)
            elif self.curChar == '\t':
                # Handle tab characters.
                self.addToken("TT_TAB", '', token_start)
            else:
                # Handle unknown tokens.
                self.abort(f"Unknown token: {self.curChar}")

            self.nextChar()  # Move to the next character.

        # Add the end-of-file token.
        self.addToken("TT_EOF")
        return self.tokenList

    def tokenizeString(self, quote):
        """
        Tokenizes a string literal enclosed in single or double quotes.
        """
        self.nextChar()  # Skip the opening quote.
        start_pos = self.curPos  # Record the starting position of the string.

        while self.curChar != quote:
            if self.curChar in {'\r', '\n', '\t', '\\', '%'} or self.curChar == '\0':
                # Abort if an illegal character is found inside the string.
                self.abort("Illegal character in string.")
            self.nextChar()  # Advance to the next character.

        # Add the string token.
        self.addToken("TT_STRING", self.source[start_pos:self.curPos], start_pos, self.curPos)

    def tokenizeNumber(self):
        """
        Tokenizes a numeric literal, including integers and floats.
        """
        start_pos = self.curPos  # Record the starting position of the number.
        while self.peek().isdigit():
            # Consume all subsequent digits.
            self.nextChar()

        if self.peek() == '.':  # Check for a decimal point.
            self.nextChar()
            if not self.peek().isdigit():
                # Abort if the decimal is not followed by digits.
                self.abort("Illegal character in number.")
            while self.peek().isdigit():
                # Consume all digits after the decimal point.
                self.nextChar()

        # Add the numeric token.
        self.addToken("TT_NUMBER", self.source[start_pos:self.curPos + 1], start_pos, self.curPos)

    def tokenizeIdentifierOrKeyword(self):
        """
        Tokenizes identifiers or keywords.
        """
        start_pos = self.curPos  # Record the starting position of the identifier.
        while self.peek().isalnum():
            # Consume all alphanumeric characters.
            self.nextChar()

        tok_text = self.source[start_pos:self.curPos + 1]  # Extract the token text.
        # Determine if it's a keyword or an identifier.
        token_type = "TT_KEYW" if tok_text in self.KEYWORDS else "TT_IDENT"
        self.addToken(token_type, tok_text, start_pos, self.curPos)
