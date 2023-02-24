import os.path
from datetime import datetime

class Logger():
    def __init__(self, config: dict) -> None:
        self.path = config["logfile_path"]
        self.create_logfile(self.path)
    
    def create_logfile(self, log_file: str) -> bool:
        if os.path.isfile(log_file):
            return False
        else:
            f = open(log_file, "w")
            f.write(f"Created log file at {datetime.now()}")
            f.close()
            return True

    def log(self, message: str) -> bool:
        try:
            f = open(self.path.txt, "a")
            f.write(message)
            f.close()
            return True
        except Exception as e:
            print(f"ERROR: Could not log Message: {message}.\n EXCEPTION: {e}")
            return False

        