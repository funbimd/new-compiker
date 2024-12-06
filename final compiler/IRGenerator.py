from parser import (Program, Assignment, PrintStatement, BinaryOp, Literal, 
    Variable, Array, ArrayAccess, ForLoop, WhileLoop, IfStatement) 

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
        # Handle primitive types directly
        if isinstance(node, (int, float, str)):
            node = Literal(node)

        if isinstance(node, Program):
            for statement in node.statements:
                self.generate(statement)
        elif isinstance(node, Assignment):
            # If the value is a literal, directly generate its IR
            if isinstance(node.value, Literal):
                temp = self.generate(node.value)
                self.instructions.append(f"STORE {temp} {node.variable.name}")
            else:
                temp = self.generate(node.value)
                self.instructions.append(f"STORE {temp} {node.variable.name}")
        elif isinstance(node, PrintStatement):
            # If the expression is a variable, load its value first
            if isinstance(node.expression, Variable):
                temp = self.generate(node.expression)
                self.instructions.append(f"PRINT {temp}")
            else:
                temp = self.generate(node.expression)
                self.instructions.append(f"PRINT {temp}")
        elif isinstance(node, BinaryOp):
            left = self.generate(node.left)
            right = self.generate(node.right)
            temp = self.new_temp()
            operator = self._map_operator(node.operator)
            self.instructions.append(f"{operator} {left} {right} {temp}")
            return temp
        elif isinstance(node, Literal):
            temp = self.new_temp()
            # Generate IR for a literal value
            if isinstance(node.value, str):  # String literals
                self.instructions.append(f"LOAD \"{node.value}\" {temp}")
            elif isinstance(node.value, float):
                self.instructions.append(f"LOAD {node.value:.6f} {temp}")
            else:  # Numeric literals
                self.instructions.append(f"LOAD {node.value} {temp}")
            return temp
        elif isinstance(node, Variable):
            # Generate IR for loading a variable's value
            temp = self.new_temp()
            self.instructions.append(f"LOAD {node.name} {temp}")
            return temp
        elif isinstance(node, Array):
            # Create a temporary array
            temp = self.new_temp()
            # Generate IR for each element in the array
            element_temps = [self.generate(element) for element in node.elements]
            
            # Add instructions to create the array
            self.instructions.append(f"ARRAY {temp} {len(element_temps)}")
            
            # Add instructions to populate the array
            for i, element_temp in enumerate(element_temps):
                self.instructions.append(f"STORE_ARRAY {temp} {i} {element_temp}")
            return temp
        elif isinstance(node, ForLoop):
            iterable_temp = self.generate(node.iterable)

            lenght_temp = self.new_temp()
            self.instructions.append(f"ARRAY_LENGTH {iterable_temp} {lenght_temp}")

            counter_temp = self.new_temp()
            self.instructions.append(f"LOAD 0 {counter_temp}")

            loop_start_label = self.new_temp()
            loop_end_label = self.new_temp()

            self.instructions.append(f"LABEL {loop_start_label}")
            comparison_temp = self.new_temp()
            self.instructions.append(f"LT {counter_temp} {lenght_temp} {comparison_temp}")

            self.instructions.append(f"JUMPF {comparison_temp} {loop_end_label}")

            element_temp = self.new_temp()
            self.instructions.append(f"LOAD_ARRAY {iterable_temp} {counter_temp} {element_temp}")

            self.instructions.append(f"STORE {element_temp} {node.variable.name}")

            for statement in node.body:
                self.generate(statement)

            increment_temp = self.new_temp()
            self.instructions.append(f"ADD {counter_temp} 1 {increment_temp}")
            self.instructions.append(f"STORE {increment_temp} {counter_temp}")

            self.instructions.append(f"ADD {counter_temp} 1 {increment_temp}")
            self.instructions.append(f"STORE {increment_temp} {counter_temp}")

            self.instructions.append(f"JUMP {loop_start_label}")

            self.instructions.append(f"LABEL {loop_end_label}")
        elif isinstance(node, ArrayAccess):
            # Generate IR to access an array element
            array_temp = self.generate(node.array)
            index_temp = self.generate(node.index)
            temp = self.new_temp()
            self.instructions.append(f"LOAD_ARRAY {array_temp} {index_temp} {temp}")
            return temp
        else:
            raise Exception(f"Unsupported AST node: {type(node)}")

    def _map_operator(self, operator):
        """Map operator symbols to IR instruction names."""
        operator_map = {
            "+": "ADD",
            "-": "SUB",
            "*": "MUL",
            "/": "DIV",
            "**": "POW",
        }
        if operator not in operator_map:
            raise Exception(f"Unsupported operator: {operator}")
        return operator_map[operator]

    def get_ir(self):
        """Return the generated IR as a string."""
        return "\n".join(self.instructions)


