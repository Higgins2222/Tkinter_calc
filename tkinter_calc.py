# tkinter_calc.py
# Author: Higgins
# Build 09

import tkinter as tk
import pyperclip
import cProfile # For profiling startup

VALID_OPERATIONS = ['*', '/', '+', '-', '**']

def solver(equation):
    def exponent(equation):
        result = []

        while equation:
            token = equation.pop(0)

            if token == '**':
                left = temp.pop()
                right = equation.pop(0)
                solution = left ** right
                result.append(solution)
            else:
                result.append(token)

        return result
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
                if right == 0:
                        raise ValueError("Division by zero")
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

    equation = equation.copy()
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
    except Exception as e:
        raise e

def validate_equation(equation: list):
    print('validating', equation)

    #first char should either be: float, int, or '('
    open_paren = 0
    has_num = False
    is_valid = True
    for term in equation:
        # open parenthesis are only valid when expecting a number
        if not has_num and term == '(':
            open_paren += 1
        # if has_num is False, we need the next term to be an int or float
        elif not has_num:
            has_num = is_number(term)
            # needed a number, is not number, this equation is not valid
            if not has_num:
                is_valid = False
        # we can only close paren after recording an int or float
        elif has_num and term == ')':
            open_paren -= 1
            has_num = False
        elif has_num and term in VALID_OPERATIONS:
            has_num = False
        else:
            is_valid = False

    # check we have an equal amount of open and close parens
    if open_paren != 0:
        is_valid = False

    return is_valid

class InvalidEquationException(Exception):
    def __init__(self, equation, message="Invalid equation format or structure"):
        self.equation = equation
        self.message = message
        super().__init__(f"{message}: {equation}")

