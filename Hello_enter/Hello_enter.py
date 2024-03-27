import tkinter as tk
from tkinter import *
def click(enter):
    text = Label(text='Hello world!')
    text.pack()
root = tk.Tk()
root.title('123')
root.geometry('400x300')
root.resizable(False,False)
enter = tk.Entry(root)
enter.pack()
enter.bind('<Key>', click)
root.mainloop()
