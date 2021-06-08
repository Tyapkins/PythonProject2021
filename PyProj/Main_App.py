"""Main Menu."""

import tkinter as tk
import sys
from skeleton import Application

sys.path.insert(0, 'To-Do')
sys.path.insert(0, 'Weather')
sys.path.insert(0, 'Entertainment')
sys.path.insert(0, 'Application')

from To_Do import ToD
from weather import WeatherApp
from Entertainment import Entertainment
from Applications import MathApps


class View(Application):
    """Sample Application."""

    def __init__(self, master=None, **kw):
        """Initializate Main Menu."""
        super().__init__(master, **kw)
        master.minsize(400, 200)
        master.maxsize(600, 300)
        self.create_widgets()

    def create_widgets(self):
        """Widgets creation."""
        """Quit Button."""
        self.quitButton = tk.Button(self, text=_("Quit"), command=self.quit)
        self.quitButton.grid(row=6, columnspan=6, sticky="NEWS")

        """To-Do Button."""
        self.ToDo = tk.Button(self, text=_('To-Do List'), command=self.to_do)
        self.ToDo.grid(row=0, rowspan=3, column=0, columnspan=3, sticky="NEWS")

        """Weather Button."""
        self.Weather = tk.Button(self, text=_('Weather'), command=self.weather)
        self.Weather.grid(row=0,
                          rowspan=3,
                          column=3,
                          columnspan=3,
                          sticky="NEWS")

        """Application Button."""
        self.Applic = tk.Button(self, text=_('Application'), command=self.apps)
        self.Applic.grid(row=3,
                         rowspan=3,
                         column=0,
                         columnspan=3,
                         sticky="NEWS")

        """Entertainment Button."""
        self.Entertainment = tk.Button(self,
                                       text=_('Entertainment'),
                                       command=self.entertain)
        self.Entertainment.grid(row=3,
                                rowspan=3,
                                column=3,
                                columnspan=3,
                                sticky="NEWS")

    def to_do(self):
        """To-Do."""
        print("To-Do!")
        self.grid_forget()
        self.master.minsize(1150, 850)
        self.master.maxsize(1200, 900)
        if (hasattr(self, 'ToD')):
            self.ToD.grid(sticky="NEWS")
            self.master.config(menu=self.ToD.menubar)
        else:
            self.ToD = ToD(master=self.master, mainm=self)

    def weather(self):
        """Weather."""
        print("Weather!")
        self.grid_forget()
        self.master.minsize(1150, 850)
        self.master.maxsize(1200, 900)
        if (hasattr(self, 'WeatherApp')):
            self.WeatherApp.grid(sticky="NEWS")
            self.master.config(menu=self.WeatherApp.menubar)
        else:
            self.WeatherApp = WeatherApp(master=self.master, mainm=self)

    def apps(self):
        """Applications."""
        print("Applications!")
        self.grid_forget()
        self.master.minsize(1150, 850)
        self.master.maxsize(1200, 900)
        if (hasattr(self, 'MathApps')):
            self.MathApps.grid(sticky="NEWS")
            self.master.config(menu=self.MathApps.menubar)
        else:
            self.MathApps = MathApps(master=self.master, mainm=self)

    def entertain(self):
        """Entertainment."""
        print("Entertainment!")
        self.grid_forget()
        self.master.minsize(1150, 850)
        self.master.maxsize(1200, 900)
        if (hasattr(self, 'Entertainments')):
            self.Entertainments.grid(sticky="NEWS")
            self.master.config(menu=self.Entertainments.menubar)
        else:
            self.Entertainments = Entertainment(master=self.master, mainm=self)
