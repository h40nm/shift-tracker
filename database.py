import sqlite3
from datetime import datetime

class Database():
    def __init__(self, config: dict):
        self.path = config["db_path"]
        self.db = config["db_shifts"]
        self.connect_to_db(self.path)

    def connect_to_db(self, database: str) -> bool:
        try:
            self.connection = sqlite3.connect(self.path)
            return True
        except Exception as e:
            print(e)
            f = open(self.path, "w")
            f.close()
            self.connection = sqlite3.connect(self.path)
            self.create_shifts_table()
            return True

    def create_shifts_table(self) -> bool:
        message = f'''CREATE TABLE {self.db} 
                    (SID INT PRIMARY KEY NOT NULL AUTO INCREMENT, 
                    CREATED_AT DATETIME NOT NULL,
                    TIME_START DATETIME,
                    TIME_END DATETIME)'''
        try:
            self.write(message)
            return True
        except Exception as e:
            print(f"Could not create database {self.db}!\nError: {e}")
            return False

    def log_shift(self, time_start: str, time_end: str)-> bool:
        message = f"INSERT INTO {self.db} (CREATED_AT, TIME_START, TIME_END) VALUES ({datetime.now()}, {time_start}, {time_end})"
        self.write(message)

    def write(self, message: str) -> bool:
        try:
            self.connection.execute(message)
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Could not write message {message} to database {self.path}!")
            return False

    def destroy(self) -> None:
        try:
            self.connection.close()
        except Exception as e:
            print(f"Could not close Database {self.path}!\nError: {e}")


