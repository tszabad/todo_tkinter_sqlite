from tkinter import *

class Todo():
    def __init__(self):
        self.todos = []

    def add_todo(self, todo):
        self.todos.append(todo)

    def draw(self, canvas):
        canvas.create_rectangle(0, 0, 600, 30, fill = "grey")
        for todo in self.todos:
            #text = f"Hero (Level: {hero.level}) HP: {int(hero.HP)}/38 | DP: {hero.DP} | SP: {hero.SP}"
            #canvas_text = canvas2.create_text(10, 10, text=text, font=('freemono bold',11),anchor=NW)
            

    