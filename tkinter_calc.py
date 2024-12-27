# order of operations is done correctly on the 'equation' display, and the textbox display still works like the originial in the tutorial that does not process order of operations.

# pressing '=' now resets the equation

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



equation = []

class CalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Calculator")
        
        self.current_operation = None
        self.first_number = None
        self.second_number = None

        # Entry widget for display
        self.display = tk.Entry(root, width=35, borderwidth=5)
        self.display.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

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


        equation_label = tk.Label(root, width=35, borderwidth=5)
        equation_label.grid(row=7, column=0, columnspan=3, padx=10, pady=10)

    def append_to_equation(self, first_number, operation):
        equation.append(str(first_number))
        equation.append(operation)
        print(equation)
        equation_label = tk.Label(root, text=' '.join(equation), width=35, borderwidth=5)
        equation_label.grid(row=7, column=0, columnspan=3, padx=10, pady=10)


    def button_click(self, number):
        """Appends a digit to the display."""
        current = self.display.get()
        self.display.delete(0, tk.END)
        self.display.insert(0, current + str(number))

    def clear_display(self):
        """Clears the display."""
        self.display.delete(0, tk.END)

    def button_add(self):
        self.append_to_equation(int(self.display.get()), '+')
        self.set_operation('addition')
        

    def button_subtract(self):
        self.append_to_equation(int(self.display.get()), '-')
        self.set_operation('subtraction')
        

    def button_multiply(self):
        self.append_to_equation(int(self.display.get()), '*')
        self.set_operation('multiplication')
        

    def button_divide(self):
        self.append_to_equation(int(self.display.get()), '/')
        self.set_operation('division')
        

    def set_operation(self, operation):
        """Sets the current operation and stores the first number."""
        print(f'{self.first_number=} {self.second_number=}')
        if self.first_number:
            self.calculate_result_inline()        
        self.first_number = int(self.display.get())
        self.current_operation = operation

        self.clear_display()

    def calculate_result_inline(self):
        """Performs the selected operation and displays the result."""
        second_number = int(self.display.get())
        result = None

        if self.current_operation == 'addition':
            result = self.first_number + second_number
        elif self.current_operation == 'subtraction':
            result = self.first_number - second_number
        elif self.current_operation == 'multiplication':
            result = self.first_number * second_number
        elif self.current_operation == 'division':
            if second_number == 0:
                result = "Error"  # Handling division by zero
            else:
                result = self.first_number / second_number

        self.clear_display()
        self.first_number = None
        self.current_operation = None
        if result is not None:
            self.display.insert(0, str(result))

    def calculate_result(self):
        global equation
        """Performs the selected operation and displays the result."""
        second_number = int(self.display.get())
        result = None

        self.calculate_result_inline()

        equation.append(str(second_number))

        equation_int = [float(x) if x.isdigit() else x for x in equation]

        result = solver(equation_int)
        equation_label = tk.Label(root, text=str(result), width=35, borderwidth=5)
        equation_label.grid(row=7, column=0, columnspan=3, padx=10, pady=10)
        equation = []





if __name__ == "__main__":
    root = tk.Tk()
    app = CalculatorApp(root)
    root.mainloop()
