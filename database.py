import sqlite3
from datetime import datetime

class Database():
    def __init__(self, config: dict):
        self.path = config["db_path"]
        self.db = config["db_shifts"]
        self.connect_to_db(self.path)

    def connect_to_db(self, database: str) -> bool:
        self.connection = sqlite3.connect(self.path)
        self.cursor = self.connection.cursor()
        cursor = self.write(f"SELECT * FROM {self.db};")
        if cursor != False:
            print("CONNECTED TO DB.")
        else:
            if self.create_shifts_table():
                print(f"Created Database {self.db}.")
            else:
                print(f"Database {self.db} could not be found nor created.")
            return True

    def create_shifts_table(self) -> bool:
        message = f'''CREATE TABLE {self.db} 
                    (SID INTEGER PRIMARY KEY AUTOINCREMENT, 
                    CREATED_AT DATETIME NOT NULL,
                    TIME_START DATETIME,
                    TIME_END DATETIME);'''
        try:
            if self.write(message):
                return True
            else:
                return False
        except Exception as e:
            print(f"Could not create database {self.db}!\nError: {e}")
            return False

    def log_shift(self, time_start: datetime, time_end: datetime)-> bool:
        try:
            message = f"INSERT INTO {self.db} (CREATED_AT, TIME_START, TIME_END) VALUES ('{datetime.now()}', '{time_start}', '{time_end}');"
            self.write(message)
            return True
        except Exception as e:
            print(e)
            return False

    def write(self, message: str):
        try:
            result = self.cursor.execute(message)
            self.connection.commit()
            return result
        except Exception as e:
            print(f"Could not write message {message} to database {self.path}!")
            print(e)
            return False

    def disconnect(self) -> None:
        try:
            self.connection.close()
            print("Disconnected from database.")
        except Exception as e:
            print(f"Could not close Database {self.path}!\nError: {e}")


