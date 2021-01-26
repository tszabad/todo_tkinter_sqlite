from tkinter import *
import sqlite3

from todo import Todo

class Todo_list():
    
    def __init__(self):
        self.todos = []

    def add_todo(self, todo):
        self.todos.append(todo)

    def draw(self, canvas):
        for todo in self.todos:
            canvas.create_rectangle(0, 0, 600, 30, fill = "grey")
            text = f"No.:  {todo.todo_number} Status: {todo.todo_status} | Text: {todo.todo_text}"
            canvas_text = canvas.create_text(10, 10, text=text, font=('freemono bold',11),anchor=NW)
            

    