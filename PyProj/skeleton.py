"""Application Design."""

import tkinter as tk


class Application(tk.Frame):
    """Tkinter skeleton app."""

    def __init__(self, master=None, title="<application>", **kwargs):
        """Create root window with frame, tune weight and resize."""
        super().__init__(master, **kwargs)
        self.master.title(title)
        self.check = False
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        self.grid(sticky="NEWS")
        self.create_widgets()
        for column in range(self.grid_size()[0]):
            for row in range(self.grid_size()[1]):
                self.rowconfigure(row, weight=1)
            self.columnconfigure(column, weight=1)
        master.grid_propagate(0)

    def create_widgets(self):
        """Create all the widgets."""
