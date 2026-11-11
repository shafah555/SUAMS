import tkinter as tk
from tkinter import ttk, messagebox
from demo_data import MARKS, STUDENTS, COURSES
from core import calculate_result

class ResultPage(ttk.Frame):
    def __init__(self,parent,user):
        super().__init__(parent,padding=18); self.user=user
        ttk.Label(self,text="Continuous Assessment & Results",font=("Segoe UI",18,"bold"),foreground="#164f91").pack(anchor="w",pady=(0,12))
        form=ttk.LabelFrame(self,text="Enter marks (maximum: 10, 10, 10, 30, 40)",padding=12); form.pack(anchor="w",fill="x")
        self.fields={}
        for i,key in enumerate(["assignment","class_test","attendance","midterm","final"]):
            ttk.Label(form,text=key.replace("_"," ").title()).grid(row=i//3,column=(i%3)*2,padx=5,pady=7,sticky="w")
            ent=ttk.Entry(form,width=8); ent.grid(row=i//3,column=(i%3)*2+1,padx=5,pady=7); self.fields[key]=ent
        ttk.Button(self,text="Calculate result",command=self.calculate).pack(anchor="w",pady=10)
        self.output=ttk.Label(self,text="Enter marks to calculate total, grade and GPA.",font=("Segoe UI",12)); self.output.pack(anchor="w")
        ttk.Label(self,text="Saved sample results",font=("Segoe UI",13,"bold")).pack(anchor="w",pady=(20,5))
        self.tree=ttk.Treeview(self,columns=("student","course","total","grade","gpa"),show="headings",height=7)
        for c in ("student","course","total","grade","gpa"): self.tree.heading(c,text=c.title())
        self.tree.pack(fill="x")
        for sid, courses in MARKS.items():
            for code, marks in courses.items():
                try:
                    r=calculate_result(marks); self.tree.insert("","end",values=(sid,code,r["total"],r["grade"],r["gpa"]))
                except ValueError: pass
    def calculate(self):
        try:
            marks={k:float(v.get()) for k,v in self.fields.items()}
            r=calculate_result(marks)
            self.output.config(text=f'Total: {r["total"]}/100     Grade: {r["grade"]}     GPA: {r["gpa"]:.2f}     Status: {r["status"]}')
        except ValueError as e: messagebox.showerror("Invalid marks",str(e))
