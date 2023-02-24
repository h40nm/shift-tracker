import tkinter as tk
from config import Config
from logger import Logger
from database import Database

from datetime import datetime

class App():
    def __init__(self):
        self.app = tk.Tk()
        self.config = Config()
        self.Logger = Logger(self.config.get_config())
        self.database = Database(self.config.get_config())

        self.configure_window()
        self.configure_menubar()
        self.show_add_frame()
        self.app.mainloop()

    def configure_window(self):
        self.app.title(self.config.config_dict["title"])
        x_pos = int((self.app.winfo_screenwidth() - self.config.config_dict['width']) / 2)
        y_pos = int((self.app.winfo_screenheight() - self.config.config_dict['height']) / 2)
        self.app.geometry(f"{self.config.config_dict['width']}x{self.config.config_dict['height']}+{x_pos}+{y_pos}")
        self.app.resizable(False, False)

    def configure_menubar(self):
        self.menubar = tk.Menu(self.app)
        self.menubar.add_command(label="Hinzufügen", command=self.show_add_frame)
        self.menubar.add_command(label="Statistik", command=self.show_stats_frame)
        self.menubar.add_command(label="Exportieren", command=self.show_export_frame)
        self.menubar.add_command(label="Beenden", command=self.destroy)
        self.app.config(menu = self.menubar)

    def destroy(self):
        self.app.destroy()

    def change_frame(self, frame: tk.Frame) -> bool:
        self.frame = frame
        self.frame.grid(row=0, column=0, sticky="NESW")

    def show_add_frame(self):
        self.frame = tk.Frame(self.app, background="red")
        label = tk.Label(self.app, text=f"{datetime.now()}")
        label.grid(row=0, column=0, sticky="NESW")
        self.frame.grid(row=0, column=0, sticky="NESW")

    def show_stats_frame(self) -> tk.Frame:
        self.frame = tk.Frame(self.app)
        self.frame.config(background="blue")
        label = tk.Label(self.app, text="Statistiken")
        label.grid(row=0, column=0, sticky="NESW")
        self.frame.grid(row=0, column=0, sticky="NESW")

    def show_export_frame(self) -> tk.Frame:
        self.frame = tk.Frame(self.app)
        label = tk.Label(self.app, text="Exportieren")
        label.grid(row=0, column=0, sticky="NESW")
        self.frame.grid(row=0, column=0, sticky="NESW")
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