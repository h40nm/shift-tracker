import tkinter as tk
from tkinter import ttk
from datetime import datetime
from datetime import timedelta
from db import Database
import docx                         # pip install python-docx
from docxtpl import DocxTemplate    # pip install docxtpl

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
        date_start, date_end = self.get_query_dates()
        self.set_feedback_text(f"Starting at {date_start}")
        work_times = self.get_entries_from_db(date_start, date_end)
        work = self.merge_work_times(work_times, date_start, date_end)
        self.write_to_document(work)
        

    def get_query_dates(self) -> datetime:
        month = int(self.combobox_month.get())
        year = int(self.combobox_year.get())
        date_end = f"{year}-{month}-10 00-00-00"
        month = int(self.combobox_month.get())-1

        if month == 0:
            month = 12
            year = year-1

        date_start = f"{year}-{month}-10 00-00-00"
        date_start = datetime.strptime(date_start, "%Y-%m-%d %H-%M-%S")
        date_end = datetime.strptime(date_end, "%Y-%m-%d %H-%M-%S")
        return date_start, date_end
    
    def get_entries_from_db(self, date_start: datetime, date_end: datetime) -> list:
        query = f"SELECT * FROM {self.config['db_shifts']} WHERE TIME_START>='{date_start}' AND TIME_START<'{date_end}'"
        result = self.database.write(query)
        list = []
        for line in result:
            list.append(line)
        return list

    def set_feedback_text(self, text: str) -> None:
        self.label_feedback.configure(text=text)

    def merge_work_times(self, work_times: list, date_start: datetime, date_end: datetime) -> list: 
        # generate a dictionary of work times on the same day to prepare further modification
        temp_dict = {}
        for elem in work_times:
            date = elem[2]
            date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
            date = date.strftime("%Y-%m-%d")

            exist_flag = False

            for key in temp_dict.keys():
                if key == date:
                    exist_flag = True
                    break

            if exist_flag == False:
                temp_dict[date] = []

            temp_dict[date].append(elem)

        # get the total working time, start, end and pause times for each day
        self.monthly_work_no_breaks = timedelta(days=0)
        worked_list = []
        for elem in temp_dict:
            worked_per_day = timedelta(days=0)
            time_start = datetime.now()
            for shift in temp_dict[elem]:

                end = shift[3]
                start = shift[2]
                end = datetime.strptime(end, "%Y-%m-%d %H:%M:%S")
                start = datetime.strptime(start, "%Y-%m-%d %H:%M:%S")
                delta = end - start
                worked_per_day += delta

                if start < time_start:
                    time_start = start

            self.monthly_work_no_breaks += worked_per_day
            notification = ""
            time_end = time_start + worked_per_day
            if timedelta(hours=6) <= worked_per_day < timedelta(hours=9):
                time_end += timedelta(minutes=30)
                notification = "Pause: 00:30h"
            elif timedelta(hours=9) <= worked_per_day:
                time_end +=  timedelta(hours=1)
                notification = "Pause: 01:00h"


            working_duration = f"{time_start.strftime('%H:%M')} - {time_end.strftime('%H:%M')}"
            worked_list.append([start.strftime("%Y-%m-%d"), working_duration, worked_per_day, notification])

        # fill the list with blank days with no working times for the entire month
        dates_list = []
        date = date_start
        while date < date_end:
            date += timedelta(days=1)
            dates_list.append(date.strftime("%Y-%m-%d"))

        worked = []
        for date in dates_list:
            shift = [str(date), " ", " ", " "]
            for work_day in worked_list:
                if date == work_day[0]:
                    shift = [str(date), str(work_day[1]), str(work_day[2]), str(work_day[3])]
            worked.append(shift)

        #make sure table is always 31 rows long
        first_half = []
        second_half = []
        length = 31         # max days in month
        modified = False
        
        if len(worked) == 30:
            first_half = worked[0:20]   # get all days from previous month to the 28th
            second_half = worked[-10:]
            buffer = [" ", " ", " ", " "]
            modified = True
        elif len(worked) == 29:
            first_half = worked[0:19]   # get all days from previous month to the 28th
            second_half = worked[-10:]
            buffer = [" ", " ", " ", " "],[" ", " ", " ", " "]
            modified = True
        elif len(worked) == 28:
            first_half = worked[0:18]   # get all days from previous month to the 28th
            second_half = worked[-10:]
            buffer = [" ", " ", " ", " "],[" ", " ", " ", " "],[" ", " ", " ", " "]
            modified = True

        if modified == True:
            worked = []
            for elem in first_half:
                worked.append(elem)
            for elem in buffer:
                worked.append(elem)
            for elem in second_half:
                worked.append(elem)

        #print(len(worked))

        #for line in worked:
        #    print(line)

        return worked


    def write_to_document(self, work: list) -> None:
        template = docx.Document('Stundenzettel.docx')

        #for i, row in enumerate(template.tables[0].rows):
        #    text = list((cell.text for cell in row.cells))
        #    print(text)

        year = self.combobox_year.get()
        month = int(self.combobox_month.get())
        if month < 10:
            month = "0" + str(month)
        date = f"{year}-{month}"
        filename = f"{date}-Stundenzettel.docx"

        # convert monthly_total work to the right format
        self.monthly_work_no_breaks = int(self.monthly_work_no_breaks.total_seconds())
        seconds_in_hour = 3600
        seconds_in_minute = 60
        hours = int(self.monthly_work_no_breaks / seconds_in_hour)
        minutes = int(self.monthly_work_no_breaks % seconds_in_hour)
        if minutes == 0:
            minutes = "00"
        else:
            minutes = int(minutes / seconds_in_minute)
        self.monthly_work_no_breaks = str(hours) + ":" + str(minutes)

        template.save(filename)

        doc = DocxTemplate(filename)

        context = {'date': f"{month}/{year}",
                   'work': work,
                   'work_sum': self.monthly_work_no_breaks
                   }
        doc.render(context)
        doc.save(filename)
        