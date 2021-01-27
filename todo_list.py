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

        self.root = Tk()
        self.root.title("Tom's todo App")
        self.canvas = Canvas(self.root, width=800, height=800)   
        entry1 = ttk.Entry(self.root)
        label1 = ttk.Label(self.root, text = '< Name of the label >')
        l1 = ttk.Label(self.root, text = 'To-Do List', font=('freemono bold',20),anchor=NW)
        l2 = ttk.Label(self.root, text='Enter task title: ')
        self.e1 = ttk.Entry(self.root, width=80)
        b1 = ttk.Button(self.root, text='Add task', width=50, command=self.write_file)
        b3 = ttk.Button(self.root, text='Delete all', width=50, command=self.delete_all)
        b4 = ttk.Button(self.root, text='Exit', width=50, command=self.bye)
        l2.place(x=80, y=50)
        self.e1.place(x=80, y=80)
        b1.place(x=80, y=110)
        b3.place(x=80, y=140)
        b4.place(x=400, y =140)
        l1.place(x=80, y=10)
        
        self.read_file()
        self.draw()
        
        
    def write_file(self):
        todo = self.e1.get()
        status = 1
        if len(todo)==0:
            messagebox.showinfo('Empty Entry', 'Enter task name')
        else:
            try:
                with self.connection as con:
                    cur = con.cursor()
                    last = cur.execute("SELECT todo_number FROM todo ORDER BY todo_number DESC LIMIT 1").fetchone()
                    if last is None:
                        number = 1
                    else:
                        number = last[0] + 1
                    cur.execute("INSERT INTO todo VALUES (?, ?, ?);", (number, status, todo))
            except IOError:
                print("Unable to open database")
            self.e1.delete(0,'end')
            self.todos = []
            self.read_file()
            self.draw()
    

    def read_file(self):
        done = "closed"
        undone = "open"
        try:
            with self.connection as con:
                cur = con.cursor()
                rows = cur.execute("SELECT todo_number, todo_status, todo_text FROM todo").fetchall()
                print(rows)
                for i in rows:
                    if len(rows) > 0:
                        symbol = undone if i[1] == 1 else done
                        todo = Todo(i[0], symbol, i[2])
                        self.todos.append(todo)
        except IOError:
            print("Unable to open database")

    def bye(self):
        self.root.destroy()
    
    def delete_all(self):
        try:
            with self.connection as con:
                cur = con.cursor()
                cur.execute("DELETE from todo")
        except IOError:
            print("Unable to open database")
        self.todos = []
        self.canvas.delete("all")

    def draw(self):
        for i, todo in enumerate(self.todos):
            text = f"No.:{todo.todo_number} | Status: {todo.todo_status} | Todo: {todo.todo_text}"
            canvas_text = self.canvas.create_text((80, (i*30)+200), text=text, font=('Arial',11),anchor=NW)
            button = Button(text = "Done", command = lambda i=todo.todo_number: self.update(i), anchor = W)
            button.configure(width = 10, activebackground = "#33B5E5", relief = FLAT)
            button_window = self.canvas.create_window(650, (i*30)+200, anchor=NW, window=button)
            button = Button(text = "Delete", command = lambda i=todo.todo_number: self.delete(i), anchor = W)
            button.configure(width = 10, activebackground = "#33B5E5", relief = FLAT)
            button_window = self.canvas.create_window(700, (i*30)+200, anchor=NW, window=button)
        

    def delete(self, i):
        try:
            with self.connection as con:
                cur = con.cursor()
                cur.execute("DELETE from todo WHERE todo_number = ?",(i,))
        except IOError:
            print("Unable to open database")
        self.todos = []
        self.canvas.delete("all")
        self.read_file()
        self.draw()

    def update(self,i):
        try:
            with self.connection as con:
                cur = con.cursor()
                print(i)
                cur.execute("UPDATE todo SET todo_status = 0 WHERE todo_number = ?",(i,))
        except IOError:
            print("Unable to open database")
        self.todos = []
        self.canvas.delete("all")
        self.read_file()
        self.draw()
        
        
            

    