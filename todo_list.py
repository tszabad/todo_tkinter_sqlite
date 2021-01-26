from tkinter import *
import sqlite3

from todo import Todo

class Todo_list():
    
    def __init__(self):
        self.todos = []

    def add_todo(self, todo):
        self.todos.append(todo)

    def draw(self, canvas):
        for i, todo in enumerate(self.todos):
            canvas.create_rectangle(400, (i+30)*30, 800, (i+1)*30)
            text = f"No.:  {todo.todo_number} Status: {todo.todo_status} | Text: {todo.todo_text}"
            canvas_text = canvas.create_text((400, (i*30)+30), text=text, font=('freemono bold',11),anchor=NW)

    def del_todos(self):
        self.todos = []
            

    