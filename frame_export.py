import tkinter as tk
from tkinter import ttk
from datetime import datetime
from datetime import timedelta
from db import Database

class Frame_Export(tk.Frame):
    def __init__(self, master, config: dict):
        self.master = master
        self.config = config
        tk.Frame.__init__(self, self.master)
        self.database = Database(config)

        self.spacer_left = tk.Label(self, text="")
        self.spacer_right = tk.Label(self, text="")

        self.label_export = tk.Label(self, text="Select Month to Export")
        self.combobox_year = ttk.Combobox(self, width=4)
        self.combobox_month = ttk.Combobox(self, width=4)
        self.button_export = tk.Button(self, text="Export", command=self.export)
        self.label_feedback = tk.Label(self, text="")

        self.spacer_left.grid(row=0, column=0, sticky="NESW")
        self.spacer_right.grid(row=5, column=3, sticky="NESW")
        self.label_export.grid(row=1, column=1, columnspan=2, sticky="NESW")
        self.combobox_year.grid(row=2, column=1, sticky="NES")
        self.combobox_month.grid(row=2, column=2, sticky="NSW")
        self.button_export.grid(row=3, column=1, columnspan=2, sticky="NS")
        self.label_feedback.grid(row=4, column=1, columnspan=2, sticky="NESW")

        self.combobox_year["values"] = list(range(2000, 2051))
        self.combobox_month["values"] = list(range(1, 13))
        
        current_date = datetime.now()
        year = int(current_date.strftime("%Y"))
        month = int(current_date.strftime("%m"))
        self.combobox_year.current(year-2000)
        self.combobox_month.current(month-1)

        self.columnconfigure(0, weight=3, minsize=120)
        self.columnconfigure(1, weight=1, minsize=120)
        self.columnconfigure(2, weight=1, minsize=120)
        self.columnconfigure(3, weight=3, minsize=120)

        self.rowconfigure(0, weight=100)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(5, weight=100)

        self.configure_background_color(container=self, color="white")

    def configure_background_color(self, container, color):
        container.configure(bg=color)
        for child in container.winfo_children():
            try:
                child.configure(bg=color)
            except:
                pass

    def export(self):
        date = self.get_query_date()
        self.set_feedback_text(f"Querying all working times starting from {date}")
        work_times = self.get_entries_from_db(date)
        self.merge_work_times(work_times)
        

    def get_query_date(self) -> datetime:
        month = int(self.combobox_month.get())-1
        year = int(self.combobox_year.get())

        if month == 0:
            month = 12
            year = year-1

        date = f"{year}-{month}-10 00-00-00"
        date = datetime.strptime(date, "%Y-%m-%d %H-%M-%S")
        return date
    
    def get_entries_from_db(self, date: datetime) -> list:
        query = f"SELECT * FROM {self.config['db_shifts']} WHERE TIME_START>='{date}'"
        result = self.database.write(query)
        return result

    def set_feedback_text(self, text: str) -> None:
        self.label_feedback.configure(text=text)

    def merge_work_times(self, work_times: list) -> list:
        for elem in work_times:
            date = elem[2]
            date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
            date = date.strftime("%Y-%m-%d")
            print(date)
