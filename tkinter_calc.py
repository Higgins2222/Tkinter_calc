from tkinter import *

root = Tk()
root.title('Simple Calculator')

e = Entry(root, width=35, borderwidth=5)
e.grid(row=0, column=0, columnspan=3, padx=10, pady=10)



def button_click(number):
    current = e.get()
    e.delete(0, END)
    e.insert(0, current + str(number))

def button_clearscreen():
    e.delete(0, END)

def button_add_():
    first_number = e.get()
    global f_num
    global opperation
    opperation = 'addition'
    f_num = int(first_number)
    e.delete(0, END)

    return

def button_subtract_():
    first_number = e.get()
    global f_num
    global opperation
    opperation = 'subtraction'
    f_num = int(first_number)
    e.delete(0, END)

    return

def button_multiply_():
    first_number = e.get()
    global f_num
    global opperation
    opperation = 'multiplication'
    f_num = int(first_number)
    e.delete(0, END)

    return

def button_divide_():
    first_number = e.get()
    global f_num
    global opperation
    opperation = 'division'
    f_num = int(first_number)
    e.delete(0, END)

    return

def button_equal_():
    second_number = e.get()
    e.delete(0, END)
    if opperation == 'addition':
        e.insert(0, f_num + int(second_number))
    elif opperation == 'subtraction':
        e.insert(0, f_num - int(second_number))
    elif opperation == 'multiplication':
        e.insert(0, f_num * int(second_number))
    elif opperation == 'division':
        e.insert(0, f_num / int(second_number))


button_1 = Button(root, text='1', padx=40, pady=20, command=lambda: button_click(1))
button_2 = Button(root, text='2', padx=40, pady=20, command=lambda: button_click(2))
button_3 = Button(root, text='3', padx=40, pady=20, command=lambda: button_click(3))
button_4 = Button(root, text='4', padx=40, pady=20, command=lambda: button_click(4))
button_5 = Button(root, text='5', padx=40, pady=20, command=lambda: button_click(5))
button_6 = Button(root, text='6', padx=40, pady=20, command=lambda: button_click(6))
button_7 = Button(root, text='7', padx=40, pady=20, command=lambda: button_click(7))
button_8 = Button(root, text='8', padx=40, pady=20, command=lambda: button_click(8))
button_9 = Button(root, text='9', padx=40, pady=20, command=lambda: button_click(9))
button_0 = Button(root, text='0', padx=40, pady=20, command=lambda: button_click(0))
button_add = Button(root, text='+', padx=39, pady=20, command=lambda: button_add_())
button_equal = Button(root, text='=', padx=91, pady=20, command=lambda: button_equal_())
button_clear = Button(root, text='Clear', padx=79, pady=20, command=button_clearscreen)

button_subtract = Button(root, text='-', padx=40, pady=20, command=lambda: button_subtract_())
button_multiply = Button(root, text='*', padx=40, pady=20, command=lambda: button_multiply_())
button_divide = Button(root, text='/', padx=40, pady=20, command=lambda: button_divide_())


button_7.grid(row=1, column=0)
button_8.grid(row=1, column=1)
button_9.grid(row=1, column=2)

button_4.grid(row=2, column=0)
button_5.grid(row=2, column=1)
button_6.grid(row=2, column=2)

button_1.grid(row=3, column=0)
button_2.grid(row=3, column=1)
button_3.grid(row=3, column=2)

button_0.grid(row=4, column=0)
button_clear.grid(row=4, column=1, columnspan=2)

button_add.grid(row=5, column=0)
button_equal.grid(row=5, column=1, columnspan=2)

button_subtract.grid(row=6, column=0)
button_multiply.grid(row=6, column=1)
button_divide.grid(row=6, column=2)







root.mainloop()
