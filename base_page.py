import tkinter as tk
from tkinter import ttk, messagebox

class TablePage(ttk.Frame):
    """Reusable table with validated Add, Edit, Delete and View actions."""
    def __init__(self, parent, title, columns, rows, can_edit=True, form_fields=None, on_change=None):
        super().__init__(parent, padding=18)
        self.title_text, self.columns, self.rows = title, columns, rows
        self.can_edit, self.form_fields, self.on_change = can_edit, form_fields or columns, on_change
        ttk.Label(self, text=title, font=("Segoe UI", 18, "bold"), foreground="#164f91").pack(anchor="w", pady=(0,12))
        bar = ttk.Frame(self); bar.pack(fill="x", pady=(0,10))
        self.search = ttk.Entry(bar); self.search.pack(side="left", fill="x", expand=True, padx=(0,8))
        self.search.insert(0, "Search...")
        self.search.bind("<KeyRelease>", lambda _e: self.refresh())
        ttk.Button(bar, text="Search", command=self.refresh).pack(side="left")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=15)
        for c in columns:
            self.tree.heading(c, text=c.replace("_"," ").title())
            self.tree.column(c, width=135, anchor="w")
        self.tree.pack(fill="both", expand=True)
        buttons = ttk.Frame(self); buttons.pack(fill="x", pady=10)
        if can_edit:
            ttk.Button(buttons, text="Add", command=self.add).pack(side="left", padx=3)
            ttk.Button(buttons, text="Edit", command=self.edit).pack(side="left", padx=3)
            ttk.Button(buttons, text="Delete", command=self.delete).pack(side="left", padx=3)
        ttk.Button(buttons, text="View", command=self.view).pack(side="left", padx=3)
        self.refresh()
    def refresh(self):
        self.tree.delete(*self.tree.get_children())
        query = self.search.get().lower()
        if query == "search...": query = ""
        for index, row in enumerate(self.rows):
            vals = [row.get(c, "") for c in self.columns]
            if query and query not in " ".join(map(str, vals)).lower(): continue
            self.tree.insert("", "end", iid=str(index), values=vals)
    def selected(self):
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Select a row", "Please select a row first.")
            return None
        return int(selection[0])
    def form(self, title, initial=None):
        win = tk.Toplevel(self); win.title(title); win.transient(self.winfo_toplevel()); win.grab_set()
        entries = {}
        for i, field in enumerate(self.form_fields):
            ttk.Label(win, text=field.replace("_"," ").title()).grid(row=i, column=0, padx=12, pady=7, sticky="w")
            ent = ttk.Entry(win, width=35); ent.grid(row=i, column=1, padx=12, pady=7)
            if initial: ent.insert(0, str(initial.get(field,"")))
            entries[field] = ent
        def save():
            data = {k:v.get().strip() for k,v in entries.items()}
            if any(not v for v in data.values()):
                messagebox.showerror("Invalid input", "Please complete every field.", parent=win); return
            if initial is None: self.rows.append(data)
            else: self.rows[self.edit_index].update(data)
            self.refresh()
            if self.on_change: self.on_change()
            win.destroy()
        ttk.Button(win, text="Save", command=save).grid(row=len(entries), column=0, columnspan=2, pady=12)
    def add(self): self.form("Add "+self.title_text)
    def edit(self):
        idx = self.selected()
        if idx is not None:
            self.edit_index = idx
            self.form("Edit "+self.title_text, self.rows[idx])
    def delete(self):
        idx = self.selected()
        if idx is not None and messagebox.askyesno("Confirm delete", "Delete selected record?"):
            del self.rows[idx]; self.refresh()
            if self.on_change: self.on_change()
    def view(self):
        idx = self.selected()
        if idx is not None:
            messagebox.showinfo(self.title_text, "\n".join(f"{k}: {v}" for k,v in self.rows[idx].items()))
