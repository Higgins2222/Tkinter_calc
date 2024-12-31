# tkinter_calc.py
# Author: Higgins
# Build 12

import tkinter as tk
import pyperclip
from math import sqrt

VALID_OPERATIONS = ['*', '/', '+', '-', '**']

def exponent(equation):
    temp = []

    while equation:
        token = equation.pop(0)

        if token == '**':
            left = temp.pop()
            right = equation.pop(0)
            result = left ** right
            temp.append(result)
        else:
            temp.append(token)

    return temp

def mult_div(equation):
    temp = []

    while equation:
        token = equation.pop(0)

        if token == '*':
            left = temp.pop()
            right = equation.pop(0)
            result = left * right
            temp.append(result)
        elif token == '/':
            left = temp.pop()
            right = equation.pop(0)
            result = left / right
            temp.append(result)
        else:
            temp.append(token)

    return temp


def add_sub(equation):
    temp = []

    while equation:
        token = equation.pop(0)

        if token == '+':
            left = temp.pop()
            right = equation.pop(0)
            result = left + right
            temp.append(result)
        elif token == '-':
            left = temp.pop()
            right = equation.pop(0)
            result = left - right
            temp.append(result)
        else:
            temp.append(token)

    return temp

def solver(equation):
    temp = []

    while equation:
        token = equation.pop(0)
        if token == '(':
            inside_equation = equation
            reduced_equation = solver(inside_equation)
            temp.extend(reduced_equation)
        elif token == ')':
            temp = exponent(temp)
            temp = mult_div(temp)
            temp = add_sub(temp)
            return temp
        else:
            temp.append(token)

    temp = exponent(temp)
    temp = mult_div(temp)
    temp = add_sub(temp)

    return temp[0]

def is_number(s):
    # This implementation is fine, but could be a regex as further requirements demand.  Likely undefined behavoir with NaN and infinity
    try:
        float(s)
        return True
    except ValueError:
        return False
    except TypeError:
        return False
    except Exception:
        raise

def validate_equation(equation: list):
    print('validating', equation)
    if not equation:
        return False

    open_paren = 0 # Nested level of parenthesis
    need_num = True # Weither we need the next term to be a number
    is_valid = True # False while our equation is invalid

    for term in equation:
        print(term)

        if need_num:
            if term == '(':
                open_paren += 1
            elif is_number(term):
                need_num = False
            else:
                is_valid = False
                break
        else:
            if term == ')':
                open_paren -= 1
                # Check if we have a ')' but no matching '(' preceding it
                if open_paren < 0:
                    is_valid = False
                    break
                need_num = False
            elif term in VALID_OPERATIONS:
                need_num = True
            else:
                is_valid = False
                break
    # Equation likely ends with an operation, invalid
    if need_num:
        is_valid = False

    # Valid only when there are matching pairs of parenthesis
    if open_paren != 0:
        is_valid = False

    print(f'{is_valid=}')

    return is_valid

class InvalidEquationException(Exception):
    def __init__(self, equation, message="Invalid equation format or structure"):
        self.equation = equation
        self.message = message
        super().__init__(f"{message}: {equation}")

class ParenthesisBeforeOperationException(Exception):
    def __init__(self, equation, message="Invalid equation format or structure"):
        self.equation = equation
        self.message = message
        super().__init__(f"{message}: {equation}")

class UnknownOperationException(Exception):
    def __init__(self, operation, message="Unknown operation"):
        self.operation = operation
        self.message = message
        super().__init__(f"{message}: {operation}")

