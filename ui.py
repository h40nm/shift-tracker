import tkinter as tk
from tkinter import ttk
from config import Config
from db import Database
from frame_add import Frame_Add
from frame_overview import Frame_Overview

from datetime import datetime
from datetime import date

class App():
    def __init__(self):
        self.app = tk.Tk()
        self.config = Config()
        self.frame = tk.Frame(self.app)
        self.spacer1 = tk.Label(self.app, text="", width=int(self.app.winfo_width()/4))
        self.spacer2 = tk.Label(self.app, text="", width=int(self.app.winfo_width()/4))
        self.app.columnconfigure(0, weight=10)
        self.app.columnconfigure(1, weight=1)
        self.app.columnconfigure(2, weight=10)
        self.spacer1.grid(row=0, column=0, sticky="NESW")
        self.spacer2.grid(row=0, column=2, sticky="NESW")
        self.app.config(bg="white")
        self.spacer1.config(bg="white")
        self.spacer2.config(bg="white")

        self.configure_window()
        self.configure_menubar()
        self.show_overview_frame()
        self.app.mainloop()

    def configure_window(self):
        self.app.title(self.config.config_dict["title"])
        x_pos = int((self.app.winfo_screenwidth() - self.config.config_dict['width']) / 2)
        y_pos = int((self.app.winfo_screenheight() - self.config.config_dict['height']) / 2)
        self.app.geometry(f"{self.config.config_dict['width']}x{self.config.config_dict['height']}+{x_pos}+{y_pos}")
        self.app.resizable(False, False)

    def configure_menubar(self):
        self.menubar = tk.Menu(self.app)
        #self.menubar.add_command(label="Add", command=self.show_add_frame)
        self.menubar.add_command(label="Overview", command=self.show_overview_frame)
        self.menubar.add_command(label="Statistics", command=self.show_stats_frame)
        self.menubar.add_command(label="Export", command=self.show_export_frame)
        self.menubar.add_command(label="Quit", command=self.destroy)
        self.app.config(menu = self.menubar)

    def destroy(self):
        self.app.destroy()

    def show_add_frame(self):
        try:
            self.frame.__del__()
        except Exception as e:
            print(e)
        self.frame = Frame_Add(self.app, self.config.get_config())
        self.frame.grid(row=0, column=1, sticky="NESW")

    def show_overview_frame(self):
        try:
            self.frame.__del__()
        except Exception as e:
            print(e)
        self.frame = Frame_Overview(self.app, self.config.get_config())
        #self.frame = frame_edit.Frame_Edit(self.app, self.config.get_config())
        self.frame.grid(row=0, column=1, sticky="EW")

    def show_stats_frame(self) -> tk.Frame:
        self.frame = tk.Frame(self.app)
        label = tk.Label(self.frame, text="Statistiken")
        label.grid(row=0, column=0, sticky="NESW")
        self.frame.grid(row=0, column=1, sticky="NESW")

    def show_export_frame(self) -> tk.Frame:
        self.frame = tk.Frame(self.app)
        label = tk.Label(self.frame, text="Exportieren")
        label.grid(row=0, column=0, sticky="NESW")
        self.frame.grid(row=0, column=1, sticky="NESW")
'''
class Window(Tk):
    def __init__(self) -> None:
            Tk.__init__(self)
            self.protocol("WM_DELETE_WINDOW", self.delete_window)
            
            self.width = 640
            self.height = 480
            self.title = "Arbeitszeit-Tracker"
            geometry = str(self.width) + "x" + str(self.height) + "+0+0"

            self.geometry(geometry)
            self.resizable(False, False)

    def delete_window(self) -> None:
        self.destroy()
'''