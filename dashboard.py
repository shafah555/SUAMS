import tkinter as tk
from tkinter import ttk, messagebox
from demo_data import STUDENTS, TEACHERS, COURSES, SEMESTERS, NOTIFICATIONS
from base_page import TablePage
from admission import AdmissionPage
from course_registration import CourseRegistrationPage
from semester_enrollment import SemesterEnrollmentPage
from examination import ExaminationPage
from result_processing import ResultPage
from advising import AdvisingPage
from notifications import NotificationsPage
from analytics import AnalyticsPage

class Dashboard:
    def __init__(self,root,user,on_logout):
        self.root,self.user,self.on_logout=root,user,on_logout
        root.title("SUAMS | Academic Dashboard")
        root.geometry("1180x740"); root.minsize(950,620); root.configure(bg="#edf3fb")
        style=ttk.Style(); style.theme_use("clam")
        style.configure("Treeview",rowheight=28,background="white",fieldbackground="white")
        style.configure("Treeview.Heading",font=("Segoe UI",9,"bold"))
        style.configure("TButton",padding=7)
        shell=ttk.Frame(root); shell.pack(fill="both",expand=True)
        side=tk.Frame(shell,bg="#153f75",width=220); side.pack(side="left",fill="y"); side.pack_propagate(False)
        tk.Label(side,text="SUAMS",font=("Segoe UI",22,"bold"),fg="white",bg="#153f75").pack(pady=(24,2))
        tk.Label(side,text="Academic Management",font=("Segoe UI",9),fg="#d9e8ff",bg="#153f75").pack(pady=(0,20))
        self.content=ttk.Frame(shell); self.content.pack(side="right",fill="both",expand=True)
        header=ttk.Frame(self.content,padding=(18,12)); header.pack(fill="x")
        ttk.Label(header,text=f'{user["name"]}  |  {user["role"]}',font=("Segoe UI",11,"bold")).pack(side="left")
        ttk.Button(header,text="Log out",command=on_logout).pack(side="right")
        self.body=ttk.Frame(self.content); self.body.pack(fill="both",expand=True)
        self.nav_items=self.permissions(user["role"])
        for label,key in self.nav_items:
            tk.Button(side,text=label,anchor="w",font=("Segoe UI",10),fg="white",bg="#153f75",
                      activebackground="#2865a9",activeforeground="white",relief="flat",
                      command=lambda k=key:self.show(k)).pack(fill="x",ipady=8,padx=10)
        self.show("home")
    def permissions(self,role):
        common=[("Dashboard","home"),("Notifications","notifications")]
        mapping={
          "Student":common+[("Admission","admission"),("Course Registration","courses"),("Semester Enrollment","semester"),("Examination","examination"),("Results","results"),("Advising","advising"),("Analytics","analytics")],
          "Teacher":common+[("Students","students"),("Courses","courses_admin"),("Results / Marks","results"),("Advising","advising"),("Analytics","analytics")],
          "Administrator":common+[("Students","students"),("Teachers","teachers"),("Courses","courses_admin"),("Semesters","semesters"),("Admissions","admission"),("Advising","advising"),("Analytics","analytics")],
          "Examination Controller":common+[("Examination Forms & Routine","examination"),("Results Processing","results"),("Analytics","analytics")]
        }
        return mapping[role]
    def show(self,key):
        for w in self.body.winfo_children(): w.destroy()
        if key=="home":
            frame=ttk.Frame(self.body,padding=24); frame.pack(fill="both",expand=True)
            ttk.Label(frame,text="Welcome to SUAMS",font=("Segoe UI",22,"bold"),foreground="#164f91").pack(anchor="w",pady=(0,5))
            ttk.Label(frame,text="A simple academic management dashboard for university activities.").pack(anchor="w",pady=(0,20))
            cards=ttk.Frame(frame); cards.pack(fill="x")
            values=[("Students",len(STUDENTS)),("Teachers",len(TEACHERS)),("Courses",len(COURSES)),("Semesters",len(SEMESTERS))]
            for title,value in values:
                card=ttk.LabelFrame(cards,text=title,padding=20); card.pack(side="left",fill="x",expand=True,padx=5)
                ttk.Label(card,text=str(value),font=("Segoe UI",22,"bold"),foreground="#1555a5").pack()
            ttk.Label(frame,text=f'Logged in as {self.user["role"]}. Use the left menu to open an allowed module.',font=("Segoe UI",11)).pack(anchor="w",pady=25)
            return
        if key=="students": page=TablePage(self.body,"Student Management",("id","name","email","department","previous_result"),STUDENTS,self.user["role"]=="Administrator")
        elif key=="teachers": page=TablePage(self.body,"Teacher Management",("id","name","department","email"),TEACHERS,True)
        elif key=="courses_admin": page=TablePage(self.body,"Course Management",("code","name","credit","teacher"),COURSES,self.user["role"]=="Administrator")
        elif key=="semesters": page=TablePage(self.body,"Semester Management",("semester",),[{"semester":s} for s in SEMESTERS],True)
        elif key=="admission": page=AdmissionPage(self.body,self.user)
        elif key=="courses": page=CourseRegistrationPage(self.body,self.user)
        elif key=="semester": page=SemesterEnrollmentPage(self.body,self.user)
        elif key=="examination": page=ExaminationPage(self.body,self.user)
        elif key=="results": page=ResultPage(self.body,self.user)
        elif key=="advising": page=AdvisingPage(self.body,self.user)
        elif key=="notifications": page=NotificationsPage(self.body,self.user)
        elif key=="analytics": page=AnalyticsPage(self.body,self.user)
        else:
            ttk.Label(self.body,text="Module unavailable",padding=20).pack()
            return
        page.pack(fill="both",expand=True)
