
import sqlite3

from todo_list import Todo_list
from todo import Todo


def main():
    connection = sqlite3.connect("data.db")
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE if not exists todo (todo_number INTEGER, todo_status INTEGER, todo_text TEXT)")
    todo_list = Todo_list()
    todo_list.canvas.pack()
    todo_list.root.mainloop()

if __name__ == '__main__':
    main()