import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
import subprocess
import re
import keyword
from ctypes import windll
from lexer import Lexer
from parser import Parser
from IRGenerator import IRGenerator

# Improve DPI awareness on Windows (if supported)
try:
    windll.shcore.SetProcessDpiAwareness(2)  # Enable DPI scaling for sharp visuals on high-resolution displays.
except:
    pass  # If unsupported, fail gracefully.

class CodeEditorApp:
    """
    A simple Python code editor with syntax highlighting, line numbers, 
    and the ability to execute Python code.
    """
    def __init__(self, root):
        self.root = root  # Main application window.
        self.root.title("Group 3 IDE")  # Set window title.
        self.root.state('zoomed')  # Maximize the window by default.

        self.current_file_path = ""  # Track the currently opened file.
        self.process = None  # Variable for managing the subprocess running Python code.

        # Configure the main layout of the editor.
        self.frame = tk.Frame(root)
        self.frame.pack(expand=True, fill='both')  # Expand to fill the entire window.

        self.frame.grid_rowconfigure(0, weight=1)  # Text editor area.
        self.frame.grid_rowconfigure(1, weight=1)  # Output area.
        self.frame.grid_columnconfigure(1, weight=1)  # Enable resizing of the editor areas.

        self.create_widgets()  # Create the editor and output widgets.
        self.create_menu()  # Create the menu bar for file and run options.
        self.apply_theme()  # Apply a dark theme to the UI.
        self.on_key_release()  # Initialize syntax highlighting and line numbers.

    def create_widgets(self):
        """
        Creates the line number display, text editor, and output area.
        """
        # Line numbers widget.
        self.line_numbers = self.create_text_widget(
            width=4,  # Fixed width for line numbers.
            padx=3,  # Padding for better readability.
            takefocus=0,  # Prevent focus on the line number widget.
            border=0,  # Remove border.
            background="#1e1e2f",  # Background color (dark gray).
            foreground="#6a6a8c",  # Foreground color (light gray).
            state='disabled',  # Make the widget read-only.
            wrap='none'  # Disable text wrapping.
        )
        self.line_numbers.grid(row=0, column=0, rowspan=2, sticky='ns')  # Span both rows vertically.

        # Main text editor widget.
        self.text_widget = scrolledtext.ScrolledText(
            self.frame,
            wrap=tk.WORD,  # Wrap long lines at word boundaries.
            font=("Consolas", 11),  # Monospace font for code.
            background="#282c34",  # Background color (dark gray).
            foreground="#abb2bf",  # Text color (light gray).
            insertbackground="#abb2bf"  # Caret color.
        )
        self.text_widget.grid(row=0, column=1, sticky="nsew")  # Fill the first row.
        self.text_widget.bind("<KeyRelease>", self.on_key_release)  # Trigger updates on key release.

        # Output area widget.
        self.output_text = scrolledtext.ScrolledText(
            self.frame,
            wrap=tk.WORD,
            font=("Consolas", 11),
            background="#21252b",  # Background color (slightly darker gray).
            foreground="#98c379"  # Text color (green).
        )
        self.output_text.grid(row=1, column=1, sticky="nsew")  # Fill the second row.
        self.output_text.tag_configure("error", foreground="#e06c75")  # Configure error messages (red).

    def create_menu(self):
        """
        Creates the menu bar with File and Run options.
        """
        menu_bar = tk.Menu(self.root)  # Create the top-level menu bar.

        # File menu.
        file_menu = tk.Menu(menu_bar, tearoff=False)
        file_menu.add_command(label="Open", command=self.open_file)  # Option to open files.
        file_menu.add_command(label="Save", command=self.save_file)  # Option to save files.
        file_menu.add_separator()  # Separator for better visual grouping.
        file_menu.add_command(label="Exit", command=self.exit_app)  # Exit the application.
        menu_bar.add_cascade(label="File", menu=file_menu)  # Add the File menu to the menu bar.

        # Run menu.
        run_menu = tk.Menu(menu_bar, tearoff=False)
        run_menu.add_command(label="Run", command=self.run_code)  # Option to execute the code.
        menu_bar.add_cascade(label="Run", menu=run_menu)  # Add the Run menu to the menu bar.

        self.root.config(menu=menu_bar)  # Set the menu bar as the window's menu.

    def create_text_widget(self, **kwargs):
        """
        Helper method to create text widgets with the provided properties.
        """
        return tk.Text(self.frame, **kwargs)

    def apply_theme(self):
        """
        Applies a dark theme to the text editor and output area.
        """
        self.text_widget.configure(
            background="#282c34",  # Dark background for the editor.
            foreground="#abb2bf",  # Light gray text.
            insertbackground="#abb2bf"  # Caret color.
        )
        self.output_text.configure(
            background="#21252b",  # Darker background for the output.
            foreground="#98c379"  # Green text for output.
        )
        self.line_numbers.configure(
            background="#1e1e2f",  # Dark gray background for line numbers.
            foreground="#6a6a8c"  # Light gray text for line numbers.
        )

    def open_file(self):
        """
        Opens a file and loads its content into the text editor.
        """
        file_path = filedialog.askopenfilename(filetypes=[("Python Files", "*.py"), ("All Files", "*.*")])
        if file_path:  # If a file is selected.
            with open(file_path, 'r') as file:
                self.text_widget.delete('1.0', tk.END)  # Clear the editor.
                self.text_widget.insert('1.0', file.read())  # Load the file's content.
            self.current_file_path = file_path  # Update the current file path.
            self.update_line_numbers()  # Refresh line numbers.
            self.on_key_release()  # Reapply syntax highlighting.

    def save_file(self):
        """
        Saves the content of the text editor to the current file or a new file.
        """
        if not self.current_file_path:  # If no file is currently open, prompt to save as a new file.
            self.current_file_path = filedialog.asksaveasfilename(filetypes=[("Python Files", "*.py"), ("All Files", "*.*")])
        if self.current_file_path:  # If a file path is provided.
            with open(self.current_file_path, 'w') as file:
                file.write(self.text_widget.get('1.0', tk.END))  # Write the editor content to the file.
            messagebox.showinfo("Save", "File saved successfully!")  # Notify the user.

    def exit_app(self):
        """
        Exits the application.
        """
        self.root.destroy()  # Close the application window.

    def run_code(self):
        """
        Runs the Python code in the editor and displays the output or errors.
        """
        code = self.text_widget.get('1.0', tk.END).strip()  # Get the code from the editor.
        if not code:  # If the editor is empty, show a warning.
            messagebox.showwarning("Run", "Editor is empty. Please write some code.")
            return

        # Create lexer, parser, and IR generator instances
        lexer = Lexer()
        parser = Parser()
        ir_generator = IRGenerator()

        # Tokenize the input code
        lexer.lexer.input(code)
        print("Tokens:")
        tokens = []
        for token in lexer.lexer:
            print(token)
            tokens.append(token)

        # Parse the code and generate AST
        try:
            ast = parser.parse(code)
            print("\nAST:")
            print(ast)
        except SyntaxError as e:
            print(f"Syntax error: {e}")
            return

        # Generate IR from AST
        ir_generator.generate(ast)
        print("\nGenerated IR:")
        print(ir_generator.get_ir())
        try:
            # Execute the code using a subprocess and capture stdout and stderr.
            process = subprocess.Popen(
                ["python", "-c", code],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            stdout, stderr = process.communicate()

            # Display the output and errors in the output area.
            self.output_text.config(state=tk.NORMAL)
            self.output_text.delete('1.0', tk.END)  # Clear the output area.
            if stdout:
                self.output_text.insert(tk.END, stdout)  # Insert standard output.
            if stderr:
                self.output_text.insert(tk.END, stderr, "error")  # Insert errors in red.
            self.output_text.config(state=tk.DISABLED)
        except Exception as e:
            # Display unexpected errors in the output area.
            self.output_text.config(state=tk.NORMAL)
            self.output_text.delete('1.0', tk.END)
            self.output_text.insert(tk.END, f"Error: {str(e)}", "error")
            self.output_text.config(state=tk.DISABLED)

    def update_line_numbers(self, event=None):
        """
        Updates the line numbers based on the content in the editor.
        """
        self.line_numbers.config(state=tk.NORMAL)
        self.line_numbers.delete('1.0', tk.END)  # Clear existing line numbers.
        lines = self.text_widget.get('1.0', 'end-1c').split('\n')  # Get the current lines.
        for i, _ in enumerate(lines, start=1):  # Enumerate line numbers.
            self.line_numbers.insert(tk.END, f"{i}\n")  # Insert line numbers.
        self.line_numbers.config(state=tk.DISABLED)

    def highlight_comments(self):
        """
        Highlights comments in the code.
        """
        self.apply_highlight(r"#.*", "comment", "#7f848e", ("Consolas", 11, "italic"))

    def highlight_strings(self):
        """
        Highlights string literals in the code.
        """
        pattern = r"(['\"].*?['\"]|'''[\s\S]*?'''|\"\"\"[\s\S]*?\"\"\")"
        self.apply_highlight(pattern, "string", "#e5c07b", ("Consolas", 11, "italic"))

    def highlight_keywords(self):
        """
        Highlights Python keywords in the code.
        """
        for kw in keyword.kwlist:
            pattern = rf'\b{kw}\b'
            self.apply_highlight(pattern, "keyword", "#61afef", ("Consolas", 11, "bold"))

    def apply_highlight(self, pattern, tag_name, color, font):
        """
        Applies syntax highlighting based on a pattern and style.
        """
        self.text_widget.tag_remove(tag_name, "1.0", tk.END)  # Remove existing highlights for the tag.
        for match in re.finditer(pattern, self.text_widget.get("1.0", tk.END)):  # Find matches using regex.
            start = f"1.0+{match.start()}c"  # Calculate start position.
            end = f"1.0+{match.end()}c"  # Calculate end position.
            self.text_widget.tag_add(tag_name, start, end)  # Add the tag to the matched text.
        self.text_widget.tag_configure(tag_name, foreground=color, font=font)  # Configure tag style.

    def on_key_release(self, event=None):
        """
        Handles key release events to update syntax highlighting and line numbers.
        """
        self.highlight_comments()  # Highlight comments.
        self.highlight_strings()  # Highlight strings.
        self.highlight_keywords()  # Highlight keywords.
        self.update_line_numbers()  # Update line numbers.


if __name__ == "__main__":
    root = tk.Tk()  # Create the main application window.
    app = CodeEditorApp(root)  # Create an instance of the code editor.
    root.mainloop()  # Start the Tkinter event loop.
