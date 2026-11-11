import tkinter as tk
from tkinter import ttk, messagebox
from demo_data import COURSES, REGISTRATIONS
from core import register_courses

class CourseRegistrationPage(ttk.Frame):
    def __init__(self, parent, user):
        super().__init__(parent, padding=18); self.user=user
        ttk.Label(self,text="Course Registration",font=("Segoe UI",18,"bold"),foreground="#164f91").pack(anchor="w",pady=(0,10))
        ttk.Label(self,text="Select courses. The maximum allowed credit is 18. Already registered courses cannot be selected again.").pack(anchor="w")
        self.vars={}
        self.wrap=ttk.Frame(self); self.wrap.pack(fill="both",expand=True,pady=12)
        self.refresh_courses()
        self.total=ttk.Label(self,text="Selected credits: 0"); self.total.pack(anchor="w",pady=8)
        ttk.Button(self,text="Calculate credits",command=self.calculate).pack(anchor="w",pady=3)
        ttk.Button(self,text="Submit registration",command=self.submit).pack(anchor="w",pady=3)
        self.calculate()
    def refresh_courses(self):
        for widget in self.wrap.winfo_children():
            widget.destroy()
        self.vars={}
        registered=set(REGISTRATIONS.get(self.user.get("student_id","S-1001"),[]))
        for c in COURSES:
            already_registered=c["code"] in registered
            v=tk.BooleanVar(value=already_registered)
            self.vars[c["code"]]=v
            ttk.Checkbutton(
                self.wrap,
                text=f'{c["code"]}  |  {c["name"]}  |  {c["credit"]} credits  |  {c["teacher"]}',
                variable=v,
                state="disabled" if already_registered else "normal",
            ).pack(anchor="w",pady=4)
    def selected(self): return [c for c,v in self.vars.items() if v.get()]
    def calculate(self):
        credits=sum(c["credit"] for c in COURSES if c["code"] in self.selected())
        self.total.config(text=f"Selected credits: {credits} / 18")
    def submit(self):
        try:
            student_id=self.user.get("student_id","S-1001")
            registered=set(REGISTRATIONS.get(student_id,[]))
            new_courses=[code for code in self.selected() if code not in registered]
            credits=register_courses(student_id,new_courses)
            self.refresh_courses()
            self.total.config(text=f"Registration saved successfully. Total credits: {credits}")
            messagebox.showinfo("Success",f"Course registration completed ({credits} credits).")
        except ValueError as e: messagebox.showerror("Registration error",str(e))
