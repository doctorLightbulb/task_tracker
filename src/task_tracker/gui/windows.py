import tkinter as tk
from tkinter import ttk

from task_tracker.helpers import timestamp


class StatisticsWindow(tk.Toplevel):
    def __init__(self, root: tk.Tk, data):
        super().__init__(root)
        self.root = root
        self.data = data
        self.title("Statistics")

        self._initialize_window()

    def _initialize_window(self):
        """Creates the window widgets."""
        screen_label = tk.Label(
            self,
            text="Time Spent per Task",
            font=("Times New Roman", 14, "bold"),
            bg="gray",
            fg="white",
        )
        screen_label.pack(side=tk.TOP, fill=tk.X, expand=True)

        self.frame = tk.Frame(self)
        self.frame.pack(
            side=tk.BOTTOM,
            fill=tk.BOTH,
            expand=True,
            ipadx=10,
            ipady=10,
        )

        self.load_fields()

    def load_fields(self):
        """
        Dynamically populates the widgets based on the number of tasks
        in `self.data`.
        """
        treeview = ttk.Treeview(self.frame, columns=("Total"))
        treeview.heading("#0", text="Task")
        treeview.heading("Total", text="Time")

        for task in self.data.keys():
            treeview.insert(
                "",
                tk.END,
                text=task,
                values=(timestamp(self.data[task]),),
            )

        treeview.columnconfigure(0, weight=2)
        treeview.columnconfigure(1, weight=0)
        treeview.pack(fill=tk.BOTH, expand=True)
