import tkinter as tk
from tkinter import ttk, messagebox
from demo_data import NOTIFICATIONS
from core import publish_notification, NOTIFICATION_SERVICE

class NotificationsPage(ttk.Frame):
    def __init__(self,parent,user):
        super().__init__(parent,padding=18); self.user=user
        ttk.Label(self,text="Academic Notifications",font=("Segoe UI",18,"bold"),foreground="#164f91").pack(anchor="w",pady=(0,12))
        if user["role"]=="Administrator":
            form=ttk.LabelFrame(self,text="Publish new notification",padding=10); form.pack(fill="x",pady=(0,12))
            self.title=ttk.Entry(form); self.title.pack(fill="x",pady=4); self.title.insert(0,"Notification title")
            self.message=tk.Text(form,height=3); self.message.pack(fill="x",pady=4)
            self.audience=tk.StringVar(value="All")
            ttk.Combobox(form,textvariable=self.audience,values=["All","Students","Teachers"],state="readonly").pack(anchor="w")
            ttk.Button(form,text="Publish",command=self.publish).pack(anchor="w",pady=5)
        self.tree=ttk.Treeview(self,columns=("date","title","message","audience"),show="headings",height=14)
        for c in ("date","title","message","audience"): self.tree.heading(c,text=c.title()); self.tree.column(c,width=180)
        self.tree.pack(fill="both",expand=True); self.refresh()
        NOTIFICATION_SERVICE.subscribe(lambda _n:self.refresh())
    def refresh(self):
        self.tree.delete(*self.tree.get_children())
        for n in NOTIFICATIONS:
            if n["audience"]=="All" or n["audience"]==self.user["role"]+"s":
                self.tree.insert("","end",values=tuple(n.get(k,"") for k in ("date","title","message","audience")))
    def publish(self):
        try:
            publish_notification(self.title.get(),self.message.get("1.0","end").strip(),self.audience.get())
            self.refresh(); messagebox.showinfo("Published","Notification published to the selected audience.")
            self.title.delete(0,"end"); self.message.delete("1.0","end")
        except ValueError as e: messagebox.showerror("Invalid notification",str(e))
