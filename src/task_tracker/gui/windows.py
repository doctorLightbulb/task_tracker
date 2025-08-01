import tkinter as tk
from tkinter import ttk


class StatisticsWindow(tk.Toplevel):
    def __init__(self, root: tk.Tk, data):
        super().__init__(root)
        self.root = root
        self.data = data
        self.title("Statistics")

        self.initialize_window()

    def initialize_window(self):
        """Create the window widgets."""
        screen_label = tk.Label(
            self,
            text="Time Spent per Task",
            font=("Times New Roman", 14, "bold"),
            bg="gray",
            fg="white",
        )
        screen_label.pack(side=tk.TOP, fill=tk.X, expand=True)

        label_frame = tk.Frame(self, bg="white", padx=20)
        label_frame.pack(fill=tk.BOTH, expand=True)

        task_label = tk.Label(label_frame, text="TASK", bg="white")
        task_label.pack(side=tk.LEFT)

        time_label = tk.Label(label_frame, text="TIME", bg="white")
        time_label.pack(side=tk.RIGHT)

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
        """Dynamically populate the widgets based on the number of tasks
        in `self.data`.
        """
        time_font = ("Times New Roman", 12, "bold")
        task_font = ("Times New Roman", 12)
        for index, task in enumerate(self.data.keys()):
            task_label = tk.Label(
                self.frame,
                text=task,
                justify=tk.LEFT,
                font=task_font,
            )
            time_label = tk.Label(
                self.frame,
                text=str(timestamp(self.data[task])),
                font=time_font,
            )
            task_label.grid(column=0, row=index + 1)
            time_label.grid(column=1, row=index + 1)
            self.frame.grid_rowconfigure(index + 1, weight=2)
            self.frame.grid_rowconfigure(index + 2, weight=1)


def timestamp(seconds: int | float) -> str:
    """Take seconds in the form `18221.51687` and return a value
    of the form `05:03:42`.
    """
    (hours, seconds) = divmod(seconds, 3600)
    (minutes, seconds) = divmod(seconds, 60)
    return f"{hours:02.0f}:{minutes:02.0f}:{seconds:02.0f}"