class Equation:
    def __init__(self):
        self.equation = []
        self.has_result = False
        self.solution = None

    def append_term_and_opp(self, num, operation):
        # todo: if num.isdigit():
        self.equation.append(str(num))
        # todo: if operation in list_of_opps:
        self.equation.append(operation)
        #print(equation)

    def append_term(self, num):
        # note: this will commonly be called as '=' is pressed
        # todo: if num.isdigit():
        # todo: if equation[-1] in list_of_opps
        self.equation.append(str(num))

    def replace_opp(self, operation):
        self.equation.pop()
        self.equation.append(operation)\

    def clear(self):
        self.equation = []

    def get_solution(self):
        print(self.equation)
        if not validate_equation(self.equation):
            raise InvalidEquationException(self.equation)
        
        equation_int = [float(x) if is_number(x) else x for x in self.equation]
        self.solution = solver(equation_int)
        self.has_result = True
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

        # A history of all solved equations
        self.equation_history = []

        # Applocal Clipboard
        self.clipboard = None

        # Track history panel visibility
        self.history_frame_visible = False

        # Create Frames for layout management
        self.display = tk.Frame(self.root)
        self.basic_operations = tk.Frame(self.root)
        self.basic_functions = tk.Frame(self.root)
        self.history_frame = tk.Frame(self.root, width=225, relief="solid", bg="#AAAAAA")

        # Bind keyboard keys
        self.bind_keys()

        # GUI Buttons
        # root.after(100, self.create_buttons()) # Option to defer startup, to speed up initial window render
        self.create_buttons()

        # Allow for operations on exit
        self.root.protocol("WM_DELETE_WINDOW", self.on_exit)

    def on_exit(self):
        for eq in self.equation_history:
            print(eq.equation, eq.solution)
        self.root.quit()

    def bind_keys(self):
        """Binds keyboard keys to their corresponding functions."""
        for i in range(10):
            self.root.bind(str(i), lambda event, num=i: self.button_click(num))
        self.root.bind('+', lambda event: self.button_add())
        self.root.bind('-', lambda event: self.button_subtract())
        self.root.bind('*', lambda event: self.button_multiply())
        self.root.bind('/', lambda event: self.button_divide())
        self.root.bind('c', lambda event: self.clear_display())  # Clear with 'c'
        self.root.bind('<Return>', lambda event: self.calculate_result())  # Enter key for '='
        self.root.bind('.', lambda event: self.point_click())
        self.root.bind('^', lambda event: self.button_exponent())
        self.root.bind('<Control-c>', lambda event: self.copy_to_clipboard())
        self.root.bind('<Control-v>', lambda event: self.paste_from_clipboard())

    def no_implementation(self):
        print("Button Clicked")

    def create_buttons(self):
        # Create the Display
        self.equation_label = tk.Label(self.display, width=45, height=2,borderwidth=3, relief="groove", anchor="sw", padx=5, pady=5)
        self.equation_label.pack(padx=10, pady=10)

        # Pack the Display
        self.display.grid(row=0, column=0)

        # Basic Function
        operators = [
            ('AC', self.clear_display, 0, 0),
            ('CE', self.clear_entry, 0, 1),
            ('...', self.no_implementation, 0, 2),
            ('...', self.no_implementation, 0, 3)
        ]
        for symbol, command, row, col in operators:
            tk.Button(self.basic_functions, text=symbol, width=10, height=2, command=command).grid(row=row, column=col)

        # Pack the Basic Functions below the display
        self.basic_functions.grid(row=1, column=0)

        # Buttons for basic operations
        operators = [
            ('x^y', self.button_exponent, 0, 0),
            ('(', self.no_implementation, 0, 1),
            (')', self.no_implementation, 0, 2),
            ('/', self.button_divide, 0, 3),
            ('*', self.button_multiply, 1, 3),
            ('-', self.button_subtract, 2, 3),
            ('+', self.button_add, 3, 3),
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
        self.basic_operations.grid(row=2, column=0)

        # Display the history frame if it is enabled by default
        if self.history_frame_visible:
            self.history_frame.grid(row=0, column=1, rowspan=3, sticky='ns')
            self.history_label = tk.Label(self.history_frame, text="History will appear here.", bg='lightgray')
            self.history_label.pack()

        # Create a menu bar
        menu_bar = tk.Menu(self.root)

        # Create a "Show" menu
        self.show_menu = tk.Menu(menu_bar, tearoff=0)  # tearoff=0 removes the dotted line at the top of the menu
        menu_bar.add_cascade(label="Show", menu=self.show_menu)

        # Add options to the "Show" menu
        self.show_menu.add_command(label="Show History", command=self.show_history)

        # Configure the root window to use the menu bar
        self.root.config(menu=menu_bar)

    def update_history_frame(self):
        """Update history frame with text from object instances."""
        # Clear previous history items before updating
        for widget in self.history_frame.winfo_children():
            widget.destroy()

        # Display a helpful message if history is blank
        if not self.equation_history:
            self.history_label = tk.Label(self.history_frame, text="History will appear here.", bg='lightgray')
            self.history_label.pack()
        # Loop over the history objects and add each to the history frame
        for eq in self.equation_history:
            text = f"{eq.equation} = {eq.solution}"
            label = tk.Label(self.history_frame, text=text, bg="lightgray")
            label.pack(fill=tk.X, pady=2)  # Adjust padding for spacing
            label.bind("<Button-1>", self.on_history_label_click)  # Bind the click event

    def show_history(self):
        # Hide history if currently visible
        if self.history_frame_visible:
            self.history_frame.grid_forget()  # Hide the history frame
            self.history_frame_visible = False
        # Hide history if currrently not visible
        else:
            self.history_frame.grid(row=0, column=1, rowspan=3, sticky='ns')
            self.history_frame_visible = True
            self.update_history_frame()

    def on_history_label_click(self, event):
        """Callback function for label click."""
        clicked_label = event.widget  # Get the label that was clicked
        label_text = clicked_label.cget("text")  # Get the text of the label
        print(f"Label clicked: {label_text}")

    def point_click(self):
        if '.' not in self.current_number:
            self.current_number.append('.')
        else:
            # Potentially this could do something, either move the decimal, or place it at the end, for now mirror windows calc and do nothing
            pass
        # Update display
        self.equation_label.config(text=f'{" ".join(self.equation.equation)} {"".join(self.current_number)}')

    def negative_click(self):
        """Appends a negative to the current_number if positive, else removes negative."""
        if self.current_number[0] == '-':
            self.current_number.pop(0)
        else:
            self.current_number.insert(0, '-')
        # Update display
        self.equation_label.config(text=f'{" ".join(self.equation.equation)} {"".join(self.current_number)}')

    def button_click(self, number):
        """Appends a digit to the display."""
        if self.is_new:
            self.current_number = []
            self.is_new = False
        self.current_number.append(str(number))
        # Update display
        self.equation_label.config(text=f'{" ".join(self.equation.equation)} {"".join(self.current_number)}')

    def clear_display(self):
        """Clears the display."""
        self.equation.clear()
        self.equation_label.config(text=' '.join(self.equation.equation))
        self.current_number = []

    def clear_entry(self):
        """Clears the display."""
        self.current_number = []
        self.equation_label.config(text=' '.join(self.equation.equation))

    def set_operation(self, symbol, operation):
        """Sets the current operation and stores the first number."""
        # The operation variable is not currently used, but may be useful later to keep track of the names of more complex opperations where the symbol could be obscure or ambiguous

        # if an operation is entered and there is no number to record, replace the last operation with the new one
        if is_number("".join(self.current_number)):
            num = float("".join(self.current_number))
            self.equation.append_term_and_opp(num, symbol)
        else:
            self.equation.replace_opp(symbol)

        self.current_number = []

        # Update display
        self.equation_label.config(text=' '.join(self.equation.equation))

    def button_add(self):
        self.set_operation('+', 'addition')

    def button_subtract(self):
        self.set_operation('-', 'subtraction')

    def button_multiply(self):
        self.set_operation('*', 'multiplication')

    def button_divide(self):
        self.set_operation('/', 'division')

    def button_exponent(self):
        self.set_operation('**', 'exponent')
        #self.current_number.append('**')
        #self.equation_label.config(text=f'{" ".join(self.equation.equation)} {"".join(self.current_number)}')

    def copy_to_clipboard(self):
        """Copies data to the clipboard."""
        if len(self.equation.equation) >= 1:  # If an equation exists
            if self.equation.has_result:
                self.clipboard = ''.join(self.equation.solution)
            else:  # Otherwise, copy the entire equation
                self.clipboard = self.equation.equation
        else:
            self.clipboard = ''.join(self.current_number)
        pyperclip.copy(self.clipboard)
        print(f"Copied to clipboard: {self.clipboard}")  # Debugging log

    def paste_from_clipboard(self):
        """Pastes data from the clipboard."""
        clipboard_content = pyperclip.paste()

        # only support pasting number from windows clipboard, not equation as list for now
        if is_number(clipboard_content):
            self.clipboard = clipboard_content

        if isinstance(self.clipboard, list):  # Clipboard has an equation
            self.equation.set_equation_from_list(self.clipboard)
        elif isinstance(self.clipboard, str):  # Clipboard has a number
            try:
                self.current_number = list(self.clipboard)
            except InvalidEquationException:
                pass
            except Exception as e:
                raise e

        print(f"Pasted from clipboard: {self.clipboard}")  # Debugging log

        # Update display
        self.equation_label.config(text=f'{" ".join(self.equation.equation)} {"".join(self.current_number)}')

    def calculate_result(self):
        """Performs the selected operation and displays the result."""
        print(self.current_number)
        num = float("".join(self.current_number))
        self.equation.append_term(str(num))

        result = None
        try:
            result = self.equation.get_solution()
            # Update display
            self.equation_label.config(text=f'{" ".join(self.equation.equation)} = {str(result)}')
        except Exception as e:
            self.equation_label.config(text=f'Error {e}')

        # Reset Equation and operations
        self.current_operation = None
        self.current_number = list(str(result))
        print(self.current_number)
        self.equation_history.append(self.equation)
        self.equation = Equation()
        self.is_new = True
        self.update_history_frame()



# def main():
if __name__ == "__main__":
    root = tk.Tk()
    app = CalculatorApp(root)
    root.mainloop()

# cProfile.run('main()')
