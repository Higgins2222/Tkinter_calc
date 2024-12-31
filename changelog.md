# TODO

Add advanced mathematical operations (trigonometry, n!, 1/x)

Allow copy/paste of equations.

clean up methods exponent, mult_div, add_sub and solver.  Maybe use lambdas to avoid repeated code, either add to equation class or create own class.

Implement a dark mode or different themes for the interface.

Store the history of calculations even after the application is closed.

 - IN def calculate_result(self):
 - update equation_history and self.label_to_equation so that we don't have two variables essentially storing the same thing, and so that we use proper keys instead of labels as keys

Currently, the equation object must be reset to a new object once the result is calculated, this is because the append num and opp functions will break if the equation is left in as solved.  Refactor this implementation so a solved equation can be stored correctly and remove 'self.equation = Equation()' from various functions that make this call.

Consider an update_window() function that calls update_history_frame and update_display instead of handeling them seperately

Add command line call that accepts an equation

# Build 012

Memory Buttons (MC, MR, MS, M+, M-) have been added.

Memory shows up in the equation display if it is being used.

Menu option added to show/hide memory buttons.

app.current_number is no longer being converted to float then back to string before being stored when an operation is being input

Clipboard now copy and pastes the current number only, there is no copy/pasting of equations currently.

All known issues have been resolved.

'Pressing '=' with nothing in the equation_label results in a ValueError from the calculate_result function', is now fixed

'History frame changes size based on entries, which results in too many window size changes overall', is now fixed, width is set within labels in update_history_frame

'Dividing by 0 raises an exception but the equation is not handled correctly after producing a solution, not updating vars correctly, and resulting in undefined behavoir.' ZeroDivisionError is now caught in calculate_result and the equation is reset.

# Known Issues

None, as of build 12.

# Build 011
[12/30/2024]

app.create_buttons() renamed to app.init_UI()

Added result_label for to display just the result in a larger font after compute

Refactored validate_equation(), fixed errors with validating equations containing parenthesis, otherwise functionality unchanged.

Implemented Parenthesis buttons.

Major bug was introduced in version 08 when enclosing solver helper functions into the solver function, parenthesis did not compute correctly, equation has been seperated again.

removed equation.append_term_and_opp()

equation.solution is now stored as a string. equation.has_result has been removed as equation.solution will now return as True even when the solution is zero.

equation.append_opp now raises exceptions

# Build 010

Clicking on a history item will now replace the calculate_result with the history entry, update the equation object of the app class, and update the current number to the result of the equation.

button_add(), button_subtract(), ... have been removed and set_operation() with correct params is now called directly by each button

app.update_display() is now added, reducing redundent code.

# Build 009

Greatly streamlined button rendering.

Rearanged frames into; display, basic_functions, basic_operations, and history_frame.  Frames are now either packed or packed by grid, and set according to grid.

History frame is hidden by default, and the option to show it has been moved to a title bar menu.

Exponent title now shows as 'x^y' updated from '^'

Negative number button now shows as '-/+' updated from '-'

# Build 008

Added validate_equation function, which takes a list, and validates if the terms in the list form a proper equation; alternating numbers and operators, with valid opening and closing parenthesis.

validate_equation is intentionally excluded from being a class member function as we may want to use it on an equation without an instance of the equation object, such as if an equation is being inserted from the clipboard.

solver function now creates a copy of the equation instead of destroying it, and the return value is now just one value instead of one value contained in a list.  The helper functions to solver have been moved within the equation itself to make them inaccessible.

CalculatorApp.bind_keys(...) has been added, allowing for keyboard buttons to mirror gui buttons

Pressing '-' (negative num) now turns the number positive if it is negative.  Pressing '.' while the number contains a decimal point already now does nothing.

Some simple clipboard logic has been added. Supports windows clipboard through pyperclip.  Allows copy paste of equation within the app, allows paste of num from windows clipboard.  Hardening and/or Validation testing has not been attempted on this functionality if needed.

History frame has been added that shows history of equations in current session.

UI redesign begun, number buttons are now in their own frame 'number_buttons_frame'

History frame now has on click events

Top Menu has been added for future use.

app.on_exit has been added for debugging.

# Build 007

self.display has been removed entirely

calculate_result_inline has been removed as we no longer calculate the result as we are entering an equation, as we are now always respecting order of opperations

#added equation class instead of equation global var

#the equation now clears on pressing clear_display, no longer calling clear_display for each clear, only when the clear button is pressed


bug, errors present when float is introduced by division

Some error handeling has been added for divide by 0

removed all but one debugging print statement

we now use a self.label member variable and the label.config method to update the label box dispalying the equation

perform_operation has now been added to the CalculatorApp class to simplify repeated text inside the opperation button functions

the self.label member variable now shows the full equation and the result when pressing '='

the self.label member variable now properly shows as empty when clear is pressed

removed unused variables including self.current_operation

removed stray comments

added a decimal point button

added an exponent button

added a square root button

added a negative sign button