class Equation:
    def __init__(self):
        self.equation = []
        self.solution = ''

    # def append_opp(self, operation):
    #     self.equation.append(operation)

    def append_term(self, num):
        # note: this will commonly be called as '=' is pressed
        # todo: if num.isdigit():
        # todo: if equation[-1] in list_of_opps
        if is_number(num):
            self.equation.append(str(num))
        else:
            raise TypeError # or ValueError?

    def append_opp(self, operation):
        if self.equation:
            if is_number(self.equation[-1]):
                if operation in VALID_OPERATIONS:
                    self.equation.append(operation)
                elif operation == ')':
                    self.equation.append(operation)
                elif operation == '(':
                    raise ParenthesisBeforeOperationException(self.equation)
                elif operation in VALID_OPERATIONS:
                    self.equation.append(operation)
                else:
                    raise UnknownOperationException(operation)
            elif self.equation[-1] in VALID_OPERATIONS:
                if operation == '(':
                    self.equation.append(operation)
                else:
                    self.equation.pop()
                    self.equation.append(operation)
            elif self.equation[-1] == '(':
                if operation == '(':
                    self.equation.append(operation)
                else:
                    self.equation.pop()
                    self.equation.append(operation)
            elif self.equation[-1] == ')':
                self.equation.append(operation)
            else:
                raise UnknownOperationException(operation)
        elif operation == '(':
            self.equation.append(operation)

    def clear(self):
        self.equation = []

    def get_solution(self):
        print(self.equation)
        eq = self.equation
        if self.equation:
            if self.equation[-1] in VALID_OPERATIONS:
                eq = self.equation[0:len(self.equation) - 1]
        else:
            return '0'
        if not validate_equation(eq):
            raise InvalidEquationException(eq)

        equation_int = [float(x) if is_number(x) else x for x in eq]
        print(f'GET SOLUTION {equation_int=}')
        self.solution = str(solver(equation_int))
        return self.solution

    def set_equation_from_list(self, li):
        if not validate_equation(self.equation):
            raise InvalidEquationException(self.equation)

        self.equation = li


class CalculatorApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Simple Calculator")

        # Current number being input, or the result of the last equation
        self.current_number = []

        # Set to true after a solution has been solved ('=' pressed)
        # Used to differentiate between a number in the display as part of an equation or the answer to the last equation.
        self.is_new = True

        # The current equation being typed
        self.equation = Equation()

        # History of all solved equations
        self.equation_history = []
        self.label_to_equation = {}  # Maps labels to equation objects

        # Applocal Clipboard
        self.clipboard = None

        # Memory
        self.memory = '0'
        self.display_memory = False

        # Track history panel visibility
        self.history_frame_visible = False
        self.memory_frame_visible = False

        # Create Frames for layout management
        self.display = tk.Frame(self.root)
        self.extra_functions = tk.Frame(self.root)
        self.basic_operations = tk.Frame(self.root)
        self.basic_functions = tk.Frame(self.root)
        self.history_frame = tk.Frame(self.root, width=300, relief="solid", bg="#AAAAAA")

        # Bind keyboard keys
        self.bind_keys()

        # GUI Buttons
        self.init_UI()
        # Option to defer startup, to speed up initial window render
        # root.after(100, self.init_UI())

        # Create a menu bar
        menu_bar = tk.Menu(self.root)

        # Create a "Show" menu
        self.show_menu = tk.Menu(menu_bar, tearoff=0)  # tearoff=0 removes the dotted line at the top of the menu
        menu_bar.add_cascade(label="Show", menu=self.show_menu)

        # Add options to the "Show" menu
        self.show_menu.add_command(label="Show History", command=self.show_history)
        self.show_menu.add_command(label="Show Memory Buttons", command=self.show_memory_frame)

        # Configure the root window to use the menu bar
        self.root.config(menu=menu_bar)

        # Allow for operations on exit
        self.root.protocol("WM_DELETE_WINDOW", self.on_exit)

    def get_next_key(self):
        key = 0
        while True:
            yield key
            key += 1

    def on_exit(self):
        for eq in self.equation_history:
            print(eq.equation, eq.solution)
        self.root.quit()

    def bind_keys(self):
        """Binds keyboard keys to their corresponding functions."""
        for i in range(10):
            self.root.bind(str(i), lambda event, num=i: self.button_click(num))
        self.root.bind('+', lambda event: self.set_operation('+', 'addition'))
        self.root.bind('-', lambda event: self.set_operation('-', 'subtraction'))
        self.root.bind('*', lambda event: self.set_operation('*', 'multiplication'))
        self.root.bind('/', lambda event: self.set_operation('/', 'division'))
        self.root.bind('c', lambda event: self.clear_display())  # Clear with 'c'
        self.root.bind('<Return>', lambda event: self.calculate_result())  # Enter key for '='
        self.root.bind('.', lambda event: self.point_clcik())
        self.root.bind('^', lambda event: self.set_operation('**', 'exponent'))
        self.root.bind('<Control-c>', lambda event: self.copy_to_clipboard())
        self.root.bind('<Control-v>', lambda event: self.paste_from_clipboard())

    def no_implementation(self):
        print("Button Clicked")

    def init_UI(self):
        # Current Render Row
        crow = 0
        # Create the Display
        self.equation_label = tk.Label(self.display, width=45, height=1,borderwidth=3, relief="groove", anchor="sw", padx=5, pady=5)
        self.result_label = tk.Label(self.display, width=18, height=1,borderwidth=3, relief="groove", anchor="se", padx=5, pady=5, font=("Courier", 25, 'bold') )
        self.equation_label.pack(padx=5, pady=0)
        self.result_label.pack(padx=5, pady=5)
        # Pack the Display
        self.display.grid(row=crow, column=0)
        crow += 1

        # Extra Functions
        operators = [
            ('MC', self.memory_clear, 0, 0),
            ('MR', self.memory_recall, 0, 2),
            ('MS', self.memory_set, 0, 1),
            ('M+', self.memory_add, 0, 3),
            ('M-', self.memory_sub, 0, 4)
        ]

        for symbol, command, row, col in operators:
            tk.Button(self.extra_functions, text=symbol, width=7, height=1, command=command).grid(row=row, column=col)

        self.extra_func_row = crow
        self.extra_functions.grid(row=self.extra_func_row, column=0)
        crow += 1

        if not self.memory_frame_visible:
            self.extra_functions.grid_forget()  # Hide the memory frame

        # Basic Function
        operators = [
            ('AC', self.clear_display, 0, 0),
            ('CE', self.clear_entry, 0, 1),
            ('Sqrt(x)', self.sqrt_click, 0, 2),
            ('.00', self.percent_click, 0, 3)
        ]
        for symbol, command, row, col in operators:
            tk.Button(self.basic_functions, text=symbol, width=10, height=2, command=command).grid(row=row, column=col)

        # Pack the Basic Functions below the display
        self.basic_functions.grid(row=crow, column=0)
        crow += 1

        # Buttons for basic operations
        operators = [
            ('x^y', lambda: self.set_operation('**', 'exponent'), 0, 0),
            ('(', lambda: self.set_operation('(', 'paren_open'), 0, 1),
            (')', lambda: self.set_operation(')', 'paren_close'), 0, 2),
            ('/', lambda: self.set_operation('/', 'division'), 0, 3),
            ('*', lambda: self.set_operation('*', 'multiplication'), 1, 3),
            ('-', lambda: self.set_operation('-', 'subtraction'), 2, 3),
            ('+', lambda: self.set_operation('+', 'addition'), 3, 3),
            ('.', self.point_click, 4, 0),
            ('-/+', self.negative_click, 4, 1),
            ('=', self.calculate_result, 4, 3)
        ]
        for symbol, command, row, col in operators:
            tk.Button(self.basic_operations, text=symbol, width=10, height=2, command=command).grid(row=row, column=col)

        # Buttons for numeric values
        for i in range(10):
            button = tk.Button(self.basic_operations, text=str(i), width=10, height=2, command=lambda num=i: self.button_click(num), bg='#AACCFF')
            row, col = divmod(9 - i, 3)  # Position calculation for numeric keypad layout
            col = (2 - col)
            button.grid(row=row + 1, column=col)

        # Pack the Numeric Buttons and Operations below the Function Buttons
        self.basic_operations.grid(row=crow, column=0)
        crow += 1

        # Display the history frame if it is enabled by default
        if self.history_frame_visible:
            self.history_frame.grid(row=0, column=1, rowspan=4, sticky='ns')
            self.history_label = tk.Label(self.history_frame, text="History will appear here.", bg='lightgray')
            self.history_label.pack()

        self.update_display()

    def show_memory_frame(self):
        # Hide memory buttons if currently visible
        if self.memory_frame_visible:
            self.extra_functions.grid_forget()  # Hide the memory frame
            self.memory_frame_visible = False
        # Show memory buttons if currrently not visible
        else:
            self.extra_functions.grid(row=self.extra_func_row, column=0)
            self.memory_frame_visible = True

    def update_history_frame(self):
        """Update history frame with text from object instances."""
        # Clear previous history items before updating
        HISTORY_LABEL_WIDTH = 40
        for widget in self.history_frame.winfo_children():
            widget.destroy()

        # Display a helpful message if history is blank
        if not self.equation_history:
            self.history_label = tk.Label(self.history_frame, width=HISTORY_LABEL_WIDTH, text="History will appear here.", bg='lightgray')
            self.history_label.pack()
        # Loop over the history objects and add each to the history frame
        for eq in self.equation_history:
            text = f"{eq.equation} = {eq.solution}"
            label = tk.Label(self.history_frame, width=HISTORY_LABEL_WIDTH, text=text, bg="lightgray")
            label.pack(fill=tk.X, pady=2)  # Adjust padding for spacing
            label.bind("<Button-1>", self.on_history_label_click)  # Bind the click event
            self.label_to_equation[label] = eq

    def memory_recall(self):
        self.current_number = list(self.memory)

        # Remove '.0' from the end of the number if it contains .0
        if len(self.current_number) >= 3:
            if ''.join(self.current_number).endswith('.0'):
                self.current_number = self.current_number[:-2]

        self.update_display()

    def update_display(self):
        result = 0
        # Update display, display the result if the current equation is solveable
        print(f'update_display {self.current_number=}')
        print(f'update_display {self.equation.equation=}')
        if self.display_memory:
            self.equation_label.config(text=f'mem: {"".join(self.memory)}:: {" ".join(self.equation.equation)}')
        else:
            self.equation_label.config(text=f'{" ".join(self.equation.equation)}')
        if self.current_number:
            # Remove '.0' from the end of the number if it contains .0
            if len(self.current_number) >= 3:
                if ''.join(self.current_number).endswith('.0'):
                    self.current_number = self.current_number[:-2]
            self.result_label.config(text=f'{"".join(self.current_number)}')
        else:
            self.result_label.config(text=f'0')

    def show_history(self):
        # Hide history if currently visible
        if self.history_frame_visible:
            self.history_frame.grid_forget()  # Hide the history frame
            self.history_frame_visible = False
        # Show history if currrently not visible
        else:
            self.history_frame.grid(row=0, column=1, rowspan=4, sticky='ns')
            self.history_frame_visible = True
            self.update_history_frame()

    def on_history_label_click(self, event):
        """Callback function for label click."""
        clicked_label = event.widget  # Get the label that was clicked
        label_text = clicked_label.cget("text")  # Get the text of the label
        equation_obj = self.label_to_equation.get(clicked_label)  # Retrieve the equation object
        if equation_obj:
            print(f"Clicked equation: {equation_obj.equation} = {equation_obj.solution}")

        # Set Equation and Reset operations
        self.equation = equation_obj
        self.current_number = list(str(self.equation.get_solution()))
        self.current_operation = None
        self.is_new = True

        self.update_display()
        self.equation = Equation()

    def button_click(self, number):
        """Appends a digit to the display."""
        if self.is_new:
            self.current_number = []
            self.is_new = False
        self.current_number.append(str(number))
        print(f'button_click {self.current_number=}')

        self.update_display()

    def point_click(self):
        if '.' not in self.current_number:
            self.current_number.append('.')
        else:
            # Potentially this could do something, either move the decimal, or place it at the end, for now mirror windows calc and do nothing
            pass

        self.update_display()

    def percent_click(self):
        if is_number(''.join(self.current_number)):
            num = float(''.join(self.current_number))
            num *= 0.01
            self.current_number = list(str(num))
        else:
            # Set current_number to zero with a decimal point, or do nothing, for now mimic behavoir of windows calculator and do nothing.
            #self.current_number = '0.'
            pass

        self.update_display()

    def sqrt_click(self):
        print(f'sqrt_click called {self.current_number=}')
        if is_number(''.join(self.current_number)):
            num = float(''.join(self.current_number))
            num = sqrt(num)
            self.current_number = list(str(num))
            self.is_new = True
        self.update_display()

    def negative_click(self):
        """Appends a negative to the current_number if positive, else removes negative."""
        if self.current_number[0] == '-':
            self.current_number.pop(0)
        else:
            self.current_number.insert(0, '-')

        self.update_display()


    def clear_display(self):
        """Clears the display."""
        self.equation.clear()
        # self.equation_label.config(text=' '.join(self.equation.equation))
        self.current_number = []

        self.update_display()

    def clear_entry(self):
        """Clears the display."""
        self.current_number = []
        # self.equation_label.config(text=' '.join(self.equation.equation))

        self.update_display()

    def set_operation(self, symbol, operation):
        """Sets the current operation and stores the first number."""
        # The operation variable is not currently used, but may be useful later to keep track of the names of more complex opperations where the symbol could be obscure or ambiguous

        # if an operation is entered and there is no number to record, replace the last operation with the new one
        print(f'set_operation() {self.current_number=}')
        if is_number("".join(self.current_number)):
            self.equation.append_term("".join(self.current_number))
            self.equation.append_opp(symbol)
        else:
            self.equation.append_opp(symbol)

        self.current_number = []
        print(f'set_operation() {self.equation.equation}')

        self.update_display()

    def memory_add(self):
        result = float(self.memory)
        result += float(''.join(self.current_number))
        self.memory = str(result)
        self.display_memory = True

        self.update_display()

    def memory_sub(self):
        result = float(self.memory)
        result -= float(''.join(self.current_number))
        self.memory = str(result)
        self.display_memory = True

        self.update_display()

    def memory_set(self):
        self.memory = ''.join(self.current_number)
        self.display_memory = True

        self.update_display()

    def memory_clear(self):
        self.memory = '0'
        self.display_memory = False

        self.update_display()

    def copy_to_clipboard(self):
        """Copies data to the clipboard."""
        # if len(self.equation.equation) >= 1:  # If an equation exists
        #     if self.equation.solution:
        #         self.clipboard = ''.join(self.equation.solution)
        #     else:  # Otherwise, copy the entire equation
        #         self.clipboard = self.equation.equation
        # else:
        #     self.clipboard = ''.join(self.current_number)
        self.clipboard = ''.join(self.current_number)

        pyperclip.copy(self.clipboard)
        print(f"Copied to clipboard: {self.clipboard}")  # Debugging log

    def paste_from_clipboard(self):
        """Pastes data from the clipboard."""
        clipboard_content = pyperclip.paste()

        # only support pasting number from windows clipboard, not equation as list for now
        if is_number(clipboard_content):
            self.clipboard = clipboard_content
            self.current_number = list(self.clipboard)

        # if isinstance(self.clipboard, list):  # Clipboard has an equation
        #     self.equation.set_equation_from_list(self.clipboard)
        # if isinstance(self.clipboard, str):  # Clipboard has a number
        #     try:

        #     except InvalidEquationException:
        #         pass
        #     except Exception:
        #         raise

        self.update_display()

        print(f"Pasted from clipboard: {self.clipboard}")  # Debugging log

        # Update display
        self.equation_label.config(text=f'{" ".join(self.equation.equation)} {"".join(self.current_number)}')

    def calculate_result(self):
        """Performs the selected operation and displays the result."""
        print(f'calculate_result() {self.current_number=}')

        if is_number("".join(self.current_number)):
            self.equation.append_term("".join(self.current_number))

        result = None
        try:
            result = self.equation.get_solution()
            self.equation_history.append(self.equation)
            self.update_history_frame()
        except ZeroDivisionError as e:
            self.equation_label.config(text=f'Error {e}')
            self.equation.clear()
        except Exception as e:
            self.equation_label.config(text=f'Error {e}')
            self.equation.clear()
            print(e)
            raise

        # Reset Equation and operations
        self.current_operation = None
        self.current_number = list(result)

        self.update_display()

        # Todo: update equation_history and self.label_to_equation so that we don't have two variables essentially storing the same thing, and so that we use proper keys instead of labels as keys
        # key = self.get_next_key()
        # self.label_to_equation.append([key, text, label, self.equation])

        self.equation = Equation()
        self.is_new = True


if __name__ == "__main__":
    root = tk.Tk()
    app = CalculatorApp(root)
    root.mainloop()

