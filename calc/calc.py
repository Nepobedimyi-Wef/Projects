import tkinter as tk
from tkinter import *
def click():
    summ = int(menu.get()) + int(menu1.get())
    text = Label(text='Summ:')
    text.pack()
    text = Label(text=summ)
    text.pack()
def click1():
    minus = int(menu.get()) - int(menu1.get())
    text = Label(text='Minus:')
    text.pack()
    text = Label(text=minus)
    text.pack()

root = tk.Tk()
root.title('123')
root.geometry('400x300')
menu = Entry()
menu.pack()
menu1 = Entry()
menu1.pack()
btn = Button(text='summ',padx='20',pady='20',font='20',command=click)
btn.pack()
btn1 = Button(text='minus',padx='20',pady='20',font='20',command=click1)
btn1.pack()
root.resizable(False,False)
root.mainloop()
