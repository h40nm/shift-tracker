import tkinter as tk
from tkinter import ttk
from datetime import datetime
from datetime import timedelta
from db import Database

class Frame_Overview(tk.Frame):
    def __init__(self, master, config: dict):
        self.master = master
        self.config = config
        tk.Frame.__init__(self, self.master)
        self.database = Database(config)

        self.page_count = 1
        self.page_current = 1
        self.update_flag = False
        self.delete_flag = False
        self.list_shifts = []

        self.container = tk.Frame(self, relief="ridge", borderwidth="2")
        self.spacer = tk.Label(self, text="")
        self.spacer2 = tk.Label(self, text="")
        self.spacer3 = tk.Label(self, text="__________________________________________________")
        self.spacer4 = tk.Label(self, text="")
        self.spacer5 = tk.Label(self, text="")

        self.label_filter_1 = tk.Label(self, text="Filter last")
        self.label_filter_2 = tk.Label(self, text="days")
        self.combobox_filter = ttk.Combobox(self, width=5)
        self.combobox_filter["values"] = list(range(0, 10001))
        self.combobox_filter.current(30)
        self.combobox_filter.bind("<<ComboboxSelected>>", self.update)
        self.combobox_filter.bind("<Return>", self.update)

        self.button_next = tk.Button(self, text="►", command=self.next)
        self.button_prev = tk.Button(self, text="◄", command=self.prev, state="disabled")
        self.label_total = tk.Label(self, text=f"{len(self.list_shifts)} items")
        self.label_page_count = tk.Label(self, text=f"page {self.page_current} of {self.page_count}")

        self.button_update = tk.Button(self, text="Update", command=self.update_shift)
        self.button_delete = tk.Button(self, text="Delete", command=self.delete_shift)

        self.label_edit_hid = tk.Label(self, text="ID")
        self.label_edit_hcreated_at = tk.Label(self, text="STARTING AT")
        self.label_edit_hstart = tk.Label(self, text="START")
        self.label_edit_hend = tk.Label(self, text="END")

        self.label_edit_id = tk.Label(self, text="0")
        #self.label_edit_created = tk.Label(self, text="0000-00-00")
        self.container_edit_date = tk.Frame(self)
        self.combobox_edit_year = ttk.Combobox(self.container_edit_date, width=4)
        self.combobox_edit_month = ttk.Combobox(self.container_edit_date, width=2)
        self.combobox_edit_day = ttk.Combobox(self.container_edit_date, width=2)
        self.combobox_edit_start_h = ttk.Combobox(self, width=3)
        self.combobox_edit_start_m = ttk.Combobox(self, width=3)
        self.combobox_edit_end_h = ttk.Combobox(self, width=3)
        self.combobox_edit_end_m = ttk.Combobox(self, width=3)

        self.combobox_edit_year["values"] = list(range(2000, 2050))
        self.combobox_edit_month["values"] = list(range(1, 13))
        self.combobox_edit_day["values"] = list(range(1, 32))

        hours_list = list(range(0, 25))
        i = 0
        for hour in hours_list:
            if hour < 10:
                hour = str(hour)
                hours_list[i] = "0"+hour
            else:
                hours_list[i] = str(hour)
            i += 1

        self.combobox_edit_start_h["values"] = hours_list
        self.combobox_edit_start_m["values"] = ("00", "15", "30", "45")
        self.combobox_edit_end_h["values"] = hours_list
        self.combobox_edit_end_m["values"] = ("00", "15", "30", "45")
        
        self.reset_edit_fields()

        self.label_update_message = tk.Label(self, text="")
        self.button_set_now = tk.Button(self, text="Now", command=self.current_datetime)
        self.button_reset = tk.Button(self, text="Reset", command=self.reset_edit_fields)
        self.button_save = tk.Button(self, text="Save", command=self.save_shift)

        self.combobox_edit_year.grid(row=0, column=0, sticky="NESW")
        self.combobox_edit_month.grid(row=0, column=1, sticky="NESW")
        self.combobox_edit_day.grid(row=0, column=2, sticky="NESW")

        self.label_filter_1.grid(row=0, column=0, sticky="NESW")
        self.combobox_filter.grid(row=0, column=1, sticky="NESW")
        self.label_filter_2.grid(row=0, column=2, sticky="NESW")
        self.container.grid(row=1, column=0, sticky="NESW")
        self.button_prev.grid(row=2, column=0, sticky="NESW")
        self.button_next.grid(row=2, column=1, sticky="NESW")
        self.label_total.grid(row=2, column=2, sticky="NESW")
        self.label_page_count.grid(row=2, column=3, sticky="NESW")
        self.spacer.grid(row=3, column=0, sticky="NESW")
        self.button_update.grid(row=4, column=1, sticky="NESW")
        self.button_delete.grid(row=4, column=2, sticky="NESW")
        self.spacer2.grid(row=5, column=0, sticky="NESW")
        self.spacer3.grid(row=6, column=0, sticky="NESW", columnspan=4)
        self.spacer4.grid(row=7, column=0, sticky="NESW")
        self.label_edit_hid.grid(row=8, column=0, sticky="NESW")
        self.label_edit_hcreated_at.grid(row=8, column=1, sticky="NESW")
        self.label_edit_hstart.grid(row=8, column=2, sticky="NESW")
        self.label_edit_hend.grid(row=8, column=3, sticky="NESW")
        self.label_edit_id.grid(row=9, column=0, sticky="NESW")
        #self.label_edit_created.grid(row=9, column=1, sticky="NESW")
        self.container_edit_date.grid(row=9, column=1, sticky="NESW")
        self.combobox_edit_start_h.grid(row=9, column=2, sticky="NESW")
        self.combobox_edit_start_m.grid(row=9, column=3, sticky="NESW")
        self.combobox_edit_end_h.grid(row=10, column=2, sticky="NESW")
        self.combobox_edit_end_m.grid(row=10, column=3, sticky="NESW")
        self.spacer5.grid(row=11, column=0, sticky="NESW")
        self.button_reset.grid(row=12, column=2, sticky="NESW")
        self.button_set_now.grid(row=12, column=1, sticky="NESW")
        self.button_save.grid(row=12, column=3, sticky="NESW")
        self.label_update_message.grid(row=13, column=1, columnspan=2, sticky="NESW")

        self.columnconfigure(0, minsize=100)
        self.columnconfigure(1, minsize=100)
        self.columnconfigure(2, minsize=100)
        self.columnconfigure(3, minsize=100)
        #self.columnconfigure(2, weight=1)
        self.update()


    def update(self, event=None):
        if event!=None:
            self.page_current = 1

        self.update_container()
        self.create_header()
        self.get_entries()
        self.calculate_work_sum()
        self.render_entries()
        self.update_page_count()
        self.configure_buttons()
        self.set_bg_color(self)
        self.set_bg_color(self.container)


    def update_container(self):
        try:
            self.container.destroy()
            self.list_shifts.clear()
        except:
            pass
        self.container = tk.Frame(self, relief="ridge", borderwidth="2")
        self.container.grid(row=1, column=0, columnspan=4, sticky="EW")

        self.container.columnconfigure(0, weight=1)
        self.container.columnconfigure(1, weight=1)
        self.container.columnconfigure(2, weight=1)
        self.container.columnconfigure(3, weight=1)
        self.container.columnconfigure(4, weight=1)


    def create_header(self):
        self.label_id = tk.Label(self.container, text="ID")
        self.label_created_at = tk.Label(self.container, text="STARTING AT")
        self.label_start = tk.Label(self.container, text="START")
        self.label_end = tk.Label(self.container, text="END")
        self.label_worked = tk.Label(self.container, text="WORK TIME")
        
        self.label_id.grid(row=0, column=0, sticky="NESW")
        self.label_created_at.grid(row=0, column=1, sticky="NESW")
        self.label_start.grid(row=0, column=2, sticky="NESW")
        self.label_end.grid(row=0, column=3, sticky="NESW")
        self.label_worked.grid(row=0, column=4, sticky="NESW")


    def get_entries(self):
        result = self.database.write(f"SELECT * FROM {self.config['db_shifts']} WHERE TIME_START >= '{self.get_entries_from_last_x_days(int(self.combobox_filter.get()))}'")
        self.list_shifts = []
        
        for shift in result:
            self.list_shifts.append(shift)


    def calculate_work_sum(self):
        self.work_sum = timedelta(days=0)

        for shift in self.list_shifts:
            self.work_sum += datetime.strptime(shift[3], "%Y-%m-%d %H:%M:%S") - datetime.strptime(shift[2], "%Y-%m-%d %H:%M:%S")

        self.work_sum = int(self.work_sum.total_seconds())
        seconds_in_hour = 3600
        seconds_in_minute = 60
        hours = int(self.work_sum / seconds_in_hour)
        minutes = int(self.work_sum % seconds_in_hour)
        if minutes == 0:
            minutes = "00"
        else:
            minutes = int(minutes / seconds_in_minute)
        self.work_sum = str(hours) + ":" + str(minutes)

    
    def render_entries(self):
        row = 1
        render_list = self.list_shifts[(self.page_current-1)*self.config["shifts_per_page"]:self.page_current*self.config["shifts_per_page"]]
        for shift in render_list:
            id = shift[0]
            created = datetime.strptime(shift[2], "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d")
            start = datetime.strptime(shift[2], "%Y-%m-%d %H:%M:%S").strftime("%H:%M")
            end = datetime.strptime(shift[3], "%Y-%m-%d %H:%M:%S").strftime("%H:%M")
            worked = datetime.strptime(str((datetime.strptime(shift[3], "%Y-%m-%d %H:%M:%S") - datetime.strptime(shift[2], "%Y-%m-%d %H:%M:%S"))), "%H:%M:%S").strftime("%H:%M")

            label_id = id_label(master=self.container, text=id, id=id)
            label_created = id_label(master=self.container, text=created, id=id)
            label_start = id_label(master=self.container, text=start, id=id)
            label_end = id_label(master=self.container, text=end, id=id)
            label_worked = id_label(master=self.container, text=worked, id=id)

            label_id.grid(row=row, column=0)
            label_created.grid(row=row, column=1)
            label_start.grid(row=row, column=2)
            label_end.grid(row=row, column=3)
            label_worked.grid(row=row, column=4)

            row += 1

        while row < self.config["shifts_per_page"]+1:
            label_fill = tk.Label(self.container, text="")
            label_fill.grid(row=row, column=0)
            row += 1

        text_work_sum = tk.Label(self.container, text="Total work sum:")
        label_work_sum = tk.Label(self.container, text=self.work_sum)
        text_work_sum.grid(row=row+1, column=3, sticky="NESW")
        label_work_sum.grid(row=row+1, column=4, sticky="NESW")


    def configure_buttons(self, direction=0):
        if self.page_current+direction >=1 and self.page_current+direction <= self.page_count:
            self.page_current += direction
        
        if self.page_current == 1:
            self.button_prev.configure(state="disabled")
        elif self.page_current > 1:
            self.button_prev.configure(state="active")
        if self.page_current == self.page_count:
            self.button_next.configure(state="disabled")
        elif self.page_current < self.page_count:
            self.button_next.configure(state="active")


    def get_entries_from_last_x_days(self, days: int):
        return datetime.now() - timedelta(days=days)


    def next(self, direction=1):
        self.configure_buttons(direction)
        self.update()
    

    def prev(self, direction=-1):
        self.configure_buttons(direction)
        self.update()


    def update_page_count(self):
        if len(self.list_shifts) % self.config["shifts_per_page"] == 0:
            self.page_count = int(len(self.list_shifts)/self.config["shifts_per_page"])
        else:
            self.page_count = int(len(self.list_shifts)/self.config["shifts_per_page"])+1

        if len(self.list_shifts) == 0:
            self.page_count = 1

        self.label_page_count.configure(text=f"page {self.page_current} of {self.page_count}")

        self.label_total.configure(text=f"{len(self.list_shifts)} total")
   

    def set_bg_color(self, container, color="white"):
        container.configure(bg=color)
        for row in range(100):
            for column in range(100):
                try:
                    widget = container.grid_slaves(row=row, column=column)[0]
                    widget.configure(bg=color)
                except:
                    continue


    def update_shifts(self, id):
        if self.delete_flag == True:
            sql = f"DELETE FROM {self.config['db_shifts']} WHERE SID=={id}"
            self.database.write(sql)
            self.label_update_message.configure(text=f"Log {id} deleted successfully!", fg="green")
            self.update()
            self.delete_flag = False

        elif self.update_flag == True:
            sql = f"SELECT * FROM {self.config['db_shifts']} WHERE SID=={id}"
            result = self.database.write(sql)
            for shift in result:
                created = datetime.strptime(shift[2], "%Y-%m-%d %H:%M:%S")
                start = datetime.strptime(shift[2], "%Y-%m-%d %H:%M:%S")
                end = datetime.strptime(shift[3], "%Y-%m-%d %H:%M:%S")

                self.label_edit_id.configure(text=id)
                self.combobox_edit_year.current(int(created.strftime("%Y"))-int(self.combobox_edit_year["values"][0]))
                self.combobox_edit_month.current(int(created.strftime("%m"))-1)
                self.combobox_edit_day.current(int(created.strftime("%d"))-1)
                #self.label_edit_created.configure(text=created.strftime("%Y-%m-%d"))
                self.combobox_edit_start_h.current(self.combobox_edit_start_h["values"].index(start.strftime("%H")))
                self.combobox_edit_start_m.current(self.combobox_edit_start_m["values"].index(start.strftime("%M")))
                self.combobox_edit_end_h.current(self.combobox_edit_end_h["values"].index(end.strftime("%H")))
                self.combobox_edit_end_m.current(self.combobox_edit_end_m["values"].index(end.strftime("%M")))


    def current_datetime(self):
        pos = 0
        now = datetime.now()
        #date = now.strftime("%Y-%m-%d")
        year = now.strftime("%Y")
        month = now.strftime("%m")
        day = now.strftime("%d")
        hour = int(datetime.now().strftime("%H"))
        minute = int(datetime.now().strftime("%M"))

        if minute % 15 < 15/2:
            pos = int(minute/15)
        else:
            pos = int(minute/15) + 1

        if pos >= len(self.combobox_edit_start_m["values"]):
            pos = int(pos) % 4
            hour = hour + 1

        #self.label_edit_created.configure(text=date)
        self.combobox_edit_year.current(int(year)-int(self.combobox_edit_year["values"][0]))
        self.combobox_edit_month.current(int(month)-1)
        self.combobox_edit_day.current(int(day)-1)
        self.combobox_edit_start_h.current(hour)
        self.combobox_edit_start_m.current(pos)
        self.combobox_edit_end_h.current(hour)
        self.combobox_edit_end_m.current(pos)

    def update_shift(self):
        if self.update_flag == False:
            self.update_flag = True
            self.button_update.configure(bg="lightblue")
        else:
            self.update_flag = False
            self.button_update.configure(bg="white")

    def delete_shift(self):
        if self.delete_flag == False:
            self.delete_flag = True
            self.button_delete.configure(bg="lightblue")
        else:
            self.delete_flag = False
            self.button_delete.configure(bg="white")

    def save_shift(self):
        start = f"{self.combobox_edit_year.get()}-{self.combobox_edit_month.get()}-{self.combobox_edit_day.get()} {self.combobox_edit_start_h.get()}-{self.combobox_edit_start_m.get()}-00"
        start = datetime.strptime(start, "%Y-%m-%d %H-%M-%S")
        end = f"{self.combobox_edit_year.get()}-{self.combobox_edit_month.get()}-{self.combobox_edit_day.get()} {self.combobox_edit_end_h.get()}-{self.combobox_edit_end_m.get()}-00"
        end = datetime.strptime(end, "%Y-%m-%d %H-%M-%S")
        
        if self.label_edit_id["text"] == "0":
            self.database.log_shift(start, end)
            self.label_update_message.configure(text=f"Log added successfully!", fg="green")
        
        elif self.update_flag == True:
            sql = f"UPDATE {self.config['db_shifts']} SET TIME_START='{start}', TIME_END='{end}' WHERE SID=={self.label_edit_id['text']}"
            self.database.write(sql)
            self.update()
            self.update_flag = False

            self.label_update_message.configure(text=f"Log {self.label_edit_id['text']} updated successfully!", fg="green")
        self.reset_edit_fields()
        self.update()


    def reset_edit_fields(self):
        self.label_edit_id.configure(text="0")
        #self.label_edit_created.configure(text="0000-00-00")
        self.combobox_edit_year.current(0)
        self.combobox_edit_month.current(0)
        self.combobox_edit_day.current(0)
        self.combobox_edit_start_h.current(0)
        self.combobox_edit_start_m.current(0)
        self.combobox_edit_end_h.current(0)
        self.combobox_edit_end_m.current(0)

        self.update_flag = False
        self.delete_flag = False
        self.button_delete.configure(bg="white")
        self.button_update.configure(bg="white")

    def __del__(self):
        self.database.disconnect()


class id_label(tk.Label):
    def __init__(self, master, id, text):
        self.master = master
        self.id = id
        self.text = text
        tk.Label.__init__(self, self.master, text=text)
        self.bind("<Button-1>", lambda e: self.master.master.update_shifts(self.id))