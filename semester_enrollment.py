import tkinter as tk
from tkinter import ttk, messagebox
from demo_data import SEMESTERS, ENROLLMENTS
from core import enroll_semester

class SemesterEnrollmentPage(ttk.Frame):
    def __init__(self,parent,user):
        super().__init__(parent,padding=18); self.user=user
        ttk.Label(self,text="Semester Enrollment",font=("Segoe UI",18,"bold"),foreground="#164f91").pack(anchor="w",pady=(0,12))
        self.sem=tk.StringVar(value=SEMESTERS[0])
        ttk.Label(self,text="Select semester").pack(anchor="w")
        ttk.Combobox(self,textvariable=self.sem,values=SEMESTERS,state="readonly",width=35).pack(anchor="w",pady=8)
        ttk.Button(self,text="Enroll",command=self.enroll).pack(anchor="w")
        ttk.Label(self,text="Enrollment records",font=("Segoe UI",13,"bold")).pack(anchor="w",pady=(20,5))
        self.tree=ttk.Treeview(self,columns=("student_id","semester","status"),show="headings")
        for c in ("student_id","semester","status"): self.tree.heading(c,text=c.replace("_"," ").title())
        self.tree.pack(fill="x"); self.refresh()
    def refresh(self):
        self.tree.delete(*self.tree.get_children())
        for e in ENROLLMENTS:
            if e["student_id"]==self.user.get("student_id","S-1001") or self.user["role"]=="Administrator":
                self.tree.insert("","end",values=tuple(e[k] for k in ("student_id","semester","status")))
    def enroll(self):
        try:
            enroll_semester(self.user.get("student_id","S-1001"),self.sem.get()); self.refresh()
            messagebox.showinfo("Success","Semester enrollment completed.")
        except ValueError as e: messagebox.showerror("Enrollment error",str(e))
