from tkinter import *
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


    def write_file(todo):
        status = 1
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

    todo = input("please enter a new todo")
    write_file(todo)

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

    read_file()
    todo_list.draw(canvas)

    canvas.pack()

    root.mainloop()
    


if __name__ == '__main__':
    main()