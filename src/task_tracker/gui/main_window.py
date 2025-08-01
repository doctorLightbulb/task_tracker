"""A module containing the TaskTracker class, the main window to the
application.
"""

import csv
import logging
import tkinter as tk
from datetime import datetime
from tkinter import filedialog, simpledialog, ttk

from task_tracker.database import (
    COMMIT_STATE_QUERY,
    COMMIT_TASK_QUERY,
    FETCH_DATA,
    FETCH_DAYS_TIME,
    FETCH_ELAPSED_TIME,
    FETCH_STATE,
    FETCH_TASK,
    UPDATE_STATE_QUERY,
)
from task_tracker.gui.windows import StatisticsWindow

DEFAULT_TIME = "00:00:00"


logging.basicConfig(level=logging.INFO)


class TaskTracker:
    """The main window to Task Tracker."""

    def __init__(self, root: tk.Tk, database, icons) -> None:

        # Initial values
        self.timer = tk.StringVar(value=DEFAULT_TIME)
        self.button_text = tk.StringVar(value="Start")
        self.task = tk.StringVar(value="")
        self.tasks: set = set()
        self.date = self.get_date()
        self.start_time = None
        self.stop_time = None
        self.elapsed_time = None

        # Application variables
        self.running = False
        self.counter = 0

        # Root definitions
        self.root = root
        self.root.title("Task Tracker")
        self.root.protocol("WM_DELETE_WINDOW", self.exit)

        # Load window's state
        self.db = database
        self.tasks = self.load_existing_task_names()

        logging.info(
            f"Database path {self.db.db_path!r} exists: {self.db.db_path.exists()}"
        )

        # Window size and placement
        window_width = 304
        window_height = 208
        x, y = self.set_window_state(window_width, window_height)
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # Other
        self.icons = icons
        self.task.trace_add(
            "write",
            lambda name, index, mode, task=self.task: self.task_callback(),
        )

        self.bindings()
        self.init_gui()

    def bindings(self):
        """Add bindings to menu items and buttons."""
        self.root.bind("<Alt-i>", self.import_tasks)
        self.root.bind("<Alt-e>", self.export_tasks)
        self.root.bind("<Control-e>", self.edit_entry)
        self.root.bind("<Control-a>", self.add_entry)
        self.root.bind("<Control-d>", self.delete_entry)
        self.root.bind("<Return>", self.execute_timer)
        self.root.bind("<Escape>", self.exit)

    def init_gui(self):
        """Paint the widgets to the window."""

        # Main frame
        self.frame = ttk.Frame(self.root)
        self.frame.pack(fill="both", pady=10, padx=10)

        self.load_window_icons()
        self.root.iconphoto(True, self.window_icon)  # Main window icon (for Windows OS)
        self.create_menubar()

        # Main window
        self.task_entry = tk.Entry(
            self.frame,
            font=("Times New Roman", 20),
            justify="center",
            textvariable=self.task,
        )
        self.task_entry.pack(side="top", fill="x", pady=10)
        self.task_entry.focus_set()

        self.label = tk.Label(
            self.frame,
            textvariable=self.timer,
            font=("Times New Roman", 40),
        )
        self.label.pack(pady=20)

        self.start_button = tk.Button(
            self.frame,
            command=self.execute_timer,
            textvariable=self.button_text,
            width=20,
            fg="green",
        )
        self.start_button.pack(side="bottom", fill="x")

    # GUI assistant methods
    def create_menubar(self):
        """Create the main window's menubar."""

        menubar = tk.Menu(self.root, tearoff=False)
        self.root.config(menu=menubar)

        # File menu and sub-menus
        file_menu = tk.Menu(menubar, tearoff=False)
        file_menu.add_command(
            label="Import",
            command=self.import_tasks,
            image=self.import_icon,
            compound="left",
            accelerator="Alt+I",
        )
        file_menu.add_command(
            label="Export",
            command=self.export_tasks,
            image=self.export_icon,
            compound="left",
            accelerator="Alt+E",
        )

        # Edit menu and sub-menus
        edit_menu = tk.Menu(menubar, tearoff=False)
        edit_menu.add_command(
            label="Edit",
            command=self.edit_entry,
            image=self.edit_icon,
            compound="left",
            accelerator="Ctrl+E",
        )

        edit_menu.add_command(
            label="Add",
            command=self.add_entry,
            image=self.add_icon,
            compound="left",
            accelerator="Ctrl+A",
        )
        edit_menu.add_command(
            label="Delete",
            command=self.delete_entry,
            image=self.delete_icon,
            compound="left",
            accelerator="Ctrl+D",
        )
        edit_menu.add_command(
            label="Clear Database",
            command=self.clear_database,
            image=self.clear_database_icon,
            compound="left",
            accelerator="Ctrl+B",
        )

        # View menu and sub-menus
        view_menu = tk.Menu(menubar, tearoff=False)
        view_menu.add_command(
            label="Statistics",
            command=self.show_statistics_window,
            image=self.statistics_icon,
            compound="left",
            accelerator="Ctrl+V",
        )

        menubar.add_cascade(
            label="File",
            menu=file_menu,
            underline=0,
        )
        menubar.add_cascade(
            label="Edit",
            menu=edit_menu,
            underline=0,
        )
        menubar.add_cascade(
            label="View",
            menu=view_menu,
            underline=0,
        )

    def load_window_icons(self) -> None:
        """Load all main window icons."""
        window_icon_path = str(self.icons.joinpath("timer.png"))

        export_icon_path = str(self.icons.joinpath("image-export.png"))
        import_icon_path = str(self.icons.joinpath("image-import.png"))
        statistics_icon_path = str(self.icons.joinpath("chart.png"))
        pencil_icon_path = str(self.icons.joinpath("pencil-small.png"))
        minus_icon_path = str(self.icons.joinpath("minus.png"))
        plus_icon_path = str(self.icons.joinpath("plus.png"))
        database_icon_path = str(self.icons.joinpath("database-small.png"))

        self.window_icon = tk.PhotoImage(file=window_icon_path)
        self.export_icon = tk.PhotoImage(file=export_icon_path)
        self.import_icon = tk.PhotoImage(file=import_icon_path)
        self.statistics_icon = tk.PhotoImage(file=statistics_icon_path)
        self.edit_icon = tk.PhotoImage(file=pencil_icon_path)
        self.add_icon = tk.PhotoImage(file=plus_icon_path)
        self.delete_icon = tk.PhotoImage(file=minus_icon_path)
        self.clear_database_icon = tk.PhotoImage(file=database_icon_path)

    def task_callback(self):
        """Autofill the task's name as user types corresponding letters."""
        value = self.task.get().lower()
        task_length_count = len(value)
        max_match_length = 5
        start = 0

        for task in self.tasks:
            if value[:task_length_count] == task[:max_match_length].lower():
                self.task.set(task)
                self.task_entry.icursor(start)
                self.set_timer()
            else:
                self.set_timer()

    def update(self):
        """Update the timer once per second."""
        if self.running:

            # Timer
            time = self.format_stopwatch_time(self.counter)
            self.timer.set(time)
            self.root.after(1000, self.update)
            self.counter += 1

    def execute_timer(self, event=None):
        """Start the timer if it isn't running; stop the timer otherwise."""
        if not self.running:
            self.running = True
            self.start_time = datetime.now()

            # GUI state
            self.button_text.set("Stop")
            self.start_button.config(fg="red")

            self.update()
        else:
            self.running = False
            self.stop_time = datetime.now()
            self.elapsed_time = self.calculate_elapsed_time(
                self.start_time,
                self.stop_time,
            )

            # GUI state
            self.button_text.set("Start")
            self.start_button.config(fg="green")

            self.commit_session()

    # Load and save
    def load_existing_task_names(self) -> set:
        raw_task_names = self.db.fetch_data(FETCH_TASK)
        task_names = set(name for i in raw_task_names for name in i)
        logging.info(f"Task names: {','.join(task_names)}")
        return task_names

    def commit_session(self):
        """Commit a session to the database."""
        task = self.task.get().strip()
        start = str(self.start_time)
        end = str(self.stop_time)
        elapsed = str(self.elapsed_time.total_seconds())

        if not task:
            task = simpledialog.askstring(
                "Add Task", "Please enter the name of your task."
            )

        session = [task, start, end, elapsed]
        self.db.commit(COMMIT_TASK_QUERY, session)

        logging.info(f"Session data: {' '.join(session)}")

    def set_window_state(self, window_width, window_height):
        """Load the window state if a previous state has been saved."""
        raw_state = self.db.fetch_data(FETCH_STATE)
        previous_state = list(name for i in raw_state for name in i)

        # Default window placement -- center screen
        center_x = self.root.winfo_screenwidth() // 2
        center_y = self.root.winfo_screenheight() // 2
        x = center_x - (window_width // 2)
        y = center_y - (window_height // 2)

        if previous_state:
            x, y, task = previous_state
            self.task.set(task)
            self.set_timer()
            return x, y
        return x, y

    def commit_window_state(self):
        """Save the state of the window. This method
        commits the window's current `x` and `y` coordinates,
        as well as the task on its display.
        """
        x, y = self.root.geometry().split("+")[1:]
        current_entry = self.task.get().strip()
        window_state = [x, y, current_entry]

        previous_state = self.db.fetch_data(FETCH_STATE)
        if not previous_state:
            self.db.commit(COMMIT_STATE_QUERY, window_state)
        else:
            self.db.update(UPDATE_STATE_QUERY.format(*window_state))

    def set_timer(self):
        """Load existing time for a task."""
        raw_time = self.db.fetch_data(
            FETCH_DAYS_TIME.format(self.task.get(), self.date),
        )
        duration = sum(list(float(seconds) for i in raw_time for seconds in i))
        if duration:
            self.timer.set(self.format_stopwatch_time(duration))
            self.counter = int(duration)
            return
        self.timer.set(DEFAULT_TIME)
        self.counter = 0

    # MENUBAR COMMANDS

    # View
    def show_statistics_window(self):
        """Display the statistics window."""
        total_time_per_task = dict()
        for task in self.tasks:
            data = self.db.fetch_data(FETCH_ELAPSED_TIME.format(task))
            total_time_per_task[task.strip()] = sum(
                [float(time) for name in data for time in name]
            )
        self.statistics_window = StatisticsWindow(
            self.root,
            total_time_per_task,
        )
        self.statistics_window.focus_set()
        self.statistics_window.grab_set()

    # Edit, Add, Delete
    def edit_entry(self, event=None):
        pass

    def add_entry(self, event=None):
        pass

    def delete_entry(self, event=None):
        pass

    def clear_database(self, event=None):
        pass

    # Exports and imports
    def export_tasks(self, event=None):
        """Export tasks to `.csv` format."""
        file_path = filedialog.asksaveasfile(
            defaultextension=".csv", filetypes=[("CSV", ".csv")]
        )
        data = self.db.fetch_data(FETCH_DATA)

        if file_path and file_path.name.endswith("csv"):
            self.export_as_csv(file_path, data)

    def import_tasks(self, event=None):
        """Import an existing `.csv` file with headers in the form:
        `task, started, stopped, elapsed`."""
        file_path = filedialog.askopenfile(
            defaultextension=".csv", filetypes=[("CSV", ".csv")]
        )
        if file_path and file_path.name.endswith("csv"):
            self.import_csv(file_path)

    def exit(self, event=None):
        """Commit window position and state, save the time if
        the timer is running, then exit.
        """
        self.commit_window_state()

        # Save the time if the window is closed
        # when the timer is running.
        if self.running:
            self.execute_timer()

        self.root.destroy()

    # HELPER METHODS

    @staticmethod
    def calculate_elapsed_time(start_time, stop_time):
        """Calculate elapsed time in seconds."""
        return stop_time - start_time

    @staticmethod
    def get_date() -> str:
        """Return the current date without the time."""
        current_date = str(datetime.now()).split()[:1][0]
        return current_date

    @staticmethod
    def format_stopwatch_time(seconds: int | float) -> str:
        """Format stopwatch in the form: `hh:mm:ss`."""
        # Reset at a maximum of 99 hours.
        hours = int((seconds // 3600) % 100)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)

        return f"{hours:02}:{minutes:02}:{secs:02}"

    @staticmethod
    def export_as_csv(file_name, data):
        """Export all tasks as a `.csv` file."""
        with open(file_name.name, "w") as csv_file:
            writer = csv.writer(csv_file, lineterminator="\n")
            writer.writerow(["Task", "Started", "Stopped", "Total Time"])
            writer.writerows(data)

    def import_csv(self, file_path):
        """Import a `.csv` file with columns: `task, started, stopped, elapsed`."""
        with open(file_path.name, "r") as csv_file:
            reader = csv.reader(csv_file)
            next(reader)  # Skip headers
            # TODO:
            # Standardize dates and elapsed time.
            self.db.commit_many(COMMIT_TASK_QUERY, reader)
        self.tasks = self.load_existing_task_names()
