import random
from tkinter import *
def click(click1):
    length = random.randint(0,1900)
    height = random.randint(0,800)
    radius = 50
    canva.create_oval(length - radius, height - radius, length + radius, height + radius, width=5)
root = Tk()
root.title('Circle')
root.geometry('1500x700')
root.resizable(False,False)
canva = Canvas(bg='aqua')
canva.pack(fill=BOTH, expand=1)
canva.bind('<1>', click)
mainloop()
