from tkinter import ttk, messagebox
from base_page import TablePage
from demo_data import ADMISSIONS, STUDENTS

class AdmissionPage(TablePage):
    def __init__(self,parent,user):
        cols=("application_id","name","student_id","email","department","previous_result","status")
        super().__init__(parent,"Admission Applications",cols,ADMISSIONS,user["role"]=="Administrator",cols)
        if user["role"]=="Administrator":
            ttk.Button(self,text="Approve selected",command=self.approve).pack(anchor="w",pady=4)
            ttk.Button(self,text="Reject selected",command=self.reject).pack(anchor="w",pady=4)
    def approve(self):
        i=self.selected()
        if i is not None:
            row=self.rows[i]; row["status"]="Approved"
            if not any(s["id"]==row["student_id"] for s in STUDENTS):
                STUDENTS.append({"id":row["student_id"],"name":row["name"],"email":row["email"],"department":row["department"],"previous_result":row["previous_result"]})
            self.refresh(); messagebox.showinfo("Admission","Application approved and student added.")
    def reject(self):
        i=self.selected()
        if i is not None: self.rows[i]["status"]="Rejected"; self.refresh()
