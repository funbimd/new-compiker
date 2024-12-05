class Interpreter:
    """
    An interpreter to execute a list of abstract syntax trees (ASTs).
    """
    def __init__(self, asts):
        """
        Initializes the interpreter with a list of ASTs and a storage for variables.
        
        Parameters:
        - asts: A list of abstract syntax tree (AST) nodes representing the program to execute.
        """
        self.asts = asts  # Store the list of ASTs to execute.
        self.storage = {}  # Dictionary for variable storage, acting as the program's memory.

    def execute(self):
        """
        Executes each AST node in the list by invoking its `read` method.
        
        The `read` method of each node handles the logic for evaluating and executing
        the specific operation represented by the node.
        """
        for ast in self.asts:  # Iterate through each AST node.
            ast.read(self)  # Execute the node by passing the interpreter context (`self`).
