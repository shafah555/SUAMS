from tkinter import ttk
from demo_data import MARKS, STUDENTS, COURSES
from core import calculate_result

class AnalyticsPage(ttk.Frame):
    def __init__(self,parent,user):
        super().__init__(parent,padding=18)
        ttk.Label(self,text="Student Performance Analytics",font=("Segoe UI",18,"bold"),foreground="#164f91").pack(anchor="w",pady=(0,12))
        totals=[]
        for sid,courses in MARKS.items():
            for code,marks in courses.items():
                try: totals.append((sid,code,calculate_result(marks)))
                except ValueError: pass
        avg=sum(x[2]["gpa"] for x in totals)/len(totals) if totals else 0
        ttk.Label(self,text=f"Recorded course results: {len(totals)}     Average GPA: {avg:.2f}",font=("Segoe UI",12)).pack(anchor="w",pady=6)
        self.tree=ttk.Treeview(self,columns=("student","course","total","grade","gpa","attendance"),show="headings",height=12)
        for c in ("student","course","total","grade","gpa","attendance"): self.tree.heading(c,text=c.title())
        self.tree.pack(fill="both",expand=True)
        for sid,code,r in totals:
            att=MARKS[sid][code]["attendance"]*10
            self.tree.insert("","end",values=(sid,code,r["total"],r["grade"],r["gpa"],f"{att}%"))
        try:
            import matplotlib
            matplotlib.use("TkAgg")
            from matplotlib.figure import Figure
            from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
            fig=Figure(figsize=(5,2.2),dpi=90); ax=fig.add_subplot(111)
            ax.bar([x[1] for x in totals],[x[2]["total"] for x in totals]); ax.set_ylabel("Total marks"); ax.set_title("Course-wise performance")
            canvas=FigureCanvasTkAgg(fig,master=self); canvas.draw(); canvas.get_tk_widget().pack(fill="x",pady=8)
        except Exception:
            ttk.Label(self,text="Optional chart unavailable. Install matplotlib to display the chart.",foreground="#68778a").pack(anchor="w",pady=8)
