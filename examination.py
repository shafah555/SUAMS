import tkinter as tk
from tkinter import ttk, messagebox
from demo_data import EXAM_FORMS, SEMESTERS, ROUTINE
from core import submit_exam_form, generate_routine

class ExaminationPage(ttk.Frame):
    def __init__(self,parent,user):
        super().__init__(parent,padding=18); self.user=user
        ttk.Label(self,text="Examination Management",font=("Segoe UI",18,"bold"),foreground="#164f91").pack(anchor="w",pady=(0,10))
        if user["role"]=="Student":
            self.sem=tk.StringVar(value=SEMESTERS[0])
            ttk.Combobox(self,textvariable=self.sem,values=SEMESTERS,state="readonly",width=35).pack(anchor="w",pady=5)
            ttk.Button(self,text="Submit examination form",command=self.submit).pack(anchor="w",pady=5)
        if user["role"]=="Examination Controller":
            ttk.Button(self,text="Approve selected form",command=self.approve).pack(anchor="w",pady=5)
            ttk.Button(self,text="Generate examination routine",command=self.generate).pack(anchor="w",pady=5)
            ttk.Button(self,text="Publish routine",command=lambda:messagebox.showinfo("Published","The generated routine is now marked as published.")).pack(anchor="w",pady=5)
        ttk.Label(self,text="Examination forms",font=("Segoe UI",13,"bold")).pack(anchor="w",pady=(12,5))
        self.tree=ttk.Treeview(self,columns=("form_id","student_id","semester","status"),show="headings",height=6)
        for c in ("form_id","student_id","semester","status"): self.tree.heading(c,text=c.replace("_"," ").title())
        self.tree.pack(fill="x"); self.refresh()
        ttk.Label(self,text="Examination routine",font=("Segoe UI",13,"bold")).pack(anchor="w",pady=(16,5))
        self.rtree=ttk.Treeview(self,columns=("date","time","course","room"),show="headings",height=7)
        for c in ("date","time","course","room"): self.rtree.heading(c,text=c.title())
        self.rtree.pack(fill="x"); self.refresh_routine()
    def refresh(self):
        self.tree.delete(*self.tree.get_children())
        for f in EXAM_FORMS:
            if self.user["role"]!="Student" or f["student_id"]==self.user.get("student_id"):
                self.tree.insert("","end",iid=f["form_id"],values=tuple(f[k] for k in ("form_id","student_id","semester","status")))
    def refresh_routine(self):
        self.rtree.delete(*self.rtree.get_children())
        for r in ROUTINE: self.rtree.insert("","end",values=tuple(r[k] for k in ("date","time","course","room")))
    def submit(self):
        try: submit_exam_form(self.user.get("student_id","S-1001"),self.sem.get()); self.refresh(); messagebox.showinfo("Submitted","Examination form submitted.")
        except ValueError as e: messagebox.showerror("Cannot submit",str(e))
    def approve(self):
        sel=self.tree.selection()
        if not sel: messagebox.showwarning("Select form","Select an examination form."); return
        for f in EXAM_FORMS:
            if f["form_id"]==sel[0]: f["status"]="Approved"
        self.refresh(); messagebox.showinfo("Approved","Examination form approved.")
    def generate(self):
        generate_routine(); self.refresh_routine(); messagebox.showinfo("Generated","Examination routine generated.")
