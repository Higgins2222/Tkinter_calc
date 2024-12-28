# Simple Calculator App

A simple calculator built with Python and Tkinter for graphical user interface (GUI). This application allows users to perform basic arithmetic operations such as addition, subtraction, multiplication, division, and exponentiation.

## Features

- **Basic Arithmetic**: Perform addition, subtraction, multiplication, division, and exponentiation.
- **Clear & Delete Functions**: Clear the display or delete the last input.
- **History**: Track past calculations and display them in a history panel.
- **Keyboard Support**: Allows number and operator input through both buttons and the keyboard.

## Installation

To run this project, you need Python 3.x installed on your system. You also need to have the `Tkinter` library, which is typically included with Python. If you don't have Tkinter installed, you can install it with the following command:

```bash
# On Ubuntu-based systems
sudo apt-get install python3-tk
```

## Clone the repository

```
git clone https://github.com/your-username/calculator-app.git
cd calculator-app
```

## Usage

Run the script using Python:
```
python tkinter_calc.py
```
The calculator window will appear, and you can begin performing calculations by clicking the buttons or using the keyboard.

## Keyboard Shortcuts

Ctrl+C: Copy the current equation to the clipboard.
Ctrl+V: Paste the equation from the clipboard into the input area.

## Screenshots

TODO: Add Screenshots

## Known Issues

The history panel has inconsistant size.
Pressing '=' with nothing in the equation_label results in a ValueError from the calculate_result function

## Future Improvements

Add advanced mathematical operations (e.g., square roots, trigonometry).
Implement a dark mode or different themes for the interface.
Store the history of calculations even after the application is closed.

## License

This project is licensed under the MIT License - see the LICENSE file for details.