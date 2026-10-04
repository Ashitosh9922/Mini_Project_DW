import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

load_dotenv()


class DatabaseConnection:
    """Singleton class for managing the MySQL database connection."""

    _instance = None
    _connection = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
        return cls._instance

    def connect(self):
        """Create and return a MySQL connection."""
        if self._connection is not None and self._connection.is_connected():
            return self._connection

        try:
            self._connection = mysql.connector.connect(
                host=os.getenv("DB_HOST"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                database=os.getenv("DB_NAME")
            )

            return self._connection

        except Error as e:
            print(f"Database connection error: {e}")
            return None

    def close(self):
        """Close the database connection."""
        if self._connection is not None and self._connection.is_connected():
            self._connection.close()
            self._connection = None

    def execute(self, query, params=None):
        """Execute INSERT, UPDATE, DELETE or other SQL statements."""
        conn = self.connect()

        if conn is None:
            return False

        cursor = None

        try:
            cursor = conn.cursor()

            if params is not None:
                cursor.execute(query, params)
            else:
                cursor.execute(query)

            conn.commit()
            return True

        except Error as e:
            conn.rollback()
            print(f"SQL execution error: {e}")
            return False

        finally:
            if cursor is not None:
                cursor.close()

    def fetch(self, query, params=None):
        """Execute a SELECT query and return all rows."""
        conn = self.connect()

        if conn is None:
            return []

        cursor = None

        try:
            cursor = conn.cursor(dictionary=True)

            if params is not None:
                cursor.execute(query, params)
            else:
                cursor.execute(query)

            return cursor.fetchall()

        except Error as e:
            print(f"SQL fetch error: {e}")
            return []

        finally:
            if cursor is not None:
                cursor.close()
