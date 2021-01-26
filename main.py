import tkinter as tk
import sqlite3

from todo import Todo

connection = sqlite3.connect("data.db")

root = Tk()
root.title("Tom's todo App")
canvas = Canvas(root, width=800, height=800)







canvas.pack()



root.mainloop()