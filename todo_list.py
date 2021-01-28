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
        l3 = ttk.Label(self.root, text = "These are your todos so far:",font=('Arial',15),anchor=NW)
        self.e1 = ttk.Entry(self.root, width=80)
        b1 = ttk.Button(self.root, text='Add task', width=50, command=self.write_file)
        b3 = ttk.Button(self.root, text='Delete all', width=50, command=self.delete_all)
        b4 = ttk.Button(self.root, text='Exit', width=50, command=self.bye)
        l2.place(x=80, y=50)
        l3.place(x=80, y=200)
        self.e1.place(x=80, y=80)
        b1.place(x=80, y=110)
        b3.place(x=80, y=140)
        b4.place(x=400, y =140)
        l1.place(x=80, y=10)
        self.read_file()
        self.draw()
        self.root.bind_all('<Key>', self.on_key_press)
        

    def on_key_press(self,e):
        if e.keycode == 27:               
            self.root.destroy()
        elif e.keycode == 13:
            self.write_file()

        
    def write_file(self):
        todo = self.e1.get()
        status = 0
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
        try:
            with self.connection as con:
                cur = con.cursor()
                rows = cur.execute("SELECT todo_number, todo_status, todo_text FROM todo").fetchall()
                for i in rows:
                    if len(rows) > 0:
                        todo = Todo(i[0], i[1], i[2])
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
            btnname = "To Progress" if todo.todo_status == 0 else "To Done" if todo.todo_status == 1 else "Ready"
            text1 = "OPEN" if todo.todo_status == 0 else "IN PROGRESS" if todo.todo_status == 1 else "READY"
            text = f"No.:{todo.todo_number} | Status: {text1} | Todo: {todo.todo_text}"
            canvas_text = self.canvas.create_text((80, (i*30)+250), text=text, font=('Arial',11),anchor=NW)
            button = Button(text = btnname, command = lambda i = todo.todo_number, j = todo.todo_status: self.update(i,j), anchor = W)
            button.configure(width = 10, activebackground = "#33B5E5", relief = FLAT)
            button_window = self.canvas.create_window(620, (i*30)+250, anchor=NW, window=button)
            button = Button(text = "Delete", command = lambda i=todo.todo_number, j = todo.todo_status: self.delete(i,j), anchor = W)
            button.configure(width = 10, activebackground = "#33B5E5", relief = FLAT)
            button_window = self.canvas.create_window(700, (i*30)+250, anchor=NW, window=button)
        

    def delete(self, i,j):
        if j < 2:
            messagebox.showinfo('Todo not ready', 'Only ready todo can be deleted')
        else:
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

    def update(self,i,j):
        try:
            with self.connection as con:
                cur = con.cursor()
                cur.execute("UPDATE todo SET todo_status = ? WHERE todo_number = ?",(j+1, i,))
        except IOError:
            print("Unable to open database")
        self.todos = []
        self.canvas.delete("all")
        self.read_file()
        self.draw()
        
        
            

    