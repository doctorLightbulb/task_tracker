import tkinter as tk
from tkinter import ttk

from task_tracker.helpers import timestamp


class StatisticsWindow(tk.Toplevel):
    def __init__(self, root: tk.Tk, data, coords):
        super().__init__(root)
        self.root = root
        self.data = data
        self.title("Statistics")
        self.coords = coords

        x, y = self.coords
        self.geometry(f"400x300+{x}+{y}")

        self._initialize_window()

    def _initialize_window(self):
        """Creates the window widgets."""
        self.notebook = ttk.Notebook(self)

        # Notebook screens:
        self.daily_time_per_task = ttk.Frame(self.notebook)
        self.weekly_time_per_task = ttk.Frame(self.notebook)
        self.total_time_per_task = ttk.Frame(self.notebook)

        # Add contents:
        self.add_table(self.total_time_per_task, self.data["total"])

        if "daily" in self.data.keys():
            self.add_table(self.daily_time_per_task, self.data["daily"])
        else:
            self.add_table(self.daily_time_per_task, {"No Task Today": 0})

        # Add screens to the notebook:
        self.notebook.add(self.daily_time_per_task, text="Daily")
        self.notebook.add(self.weekly_time_per_task, text="Weekly")
        self.notebook.add(self.total_time_per_task, text="Total")
        self.notebook.pack(expand=True, fill=tk.BOTH)

    def add_table(self, parent, data):
        """
        Dynamically populates the widgets based on the number of tasks
        in `self.data`.
        """
        # Top label
        screen_label = tk.Label(
            parent,
            text="Time Spent per Task",
            font=("Times New Roman", 14, "bold"),
            bg="gray",
            fg="white",
        )
        screen_label.pack(side=tk.TOP, fill=tk.X, expand=True)

        frame = tk.Frame(parent)
        frame.pack(
            side=tk.BOTTOM,
            fill=tk.X,
            expand=True,
            ipadx=10,
            ipady=10,
        )

        # Table
        treeview = ttk.Treeview(frame, columns=("Total"))
        treeview.heading(
            "#0",
            text="Task",
            command=lambda: sort_column(treeview, "", False),
        )
        treeview.heading(
            "Total",
            text="Time",
            command=lambda: sort_column(treeview, "Total", False),
        )

        # Row tags:
        treeview.tag_configure(
            "end_row",
            background="darkgray",
            foreground="white",
            font=("TkDefaultFont", 10, "bold"),
        )

        # Row creation:
        total_time = 0
        for task in data.keys():
            total_time += data[task]

            treeview.insert(
                "",
                tk.END,
                text=task,
                values=(timestamp(data[task]),),
            )

        # Total footer:
        total_footer = ttk.Frame(frame)
        total_label = tk.Label(total_footer, text="Total")
        totalled_time = tk.Label(total_footer, text=f"{timestamp(total_time)}")

        # Widget constraints and packing:
        treeview.column("#0", width=250)
        treeview.column("#1", width=25, anchor="e")
        treeview.pack(fill=tk.BOTH, expand=True)

        total_label.pack(side=tk.LEFT, padx=5)
        totalled_time.pack(side=tk.RIGHT, padx=5)
        total_footer.pack(fill=tk.X, expand=True)


def sort_column(tv, col, reverse):
    # Source:
    # https://stackoverflow.com/questions/1966929/tk-treeview-column-sort#1967793

    # Duplicate and sort the data:
    l = [(tv.set(k, col), k) for k in tv.get_children("")]
    l.sort(reverse=reverse)

    # Update items positions in the TreeView:
    for index, (val, k) in enumerate(l):
        tv.move(k, "", index)

    # Reverse sort next time:
    tv.heading(col, command=lambda: sort_column(tv, col, not reverse))
