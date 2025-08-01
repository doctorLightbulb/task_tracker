import tkinter as tk
from tkinter import ttk


class StatisticsWindow(tk.Toplevel):
    def __init__(self, root: tk.Tk):
        super().__init__(root)
        self.root = root
        self.title("Statistics")

        self.initialize_window()

    def initialize_window(self):
        frame = ttk.Frame(self.root)

        treeview = ttk.Treeview(
            frame,
            columns=("Started", "Stopped", "Total"),
        )
        treeview.heading("#0", text="Date")
        treeview.heading("Started", text="Started")
        treeview.heading("Stopped", text="Stopped")
        treeview.heading("Total", text="Total")

        tasks = [
            "Financial Accounting I",
            "Teachings and Doctrine of the Book of Mormon",
        ]
        entries = [000, 000, 000, 000]
        for task in tasks:
            level_1 = treeview.insert(
                "",
                tk.END,
                text=task,
            )
            for entry in entries:
                treeview.insert(
                    level_1,
                    tk.END,
                    text=task,
                    values=(entry, entry),
                )

        v_scrollbar = ttk.Scrollbar(
            frame,
            orient=tk.VERTICAL,
            command=treeview.yview,
        )
        treeview.configure(yscrollcommand=v_scrollbar.set)

        treeview.pack(
            padx=10,
            pady=20,
            side=tk.LEFT,
            fill=tk.BOTH,
            expand=True,
        )
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        frame.pack(fill=tk.BOTH)

    def load_fields(self):
        pass
