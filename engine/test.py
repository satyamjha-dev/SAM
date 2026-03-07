

import tkinter as tk

# function for addition
def add():
    num1 = float(entry1.get())
    num2 = float(entry2.get())
    result.set(num1 + num2)

# function for subtraction
def subtract():
    num1 = float(entry1.get())
    num2 = float(entry2.get())
    result.set(num1 - num2)

# main window
root = tk.Tk()
root.title("Simple Calculator")

# variable to store result
result = tk.StringVar()

# labels
tk.Label(root, text="Enter First Number").grid(row=0, column=0, padx=10, pady=5)
tk.Label(root, text="Enter Second Number").grid(row=1, column=0, padx=10, pady=5)
tk.Label(root, text="Result").grid(row=4, column=0, padx=10, pady=5)

# entry fields
entry1 = tk.Entry(root)
entry2 = tk.Entry(root)
entry1.grid(row=0, column=1, padx=10, pady=5)
entry2.grid(row=1, column=1, padx=10, pady=5)

# buttons
tk.Button(root, text="Add", command=add).grid(row=2, column=0, pady=10)
tk.Button(root, text="Subtract", command=subtract).grid(row=2, column=1, pady=10)

# result display
tk.Entry(root, textvariable=result, state="readonly").grid(row=4, column=1, padx=10, pady=5)

# run application
root.mainloop()