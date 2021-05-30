"""Some Games."""
import sys
sys.path.insert(0, '..')
import tkinter as tk
from tkinter import ttk
from skeleton import Application

from PIL import Image, ImageTk
from TagGame import Tags
from Graph import Graph
from Tic_tac_toe import TTT


class Entertainment(Application):
    """Choice of three games."""

    def __init__(self, master=None, mainm=None, **kw):
        """Initialize."""
        master.minsize(1150, 850)
        master.maxsize(1200, 900)
        super().__init__(master=master, **kw)
        self.back = mainm

    def create_widgets(self):
        """Widgets creation."""
        self.TagB = tk.Button(self, text=_("Tag Game"),
                              command=self.BeginTag, justify='center')
        self.TagB.grid(row=0, column=0, sticky="NEWS")

        self.separ = ttk.Separator(self, orient='horizontal')
        self.separ.grid(row=1, column=0, columnspan=5, sticky="WE")

        self.two_separ = ttk.Separator(self, orient='horizontal')
        self.two_separ.grid(row=3, column=0, columnspan=5, sticky="NWE")

        self.one_two_separ = ttk.Separator(self, orient='vertical')
        self.one_two_separ.grid(row=0, column=1, rowspan=3, sticky="NS")

        self.TagIm = ImageTk.PhotoImage((Image.open
                                         ("./Entertainment/pyatna.png")).
                                        resize((200, 200), Image.ANTIALIAS))
        self.TagLab = tk.Label(self, image=self.TagIm, width=200, height=200)
        self.TagLab.grid(row=2, column=0, sticky="N")

        self.GraphB = tk.Button(self, text=_("Simple Graphics"),
                                command=self.BeginGraph)
        self.GraphB.grid(row=0, column=2, sticky="NEWS")

        self.GraphIm = ImageTk.PhotoImage((Image.open
                                           ("./Entertainment/paint.png")).
                                          resize((200, 200), Image.ANTIALIAS))
        self.GraphLab = tk.Label(self, image=self.GraphIm,
                                 width=200, height=200)
        self.GraphLab.grid(row=2, column=2, sticky="N")

        self.two_three_separ = ttk.Separator(self, orient='vertical')
        self.two_three_separ.grid(row=0, column=3, rowspan=3, sticky="NS")

        self.TTTB = tk.Button(self, text=_("Tic-tac-toe"),
                              command=self.BeginTTT)
        self.TTTB.grid(row=0, column=4, sticky="NEWS")

        self.TTTIm = ImageTk.PhotoImage((Image.open
                                         ("./Entertainment/tictactoe.png"))
                                        .resize((200, 200), Image.ANTIALIAS))
        self.TTTLab = tk.Label(self, image=self.TTTIm, width=200, height=200)
        self.TTTLab.grid(row=2, column=4, sticky="N")

        self.QuitB = tk.Button(self, text=_("Quit"), command=self.go_back)
        self.QuitB.grid(row=4, column=0, columnspan=5, sticky="NWE")

        self.menubar = tk.Menu(self)
        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_separator()
        self.filemenu.add_command(label=_("Go to Main Menu"),
                                  command=self.go_back)
        self.filemenu.add_command(label=_("Close"), command=self.quit)
        self.menubar.add_cascade(label=_("Menu"), menu=self.filemenu)

        self.master.config(menu=self.menubar)

    def BeginTag(self):
        """Pick Tags game."""
        top = tk.Toplevel(self)
        top.focus_set()
        top.grab_set()
        game = Tags(top)
        game.grid(row=0, column=0, sticky="NEWS")

    def BeginGraph(self):
        """Pick Graphic redactor."""
        top = tk.Toplevel(self)
        top.focus_set()
        top.grab_set()
        graph = Graph(top)
        graph.grid(row=0, column=0, sticky="NEWS")

    def BeginTTT(self):
        """Pick Tic-Tac-Toe."""
        top = tk.Toplevel(self)
        top.focus_set()
        top.grab_set()
        ttt = TTT(top)
        ttt.grid(row=0, column=0, sticky="NEWS")

    def go_back(self):
        """Return to main menu."""
        self.master.config(menu=tk.Menu())
        self.grid_forget()
        self.back.grid(sticky="NEWS")
