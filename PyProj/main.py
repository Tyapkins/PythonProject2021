"""Main module."""

from Main_App import View
import tkinter as tk
import gettext

gettext.install("messages", "./locale", names=("ngettext",))

if __name__ == "__main__":
    root = tk.Tk()
    v = View(master=root)
    root.mainloop()
