# src/task_tracker/__main__.py

"""The main entry point to Task Tracker 1.0"""

import sys
import tkinter as tk
from importlib import resources
from pathlib import Path
from tkinter import messagebox

from task_tracker.database import Database
from task_tracker.gui.main_window import TaskTracker


def main():
    # Files
    home_path = Path.home()
    app_data_path = home_path / "AppData" / "Local"
    database_path = app_data_path / "HomeApps" / "Task Tracker 1.0" / "tasks.db"

    icons = resources.files("task_tracker.images")

    try:
        database = Database(database_path)
        database.initialize_database()
    except Exception as e:
        messagebox.showerror(
            "Error", f"An error has occurred while loading the database:\n{e}"
        )
        sys.exit(1)

    # Main program
    root = tk.Tk()
    TaskTracker(root, database, icons)
    root.mainloop()


if __name__ == "__main__":
    main()
