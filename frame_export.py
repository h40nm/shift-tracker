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