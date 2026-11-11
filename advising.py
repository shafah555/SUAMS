from tkinter import ttk, messagebox
from base_page import TablePage
from demo_data import ADVISING

class AdvisingPage(TablePage):
    def __init__(self,parent,user):
        cols=("request_id","student_id","topic","comment","status")
        super().__init__(parent,"Teacher-Student Advising",cols,ADVISING,user["role"] in ("Teacher","Student"),cols)
        ttk.Button(self,text="Add comment / close request",command=self.comment).pack(anchor="w",pady=5)
    def comment(self):
        i=self.selected()
        if i is None:return
        win=__import__("tkinter").Toplevel(self); win.title("Advising comment")
        ent=__import__("tkinter").Entry(win,width=50); ent.pack(padx=12,pady=12)
        def save():
            self.rows[i]["comment"]=ent.get().strip()
            self.rows[i]["status"]="Closed" if self.rows[i]["comment"] else "Open"
            self.refresh(); win.destroy()
        ttk.Button(win,text="Save",command=save).pack(pady=8)
