from tkinter import *
from tkinter import ttk
from tkinter import messagebox


import sqlite3


from todo import Todo

class Todo_list():
    
    def __init__(self):
        self.todos = []
        self.connection = sqlite3.connect("data.db")
        self.cursor = self.connection.cursor()
        self.button_identities = []

        

    def add_todo(self, todo):
        self.todos.append(todo)

    def draw(self, canvas):
        for i, todo in enumerate(self.todos):
            text = f"No.:  {todo.todo_number} Status: {todo.todo_status} | Text: {todo.todo_text}"
            canvas_text = canvas.create_text((400, (i*30)+100), text=text, font=('Arial',11),anchor=NW)
            button = Button(text = "Delete", command = lambda i=todo.todo_number: self.delete(i), anchor = W)
            button.configure(width = 10, activebackground = "#33B5E5", relief = FLAT)
            button_window = canvas.create_window(750, (i*30)+100, anchor=NW, window=button)
            self.button_identities.append(button)

    def del_todos(self):
        self.todos = []

    def delete(self, i):
        try:
            with self.connection as con:
                cur = con.cursor()
                print(i)
                cur.execute("DELETE from todo WHERE todo_number = ?",(i,))
        except IOError:
            print("Unable to open database")
        
        
            

    