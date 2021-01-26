from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sqlite3

from todo_list import Todo_list
from todo import Todo


def main():
    connection = sqlite3.connect("data.db")
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE if not exists todo (todo_number INTEGER, todo_status INTEGER, todo_text TEXT)")

    root = Tk()
    root.title("Tom's todo App")
    canvas = Canvas(root, width=800, height=800)    

    todo_list = Todo_list()

    entry1 = ttk.Entry(root)
    label1 = ttk.Label(root, text = '< Name of the label >')


    def write_file():
        todo = e1.get()
        status = 1
        if len(todo)==0:
            messagebox.showinfo('Empty Entry', 'Enter task name')
        try:
            with connection as con:
                cur = con.cursor()
                last = cur.execute("SELECT todo_number FROM todo ORDER BY todo_number DESC LIMIT 1").fetchone()
                if last is None:
                    number = 1
                else:
                    number = last[0] + 1
                cur.execute("INSERT INTO todo VALUES (?, ?, ?);", (number, status, todo))
        except IOError:
            print("Unable to open database")
        e1.delete(0,'end')
        listUpdate()
    
    def listUpdate():
        todo_list.del_todos()
        draw_canvas()

    def read_file():
        done = "[x]"
        undone = "[ ]"
        try:
            with connection as con:
                cur = con.cursor()
                rows = cur.execute("SELECT todo_number, todo_status, todo_text FROM todo").fetchall()
                print(rows)
                for i in rows:
                    if len(rows) > 0:
                        symbol = undone if i[1] == 1 else done
                        todo = Todo(i[0], symbol, i[2])
                        todo_list.add_todo(todo)
        except IOError:
            print("Unable to open database")

    def bye():
        root.destroy()
    
    def delete_all():
        try:
            with connection as con:
                cur = con.cursor()
                cur.execute("DELETE from todo")
        except IOError:
            print("Unable to open database")
        canvas.delete('all')
        listUpdate()


    l1 = ttk.Label(root, text = 'To-Do List', font=('freemono bold',20),anchor=NW)
    l2 = ttk.Label(root, text='Enter task title: ')
    e1 = ttk.Entry(root, width=51)
    b1 = ttk.Button(root, text='Add task', width=50, command=write_file)
    b3 = ttk.Button(root, text='Delete all', width=50, command=delete_all)
    b4 = ttk.Button(root, text='Exit', width=50, command=bye)


    def draw_canvas():
        read_file()
        todo_list.draw(canvas)

    draw_canvas()

    canvas.pack()
    l2.place(x=80, y=50)
    e1.place(x=80, y=80)
    b1.place(x=80, y=110)
    b3.place(x=80, y=170)
    b4.place(x=80, y =200)
    l1.place(x=80, y=10)
    root.mainloop()
    


if __name__ == '__main__':
    main()