class Config():
    def __init__(self):
        self.config_dict = {
            "width": 640,
            "height": 720,
            "title": "Worktime Logger v1",
            "db_path": "shifts.db",
            "db_shifts": "db_shifts",
            "logfile_path": "log.txt",
            "shifts_per_page": 10,

        }

    def get_config(self) -> dict:
        return self.config_dict