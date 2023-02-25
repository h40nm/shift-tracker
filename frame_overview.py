import tkinter as tk
from tkinter import ttk
from datetime import datetime
from datetime import timedelta
from database import Database

class Frame_Overview(tk.Frame):
    def __init__(self, master, config: dict):
        self.master = master
        self.config = config
        tk.Frame.__init__(self, self.master)

        self.database = Database(config)

        self.label_id = tk.Label(self, text="ID")
        self.label_created_at = tk.Label(self, text="STARTING AT")
        self.label_start = tk.Label(self, text="START")
        self.label_end = tk.Label(self, text="END")
        self.label_worked = tk.Label(self, text="WORK TIME")
        self.label_filter_1 = tk.Label(self, text="Filter last")
        self.label_filter_2 = tk.Label(self, text="days")
        self.combobox_filter = ttk.Combobox(self, width=5)
        self.combobox_filter["values"] = list(range(0, 10001))
        self.combobox_filter.current(30)
        self.combobox_filter.bind("<<ComboboxSelected>>", self.show_entries)

        self.label_filter_1.grid(row=0, column=0, sticky="NESW")
        self.combobox_filter.grid(row=0, column=1, sticky="NESW")
        self.label_filter_2.grid(row=0, column=2, sticky="NESW")
        self.label_id.grid(row=1, column=0, sticky="NESW")
        self.label_created_at.grid(row=1, column=1, sticky="NESW")
        self.label_start.grid(row=1, column=2, sticky="NESW")
        self.label_end.grid(row=1, column=3, sticky="NESW")
        self.label_worked.grid(row=1, column=4, sticky="NESW")


        self.show_entries()

    def show_entries(self, event=None):
        result = self.database.write(f"SELECT * FROM {self.config['db_shifts']} WHERE TIME_START >= '{self.get_entries_from_last_x_days(int(self.combobox_filter.get()))}'")

        row = 2
        for shift in result:
            row += 1
            id = shift[0]
            created = datetime.strptime(shift[2], "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d")
            start = datetime.strptime(shift[2], "%Y-%m-%d %H:%M:%S")
            end = datetime.strptime(shift[3], "%Y-%m-%d %H:%M:%S")
            worked = end-start
            start = start.strftime("%H:%M")
            end = end.strftime("%H:%M")
            worked = datetime.strptime(str(worked), "%H:%M:%S")
            worked = worked.strftime("%H:%M")

            label_id = tk.Label(self, text=id)
            label_created = tk.Label(self, text=created)
            label_start = tk.Label(self, text=start)
            label_end = tk.Label(self, text=end)
            label_worked = tk.Label(self, text=worked)

            label_id.grid(row=row, column=0)
            label_created.grid(row=row, column=1)
            label_start.grid(row=row, column=2)
            label_end.grid(row=row, column=3)
            label_worked.grid(row=row, column=4)

    def get_entries_from_last_x_days(self, days: int):
        print(f"Get Entries since {datetime.now() - timedelta(days=days)}")
        return datetime.now() - timedelta(days=days)

    def __del__(self):
        self.database.disconnect()