import sys
import tkinter as tk
from tkinter import ttk
from datetime import datetime
from datetime import timedelta
from database import Database

class Frame_Shift_View(tk.Frame):
    def __init__(self, master, config: dict):
        self.master = master
        self.config = config
        tk.Frame.__init__(self, self.master)
        self.database = Database(config)

        self.frame_shift_list = Frame_Shift_List(self, self.config)
        self.frame_shift_select = Frame_Shift_Select(self, self.config)

        self.frame_shift_list.grid(row=0, column=0, sticky="NESW")
        self.frame_shift_select.grid(row=1, column=0, sticky="NESW")

        self.set_bg_color()

    def show_entries(self):
        pass

    def set_bg_color(self, color="white"):
        self.configure(bg=color)
        for row in range(100):
            for column in range(100):
                try:
                    widget = self.grid_slaves(row=row, column=column)[0]
                    widget.configure(bg=color)
                except:
                    continue

    
class Frame_Shift_List(tk.Frame):
    def __init__(self, master, config: dict):
        self.master = master
        self.config = config
        tk.Frame.__init__(self, self.master)

        self.canvas = tk.Canvas(self, bg="blue")
        self.shifts = tk.Frame(self.canvas, bg="red")
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview, bg="white")
        self.label_id = tk.Label(self, text="ID", bg="white")
        self.label_start = tk.Label(self, text="START", bg="white")
        self.label_end = tk.Label(self, text="END", bg="white")
        self.label_worked = tk.Label(self, text="WORK TIME", bg="white")
        self.label_filter_1 = tk.Label(self, text="Filter last", bg="white")
        self.label_filter_2 = tk.Label(self, text="days", bg="white")
        self.combobox_filter = ttk.Combobox(self, width=5)
        self.label_work_sum = tk.Label(self, bg="white")
        
        self.combobox_filter["values"] = list(range(0, 10001))
        self.combobox_filter.current(30)
        self.combobox_filter.bind("<<ComboboxSelected>>", self.show_entries)
        self.combobox_filter.bind("<Return>", self.show_entries)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.shifts.bind("<Configure>", self.on_frame_configure)
        self.shifts.bind_all("<MouseWheel>", self.on_mouse_wheel)
        self.shifts.bind_all("<Button-4>", self.on_mouse_wheel)
        self.shifts.bind_all("<Button-5>", self.on_mouse_wheel)

        self.label_filter_1.grid(row=0, column=0, sticky="NESW")
        self.combobox_filter.grid(row=0, column=1, sticky="NESW")
        self.label_filter_2.grid(row=0, column=2, sticky="NESW")
        self.label_id.grid(row=1, column=0, sticky="NESW")
        self.label_start.grid(row=1, column=1, sticky="NESW")
        self.label_end.grid(row=1, column=2, sticky="NESW")
        self.label_worked.grid(row=1, column=3, sticky="NESW")
        self.canvas.grid(row=2, column=0, columnspan=4, sticky="NESW")
        self.scrollbar.grid(row=2, column=4, sticky="NS")
        self.label_work_sum.grid(row=3, column=3, sticky="NESW")

        self.canvas.create_window((1, 1), window=self.shifts, anchor="nw", tags="self.shifts")
        self.show_entries()

    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_mouse_wheel(self, event):
        if sys.platform == "linux":
            if event.num == 5 or event.delta < 0:
                self.canvas.yview_scroll(1, "units")
            else:
                self.canvas.yview_scroll(-1, "units")
        elif sys.platform == "win32":
            self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def show_entries(self, event=None):
        result = self.master.database.write(f"SELECT * FROM {self.config['db_shifts']} WHERE TIME_START >= '{datetime.now() - timedelta(days=int(self.combobox_filter.get()))}'")
        self.work_sum = timedelta(days=0)

        for child in self.shifts.winfo_children():
            print(f"Destroying Child {child}")
            child.destroy()

        try:
            self.shift_list.clear()
        except:
            self.shift_list = []

        for shift in result:
            id = shift[0]
            created = datetime.strptime(shift[2], "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d")
            start = datetime.strptime(shift[2], "%Y-%m-%d %H:%M:%S")
            end = datetime.strptime(shift[3], "%Y-%m-%d %H:%M:%S")
            worked = end-start
            self.work_sum += worked
            start = start.strftime("%H:%M")
            end = end.strftime("%H:%M")
            worked = datetime.strptime(str(worked), "%H:%M:%S")
            worked = worked.strftime("%H:%M")

            shift = Shift(self.shifts, id, created, start, end, worked)
            self.shift_list.append(shift)
            self.label_work_sum.configure(text=datetime.strptime(str(self.work_sum), "%H:%M:%S").strftime("%H:%M"))
        
        self.render_shifts()

    def render_shifts(self):
        i = 0
        for shift in self.shift_list:
            shift.grid(row=i, column=0, sticky="NESW")
            shift.configure(width=380)
            self.shifts.configure(width=380)
            i += 1

    def set_bg_color(self, color="white"):
        self.configure(bg=color)
        for row in range(100):
            for column in range(100):
                try:
                    widget = self.grid_slaves(row=row, column=column)[0]
                    widget.configure(bg=color)
                except:
                    continue


class Frame_Shift_Select(tk.Frame):
    def __init__(self, master, config:dict):
        self.master = master
        self.config = config
        tk.Frame.__init__(self, self.master)

class Shift(tk.Frame):
    def __init__(self, master, id, created, start, end, worked):
        self.master = master
        tk.Frame.__init__(self, self.master)
        self.id = id
        self.created = created
        self.start = start
        self.end = end
        self.worked = worked

        self.label_id = tk.Label(self, text=self.id)
        self.label_start = tk.Label(self, text=self.start)
        self.label_end = tk.Label(self, text=self.end)
        self.label_worked = tk.Label(self, text=self.worked)

        self.label_id.grid(row=0, column=0, sticky="NESW")
        self.label_start.grid(row=0, column=1, sticky="NESW")
        self.label_end.grid(row=0, column=2, sticky="NESW")
        self.label_worked.grid(row=0, column=3, sticky="NESW")