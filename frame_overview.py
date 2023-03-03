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

        self.label_filter_1 = tk.Label(self, text="Filter last")
        self.label_filter_2 = tk.Label(self, text="days")
        self.combobox_filter = ttk.Combobox(self, width=5)
        self.combobox_filter["values"] = list(range(0, 10001))
        self.combobox_filter.current(30)
        self.combobox_filter.bind("<<ComboboxSelected>>", self.update)
        self.combobox_filter.bind("<Return>", self.update)

        self.label_filter_1.grid(row=0, column=0, sticky="NESW")
        self.combobox_filter.grid(row=0, column=1, sticky="NESW")
        self.label_filter_2.grid(row=0, column=2, sticky="NESW")

        self.shifts_per_page = 10
        self.page_count = 1
        self.page_current = 1

        self.button_next = tk.Button(self, text="►", command=self.next)
        self.button_prev = tk.Button(self, text="◄", command=self.prev, state="disabled")
        self.label_page_count = tk.Label(self, text=f"page {self.page_current} of {self.page_count}")

        self.button_next.grid(row=2, column=1, sticky="NESW")
        self.button_prev.grid(row=2, column=0, sticky="NESW")
        self.label_page_count.grid(row=2, column=2, sticky="NESW")

        self.label_test = tk.Label(self, text="TEST")
        self.label_test.grid(row=3, column=0, sticky="NESW")
        self.label_test.bind("<Button-1>", lambda e: self.new_window("clicked"))

        self.update()

    def new_window(self, event=None):
        print(event)

    def get_entries(self):
        result = self.database.write(f"SELECT * FROM {self.config['db_shifts']} WHERE TIME_START >= '{self.get_entries_from_last_x_days(int(self.combobox_filter.get()))}'")
        self.list_shifts = []
        
        for shift in result:
            self.list_shifts.append(shift)


    def calculate_work_sum(self):
        self.work_sum = timedelta(days=0)

        for shift in self.list_shifts:
            self.work_sum += datetime.strptime(shift[3], "%Y-%m-%d %H:%M:%S") - datetime.strptime(shift[2], "%Y-%m-%d %H:%M:%S")
        self.work_sum = datetime.strptime(str(self.work_sum), "%H:%M:%S").strftime("%H:%M")

    def render_entries(self):
        row = 1
        render_list = self.list_shifts[(self.page_current-1)*self.shifts_per_page:self.page_current*self.shifts_per_page]
        for shift in render_list:
            id = shift[0]
            created = datetime.strptime(shift[2], "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d")
            start = datetime.strptime(shift[2], "%Y-%m-%d %H:%M:%S").strftime("%H:%M")
            end = datetime.strptime(shift[3], "%Y-%m-%d %H:%M:%S").strftime("%H:%M")
            worked = datetime.strptime(str((datetime.strptime(shift[3], "%Y-%m-%d %H:%M:%S") - datetime.strptime(shift[2], "%Y-%m-%d %H:%M:%S"))), "%H:%M:%S").strftime("%H:%M")

            label_id = tk.Label(self.container, text=id)
            label_created = tk.Label(self.container, text=created)
            label_start = tk.Label(self.container, text=start)
            label_end = tk.Label(self.container, text=end)
            label_worked = tk.Label(self.container, text=worked)

            label_id.bind("<Button-1>", lambda e: self.new_window(id))
            label_created.bind("<Button-1>", lambda e: self.new_window(id))
            label_start.bind("<Button-1>", lambda e: self.new_window(id))
            label_end.bind("<Button-1>", lambda e: self.new_window(id))
            label_worked.bind("<Button-1>", lambda e: self.new_window(id))

            label_id.grid(row=row, column=0)
            label_created.grid(row=row, column=1)
            label_start.grid(row=row, column=2)
            label_end.grid(row=row, column=3)
            label_worked.grid(row=row, column=4)

            row += 1

        while row < self.shifts_per_page+1:
            label_fill = tk.Label(self.container, text="")
            label_fill.grid(row=row, column=0)
            row += 1

        text_work_sum = tk.Label(self.container, text="Total work sum:")
        label_work_sum = tk.Label(self.container, text=self.work_sum)
        text_work_sum.grid(row=row+1, column=3, sticky="NESW")
        label_work_sum.grid(row=row+1, column=4, sticky="NESW")

    def get_entries_from_last_x_days(self, days: int):
        return datetime.now() - timedelta(days=days)
    
    def update(self, event=None):

        if event!=None:
            self.page_current = 1
            self.configure_buttons()

        self.update_container()
        self.create_header()
        self.get_entries()
        self.calculate_work_sum()
        self.render_entries()
        self.update_page_count()
        self.set_bg_color(self)
        self.set_bg_color(self.container)


    def next(self, direction=1):
        self.configure_buttons(direction)
        self.update()
    

    def prev(self, direction=-1):
        self.configure_buttons(direction)
        self.update()


    def update_container(self):
        try:
            self.container.destroy()
            self.list_shifts.clear()
        except:
            pass
        self.container = tk.Frame(self, relief="ridge", borderwidth="2")
        self.container.grid(row=1, column=0, columnspan=4)


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


    def update_page_count(self):
        if len(self.list_shifts) % self.shifts_per_page == 0:
            self.page_count = int(len(self.list_shifts)/self.shifts_per_page)
        else:
            self.page_count = int(len(self.list_shifts)/self.shifts_per_page)+1

        if len(self.list_shifts) == 0:
            self.page_count = 1

        self.label_page_count.configure(text=f"page {self.page_current} of {self.page_count}")


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
    

    def set_bg_color(self, container, color="white"):
        container.configure(bg=color)
        for row in range(100):
            for column in range(100):
                try:
                    widget = container.grid_slaves(row=row, column=column)[0]
                    widget.configure(bg=color)
                except:
                    continue


    def __del__(self):
        self.database.disconnect()