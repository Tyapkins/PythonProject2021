"""Main module."""

from Main_App import View
import tkinter as tk

if __name__ == "__main__":
    root = tk.Tk()
    v = View(master=root)
    root.mainloop()
