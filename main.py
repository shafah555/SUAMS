"""Entry point for Smart University Academic Management System."""
import tkinter as tk
from login import LoginWindow
from dashboard import Dashboard

class SUAMS:
    def __init__(self):
        self.root=tk.Tk()
        self.show_login()
        self.root.mainloop()
    def clear(self):
        for widget in self.root.winfo_children(): widget.destroy()
    def show_login(self):
        self.clear()
        LoginWindow(self.root,self.open_dashboard)
    def open_dashboard(self,user):
        self.clear()
        Dashboard(self.root,user,self.show_login)

if __name__=="__main__":
    SUAMS()
