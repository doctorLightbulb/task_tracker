"""A module containing the Database class and related query constants."""

import sqlite3
from pathlib import Path

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

FETCH_TASK = """
    SELECT task
    FROM tasks
    ORDER BY task
"""

FETCH_DAYS_TIME = """
    SELECT elapsed
    FROM tasks
    WHERE task = '{}' AND started LIKE "%{}%"
"""

FETCH_ELAPSED_TIME = """
    SELECT elapsed
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
    """A class for committing data to and fetching data from a SQLite3
    database.
    """

    def __init__(self, path):
        self.db_path = Path(path)

        database_exists = self.db_path.exists()
        database_dir_exists = self.db_path.parent.parent.exists()

        if not database_exists and database_dir_exists:
            self.db_path.parent.mkdir(exist_ok=True)
            self.create_empty_table(CREATE_TABLE_QUERY)
            self.create_empty_table(CREATE_SESSION_TABLE_QUERY)

    @property
    def db_path(self):
        return self._db_path

    @db_path.setter
    def db_path(self, path):
        self._db_path = path

    def create_empty_table(self, query: str):
        with sqlite3.connect(self.db_path) as connection:
            cursor = connection.cursor()
            cursor.execute(query)

    def commit(self, query, data):
        """Commit data to the selected database."""
        with sqlite3.connect(self.db_path) as connection:
            cursor = connection.cursor()
            cursor.execute(query, data)
            connection.commit()

    def commit_many(self, query, data):
        """Commit data to the selected database."""
        with sqlite3.connect(self.db_path) as connection:
            cursor = connection.cursor()
            cursor.executemany(query, data)

    def update(self, query):
        """Commit data to the selected database."""
        with sqlite3.connect(self.db_path) as connection:
            cursor = connection.cursor()
            cursor.execute(query)
            connection.commit()

    def fetch_data(self, query):
        with sqlite3.connect(self.db_path) as connection:
            cursor = connection.cursor()
            results = cursor.execute(query)
            return results.fetchall()

    def find_matches(self, query, word):
        with sqlite3.connect(self.db_path) as connection:
            cursor = connection.cursor()
            results = cursor.execute(query.format(word))
            return results.fetchall()
