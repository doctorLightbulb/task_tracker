"""A module containing the Database class and related query constants."""

import sqlite3
from pathlib import Path

# SETUP QUERIES

CREATE_TABLE_QUERY = """
    CREATE TABLE IF NOT EXISTS tasks(
        task,
        started,
        stopped,
        elapsed
    )
"""

CREATE_SESSION_TABLE_QUERY = """
    CREATE TABLE IF NOT EXISTS session(
        x,
        y,
        task
    )
"""

# COMMIT QUERIES

COMMIT_TASK_QUERY = """
    INSERT INTO tasks VALUES(?, ?, ?, ?)
"""

COMMIT_STATE_QUERY = """
    INSERT INTO session VALUES(?, ?, ?)
"""

UPDATE_STATE_QUERY = """
    UPDATE session
    SET x = {},
        y = {},
        task = '{}'
"""

# FETCH QUERIES

FETCH_TASK = """
    SELECT DISTINCT task
    FROM tasks
    ORDER BY stopped
"""

FETCH_DAYS_TIME = """
    SELECT SUM(elapsed)
    FROM tasks
    WHERE task = '{}' AND started LIKE "%{}%"
"""

FETCH_ELAPSED_TIME = """
    SELECT SUM(elapsed)
    FROM tasks
    WHERE task = '{}'
"""

FETCH_DATA = """
    SELECT task, started, stopped, elapsed
    FROM tasks
    ORDER BY task
"""

FETCH_STATE = """
    SELECT x, y, task
    FROM session
"""


class Database:
    """Commits data to and fetches data from a SQLite3 database."""

    def __init__(self, path):
        self.db_path = Path(path)
        self.cursor = sqlite3.connect(self.db_path).cursor()

    @property
    def db_path(self):
        return self._db_path

    @db_path.setter
    def db_path(self, path):
        self._db_path = path

    def initialize_database(self):
        """Creates the database at the specified path if it doesn't exist."""
        database_exists = self.db_path.exists()
        database_dir_exists = self.db_path.parent.parent.exists()

        if not database_exists and database_dir_exists:
            self.db_path.parent.mkdir(exist_ok=True)
            self.create_empty_table(CREATE_TABLE_QUERY)
            self.create_empty_table(CREATE_SESSION_TABLE_QUERY)

    def create_empty_table(self, query: str):
        """Creates a table with the query."""
        self.cursor.execute(query)
        self.cursor.connection.commit()

    def commit(self, query, data):
        """Commits data to the selected database."""
        self.cursor.execute(query, data)
        self.cursor.connection.commit()

    def commit_many(self, query, data):
        """Commits data to the selected database."""
        self.cursor.executemany(query, data)
        self.cursor.connection.commit()

    def update(self, query):
        """Commit data to the selected database."""
        self.cursor.execute(query)
        self.cursor.connection.commit()

    def fetch_data(self, query):
        """Returns a list of results."""
        results = self.cursor.execute(query)
        return results.fetchall()

    def fetchone(self, query: str):
        """Returns a single result."""
        results = self.cursor.execute(query)
        return results.fetchone()

    def close_database(self):
        """Closes the database connection."""
        self.cursor.connection.close()
