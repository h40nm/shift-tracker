import tkinter as tk
from tkinter import ttk
from datetime import datetime
from database import Database

class Frame_Add(tk.Frame):
    def __init__(self, master, config: dict):
        self.master = master
        tk.Frame.__init__(self, self.master)

        self.database = Database(config)

        self.combobox_start_day = ttk.Combobox(self, width=3)
        self.combobox_start_month = ttk.Combobox(self, width=3)
        self.combobox_start_year = ttk.Combobox(self, width=5)
        self.combobox_start_hour = ttk.Combobox(self, width=3)
        self.combobox_start_minute = ttk.Combobox(self, width=3)

        days_list = list(range(1,13))
        i = 0
        for day in days_list:
            if day < 10:
                day = str(day)
                days_list[i] = "0" + day
            else:
                days_list[i] = str(day)
            i+=1
        self.combobox_start_month["values"] = days_list
        self.combobox_start_day["values"] = list(range(1,32))
        self.combobox_start_year["values"] = list(range(2000, 2101))
        self.combobox_start_hour["values"] = list(range(0, 25))
        self.combobox_start_minute["values"] = ("00", "15", "30", "45")

        self.start_set_current_date()

        self.combobox_end_day = ttk.Combobox(self, width=3)
        self.combobox_end_month = ttk.Combobox(self, width=3)
        self.combobox_end_year = ttk.Combobox(self, width=5)
        self.combobox_end_hour = ttk.Combobox(self, width=3)
        self.combobox_end_minute = ttk.Combobox(self, width=3)

        self.combobox_end_day["values"] = self.combobox_start_day["values"]
        self.combobox_end_month["values"] = self.combobox_start_month["values"]
        self.combobox_end_year["values"] = self.combobox_start_year["values"]
        self.combobox_end_hour["values"] = self.combobox_start_hour["values"]
        self.combobox_end_minute["values"] = self.combobox_start_minute["values"]

        self.end_set_current_date()

        self.label_start_time = tk.Label(self, text="Beginning:")
        self.label_end_time = tk.Label(self, text="End:")
        self.label_date = tk.Label(self, text="Date")
        self.label_time = tk.Label(self, text="Time")
        self.label_warning = tk.Label(self, text="")
        self.button_submit = tk.Button(self, text="Add", command=self.add)
        self.button_reset_start = tk.Button(self, text="reset", command=self.start_set_current_date)
        self.button_reset_end = tk.Button(self, text="reset", command=self.end_set_current_date)

        self.label_start_time.grid(row=1, column=0, sticky="NESW")
        self.label_end_time.grid(row=2, column=0, sticky="NESW")
        self.label_date.grid(row=0, column=1, columnspan=3, sticky="NESW")
        self.label_time.grid(row=0, column=4, columnspan=2, sticky="NESW")
        self.label_warning.grid(row=3, column=1, columnspan=7, sticky="NESW")
        self.combobox_start_day.grid(row=1, column=1, sticky="NESW")
        self.combobox_start_month.grid(row=1, column=2, sticky="NESW")
        self.combobox_start_year.grid(row=1, column=3, sticky="NESW")
        self.combobox_start_hour.grid(row=1, column=4, sticky="NESW")
        self.combobox_start_minute.grid(row=1, column=5, sticky="NESW")
        self.combobox_end_day.grid(row=2, column=1, sticky="NESW")
        self.combobox_end_month.grid(row=2, column=2, sticky="NESW")
        self.combobox_end_year.grid(row=2, column=3, sticky="NESW")
        self.combobox_end_hour.grid(row=2, column=4, sticky="NESW")
        self.combobox_end_minute.grid(row=2, column=5, sticky="NESW")
        self.button_submit.grid(row=3, column=0, sticky="NESW")
        self.button_reset_start.grid(row=1, column=6, sticky="NESW")
        self.button_reset_end.grid(row=2, column=6, sticky="NESW")

    def add(self):
        start_string = f"{self.combobox_start_year.get()}-{self.combobox_start_month.get()}-{self.combobox_start_day.get()} {self.combobox_start_hour.get()}-{self.combobox_start_minute.get()}"
        start_datetime = datetime.strptime(start_string, "%Y-%m-%d %H-%M")
        end_string = f"{self.combobox_end_year.get()}-{self.combobox_end_month.get()}-{self.combobox_end_day.get()} {self.combobox_end_hour.get()}-{self.combobox_end_minute.get()}"
        end_datetime = datetime.strptime(end_string, "%Y-%m-%d %H-%M")

        if start_datetime > end_datetime:
            self.label_warning.config(text="ERROR: End time < start time!")
            self.label_warning.config(fg="red")
        elif start_datetime == end_datetime:
            self.label_warning.config(text="WARNING: End time is not set yet!")
            self.label_warning.config(fg="orange")
        else:
            if  self.database.log_shift(start_datetime, end_datetime) == True:
                self.label_warning.config(text="Shift saved successfully.")
                self.label_warning.config(fg="green")
            else:
                self.label_warning.config(text="ERROR: Could not save to database!")
                self.label_warning.config(fg="red")

    def start_set_current_date(self):
        pos = 0
        next_hour = int(datetime.now().strftime("%H"))
        check = int(datetime.now().strftime("%M"))
        if int(check) % 15 < 15/2:
            pos = int(check / 15)
        else:
            pos = int(check / 15) + 1
        
        if pos >= len(self.combobox_start_minute["values"]):
            pos = int(pos) % 4
            next_hour = next_hour + 1

        self.combobox_start_minute.current(pos)
        self.combobox_start_day.current(self.combobox_start_day["values"].index(datetime.now().strftime("%d")))
        self.combobox_start_month.current(self.combobox_start_month["values"].index(datetime.now().strftime("%m")))
        self.combobox_start_year.current(self.combobox_start_year["values"].index(datetime.now().strftime("%Y")))
        self.combobox_start_hour.current(next_hour)

    def end_set_current_date(self):
        pos = 0
        next_hour = int(datetime.now().strftime("%H"))
        check = int(datetime.now().strftime("%M"))
        if int(check) % 15 < 15/2:
            pos = int(check / 15)
        else:
            pos = int(check / 15) + 1
        
        if pos >= len(self.combobox_end_minute["values"]):
            pos = int(pos) % 4
            next_hour = next_hour + 1

        self.combobox_end_minute.current(pos)
        self.combobox_end_day.current(self.combobox_end_day["values"].index(datetime.now().strftime("%d")))
        self.combobox_end_month.current(self.combobox_end_month["values"].index(datetime.now().strftime("%m")))
        self.combobox_end_year.current(self.combobox_end_year["values"].index(datetime.now().strftime("%Y")))
        self.combobox_end_hour.current(next_hour)

    def __del__(self):
        self.database.disconnect()




        


