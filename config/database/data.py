import sqlite3

class Database:
    def __init__(self, db_file: str):
        self._connection = sqlite3.connect(db_file)
        self._cursor = self._connection.cursor()

    def add_client(self, user_id: int) -> None:
        with self._connection:
            try:
                self._cursor.execute(f"INSERT INTO client VALUES({user_id})")
            except sqlite3.IntegrityError: pass

    def client_exists(self, user_id: int) -> bool:
        with self._connection:
            result = self._cursor.execute(f"SELECT 1 FROM client WHERE user_id={user_id}").fetchone()
            return result is not None

    def update_maintenance_data(self, value: int) -> None:
        with self._connection:
            self._cursor.execute(f"UPDATE maintenance SET value = {value} WHERE id = 1")

    def get_maintenance_data(self) -> int:
        return self._cursor.execute("SELECT value FROM maintenance WHERE id = 1").fetchone()[0]