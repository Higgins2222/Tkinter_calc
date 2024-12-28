# TODO

Clicking on a history item should replace the calculate_result with the history entry

Implement Parenthesis buttons

add memory buttons

allow paste for partial equation (ex: '8+3/')

clean up methods exponent, mult_div, add_sub and solver.  Maybe use lambdas to avoid repeated code, either add to equation class or create own class.

Add advanced mathematical operations (e.g., square roots, trigonometry).

Implement a dark mode or different themes for the interface.

Store the history of calculations even after the application is closed.

# Bugs

Pressing '=' with nothing in the equation_label results in a ValueError from the calculate_result function

History frame changes size based on entries, which results in too many window size changes overall


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