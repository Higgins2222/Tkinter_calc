# Build 6
# self.display has been removed entirely

# calculate_result_inline has been removed as we no longer calculate the result as we are entering an equation, as we are now always respecting order of opperations

#...
#added equation class instead of equation global var

#the equation now clears on pressing clear_display, no longer calling clear_display for each clear, only when the clear button is pressed

# FIXED as of version 5
#### bug, errors present when float is introduced by division

# Some error handeling has been added for divide by 0

# removed all but one debugging print statement

# we now use a self.label member variable and the label.config method to update the label box dispalying the equation

# perform_operation has now been added to the CalculatorApp class to simplify repeated text inside the opperation button functions

# the self.label member variable now shows the full equation and the result when pressing '='

# the self.label member variable now properly shows as empty when clear is pressed

# removed unused variables including self.current_operation

# removed stray comments

# added a decimal point button

# added an exponent button

# added a square root button

# added a negative sign button


### todo ###
# clean up methods exponent, mult_div, add_sub and solver.  Maybe use lambdas to avoid repeated code, either add to equation class or create own class

# add error checking to make sure equation is well formed

# make keyboard number buttons work
    # add a way to hide the number buttons

# add a history

# add parentheses buttons

# add memory buttons

# add a clear current number button

# error display for things like 5, +, *, 3, or 5, 5, +, 5

# add back in the entry box and allow a full equation to be input at once (copy paste)

# UI improvements, make it look nice

import tkinter as tk


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

    return temp

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

class Equation:
    def __init__(self):
        self.equation = []

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

    def clear(self):
        self.equation = []

    def get_solution(self):
        print(self.equation)
        equation_int = [float(x) if is_number(x) else x for x in self.equation]
        return solver(equation_int)[0]


class CalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Calculator")
        

        self.current_number = []

        self.equation = Equation()

        # Creating the buttons
        self.create_buttons()

    def create_buttons(self):
        # Numeric buttons
        for i in range(10):
            button = tk.Button(self.root, text=str(i), padx=40, pady=20,
                               command=lambda num=i: self.button_click(num))
            row, col = divmod(9 - i, 3)  # Position calculation for numeric keypad layout
            button.grid(row=row + 1, column=col)

        # Operator buttons
        operators = [
            ('+', self.button_add, 4, 0),
            ('-', self.button_subtract, 5, 0),
            ('*', self.button_multiply, 5, 1),
            ('/', self.button_divide, 5, 2),
        ]
        for symbol, command, row, col in operators:
            tk.Button(self.root, text=symbol, padx=40, pady=20, command=command).grid(row=row, column=col)

        # Special buttons
        tk.Button(self.root, text='Clear', padx=79, pady=20, command=self.clear_display).grid(row=4, column=1, columnspan=2)
        tk.Button(self.root, text='=', padx=91, pady=20, command=self.calculate_result).grid(row=6, column=1, columnspan=2)

        tk.Button(self.root, text='.', padx=38, pady=20, command=self.point_click).grid(row=7, column=0)

        tk.Button(self.root, text='^', padx=38, pady=20, command=self.button_exponent).grid(row=7, column=1)

        tk.Button(self.root, text='-', padx=38, pady=20, command=self.negative_click).grid(row=7, column=2)

        self.equation_label = tk.Label(root, width=35, borderwidth=5)
        self.equation_label.grid(row=8, column=0, columnspan=3, padx=10, pady=10)

    def point_click(self):
        self.current_number.append('.')
        self.equation_label.config(text=f'{" ".join(self.equation.equation)} {"".join(self.current_number)}')

    def negative_click(self):
        self.current_number.insert(0, '-')
        self.equation_label.config(text=f'{" ".join(self.equation.equation)} {"".join(self.current_number)}')

    def button_click(self, number):
        """Appends a digit to the display."""
        self.current_number.append(str(number))
        self.equation_label.config(text=f'{" ".join(self.equation.equation)} {"".join(self.current_number)}')

    def clear_display(self):
        """Clears the display."""
        self.equation.clear()
        self.equation_label.config(text=' '.join(self.equation.equation))
        self.current_number = []

    def set_operation(self, symbol, operation):
        """Sets the current operation and stores the first number."""
        # The operation variable is not currently used, but may be useful later to keep track of the names of more complex opperations where the symbol could be obscure or ambiguous

        num = float("".join(self.current_number))
        self.equation.append_term_and_opp(num, symbol)
        self.current_number = []
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

    def calculate_result(self):
        """Performs the selected operation and displays the result."""
        print(self.current_number)
        num = float("".join(self.current_number))
        self.equation.append_term(str(num))

        result = None
        try:
            result = self.equation.get_solution()
            self.equation_label.config(text=f'{" ".join(self.equation.equation)} = {str(result)}')
        except Exception as e:
            self.equation_label.config(text=f'Error {e}')

        self.current_operation = None
        self.current_number = list(str(result))
        print(self.current_number)
        self.equation.clear()




if __name__ == "__main__":
    root = tk.Tk()
    app = CalculatorApp(root)
    root.mainloop()
