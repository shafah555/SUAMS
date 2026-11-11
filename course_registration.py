import tkinter as tk
from tkinter import ttk, messagebox
from demo_data import COURSES, REGISTRATIONS
from core import register_courses

class CourseRegistrationPage(ttk.Frame):
    def __init__(self, parent, user):
        super().__init__(parent, padding=18); self.user=user
        ttk.Label(self,text="Course Registration",font=("Segoe UI",18,"bold"),foreground="#164f91").pack(anchor="w",pady=(0,10))
        ttk.Label(self,text="Select courses. The maximum allowed credit is 18.").pack(anchor="w")
        self.vars={}
        wrap=ttk.Frame(self); wrap.pack(fill="both",expand=True,pady=12)
        for c in COURSES:
            v=tk.BooleanVar(value=c["code"] in REGISTRATIONS.get(user.get("student_id","S-1001"),[]))
            self.vars[c["code"]]=v
            ttk.Checkbutton(wrap,text=f'{c["code"]}  |  {c["name"]}  |  {c["credit"]} credits  |  {c["teacher"]}',variable=v).pack(anchor="w",pady=4)
        self.total=ttk.Label(self,text="Selected credits: 0"); self.total.pack(anchor="w",pady=8)
        ttk.Button(self,text="Calculate credits",command=self.calculate).pack(anchor="w",pady=3)
        ttk.Button(self,text="Submit registration",command=self.submit).pack(anchor="w",pady=3)
        self.calculate()
    def selected(self): return [c for c,v in self.vars.items() if v.get()]
    def calculate(self):
        credits=sum(c["credit"] for c in COURSES if c["code"] in self.selected())
        self.total.config(text=f"Selected credits: {credits} / 18")
    def submit(self):
        try:
            credits=register_courses(self.user.get("student_id","S-1001"),self.selected())
            self.total.config(text=f"Registration saved successfully. Total credits: {credits}")
            messagebox.showinfo("Success",f"Course registration completed ({credits} credits).")
        except ValueError as e: messagebox.showerror("Registration error",str(e))
