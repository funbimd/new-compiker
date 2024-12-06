# --- IR Executor ---
class IRExecutor:
    def __init__(self):
        self.variables = {}  # Named variable storage
        self.temp_table = {}  # Temporary variable storage
        self.arrays = {}

    def execute(self, instructions):
        """Execute the generated IR instructions."""
        output = []  # Store execution results
        for idx, instr in enumerate(instructions):
            print(f"Processing instruction: {instr}")  # Debugging
            parts = self._split_instruction(instr)
            print(f"Parts: {parts}")  # Debugging
            op = parts[0]

            try:
                if op == "LOAD":
                    # Load a literal or variable value into a temporary variable
                    value = parts[1]
                    temp = parts[2]
                    if value.startswith("\"") and value.endswith("\""):  # Quoted string literal
                        self.temp_table[temp] = value[1:-1]  # Strip quotes
                    elif "." in value:
                        self.temp_table[temp] = float(value)
                    elif value.isdigit():  # Integer literal
                        self.temp_table[temp] = int(value)
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
                elif op == "ARRAY":
                    temp = parts[1]
                    length = int(parts[2])
                    self.arrays[temp] = [None] * length
                elif op == "STORE_ARRAY":
                    array_temp = parts[1]
                    index = int(parts[2])
                    value_temp = parts[3]

                    if array_temp not in self.arrays:
                        raise Exception(f"Undefined array: {array_temp}")

                    value = self._resolve_value(value_temp)
                    self.arrays[array_temp][index] = value
                elif op == "LOAD_ARRAY":
                    array_temp = parts[1]
                    index_temp = parts[2]
                    result_temp = parts[3]

                    if array_temp not in self.arrays:
                        raise Exception(f'Undefined array: {array_temp}')

                    index = self._resolve_value(index_temp)
                    value = self.arrays[array_temp][index]
                    self.temp_table[result_temp] = value
                elif op == "ARRAY_LENGTH":
                    array_temp = parts[1]
                    result_temp = parts[2]

                    if array_temp not in self.arrays:
                        raise Exception(f"Undefined array: {array_temp}")

                    self.temp_table[result_temp] = len(self.arrays[array_temp])
                else:
                    raise Exception(f"Unsupported operation: {op}")
            except Exception as e:
                raise Exception(f"Error at instruction {idx}: {instr}\n{e}")

        return "\n".join(output)

    def _split_instruction(self, instr):
        """Custom splitting logic to preserve quoted strings."""
        import re
        return re.findall(r'\".*?\"|\S+', instr)

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
            return left / right
        elif op == "POW":
            return left ** right