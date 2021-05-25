"""Play Tags Game."""

import tkinter as tk
import tkinter.messagebox
import random
from math import log10


class Tags(tk.Frame):
    """Tags game with different tag number."""

    def __init__(self, master=None):
        """Initialize (surprise-surprise)."""
        tk.Frame.__init__(self, master)
        # list for numbers of buttons
        self.SIZE = 4
        self.initialize()
        self.grid(sticky="NEWS")
        # all buttons are stored in list
        self.createWidgets()

    def initialize(self):
        """Fill lists as empty."""
        self.mas = [i + 1 for i in range(self.SIZE ** 2)]
        self.Buttons = []

    # function that checks win condition
    def check(self):
        """Check win condition."""
        for i in range(self.SIZE ** 2 - 1):
            if self.Buttons[i]["text"] != str(i + 1):
                return False
        return True

    # function that generates new tag configuration
    def randomize(self):
        """Generate random solvable tag configuration."""
        sum = 1
        while sum % 2:
            # list of numbers from 1 to SIZE**2 is shuffled
            random.shuffle(self.mas)
            # since number SIZE**2 should not
            # be in game, it is replaced with space
            space_num = self.mas.index(self.SIZE ** 2)
            self.Space.grid(row=space_num // self.SIZE + 1,
                            column=space_num % self.SIZE)
            sum = 0
            # computing the check sum
            for i in range(self.SIZE ** 2):
                # for every tag amount of following tags
                # with smaller numbers is computed
                if (self.mas[i] != self.SIZE**2):
                    copy_mas = [k for k in self.mas[:i] if k < self.mas[i]]
                    sum += self.mas[i] - 1 - len(copy_mas)
            # check sum also contains number of space row
            sum += self.Space.grid_info()["row"]
            # if check sum is odd, renew the process

    # generating Buttons list
    def generate(self):
        """Generate tags."""
        for i in range(self.SIZE ** 2):
            # button number is taken from randomly filled list
            self.Buttons.append(tk.Button(self, text=str(self.mas[i]),
                                          height=int(log10(self.SIZE**2)),
                                          width=int(log10(self.SIZE**2))))
            self.Buttons[i].grid(row=i // self.SIZE + 1,
                                 column=i % self.SIZE, sticky="NEWS")
            self.Buttons[i]["command"] = lambda i1=i: \
                self.change_num(
                self.Buttons[i1].grid_info()['column'],
                self.Buttons[i1].grid_info()['row'])
        self.Buttons[self.mas.index(self.SIZE ** 2)].grid_remove()

    def clear(self):
        """Clear the field."""
        for i in range(self.SIZE ** 2):
            self.Buttons[i].grid_forget()
        self.Buttons = []

    def change_num(self, i, j):
        """Generate buttons actions."""
        # new function is generated for every button
        def change():
            """Change tag position."""
            col = self.Space.grid_info()['column']
            ro = self.Space.grid_info()['row']
            empty_num = self.SIZE * (ro - 1) + col
            num = self.SIZE * (j - 1) + i
            # buttons with number num and empty_num swap their positions
            if abs(i - col) + abs(j - ro) == 1:
                self.Buttons[empty_num].grid(column=col, row=ro)
                # instead of swapping buttons, text is swapped
                self.Buttons[empty_num]["text"] = self.Buttons[num]["text"]
                self.Buttons[num]["text"] = ""
                self.Buttons[num].grid_remove()
                self.Space.grid(column=i, row=j)
            # if player wins, message box appears
            if self.check():
                tkinter.messagebox.showinfo(
                    _("Congratulations!"), _("You win!"))
                if tkinter.messagebox.askyesno(
                        _("One more game?"), _("Do you want to play again?")):
                    self.create()
        return change()

    # function for "New" button: refilling the field
    def create(self):
        """Refill the field."""
        self.clear()
        self.randomize()
        self.generate()

    def createWidgets(self):
        """Create window for a game."""
        top = self.winfo_toplevel()
        top.rowconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)

        self.Space = tk.Label(self)

        for i in range(1, self.SIZE + 1):
            self.columnconfigure(i - 1, weight=1)
            self.grid_rowconfigure(i, weight=1)

        self.quitButton = tk.Button(self, text=_('Exit'),
                                    command=self.master.destroy)
        self.NewButton = tk.Button(self, text=_('New'), command=self.create)
        self.SizeButton = tk.Button(self, text=_('Size'),
                                    command=self.change_size)
        self.buttons_grid()

        self.mas = [i + 1 for i in range(self.SIZE ** 2)]
        self.randomize()
        self.generate()

    def buttons_grid(self):
        """Configure buttons position."""
        self.quitButton.grid(row=0, column=(
                             self.SIZE // 3) * 2 + int(
                             self.SIZE % 3 >= 1),
                             columnspan=self.SIZE // 3 + int(
                             self.SIZE % 3 == 2),
                             sticky="NEWS")
        self.NewButton.grid(row=0, column=0, columnspan=self.SIZE // 3 + int(
                            self.SIZE % 3 >= 1), sticky="NEWS")
        self.SizeButton.grid(row=0, column=self.SIZE // 3 + int(
                             self.SIZE % 3 >= 1), columnspan=self.SIZE // 3,
                             sticky="NEWS")

    def change_size(self):
        """Change the number of tags."""
        new_top = tk.Toplevel(self)
        new_top.resizable(False, False)
        new_top.focus_set()
        new_top.grab_set()

        size_label = tk.Label(new_top, text=_("Size:"))
        size_label.grid(row=1, column=0)

        actual_size = tk.IntVar()
        actual_size.set(self.SIZE)

        def size_val():
            """Check correction of tags number."""
            return (3 < actual_size.get() < 20) and (actual_size.get() != '')

        def size_ch(change):
            """Change tags number by one."""
            choose = int(change)
            if (actual_size.get() != ''):
                num = actual_size.get()
                if (choose == -1):
                    if (num < 20):
                        actual_size.set(num+1)
                elif (choose == 1):
                    if (num > 3):
                        actual_size.set(num-1)

        def accept():
            """Generate new size field."""
            new_top.destroy()
            self.clear()
            self.SIZE = actual_size.get()
            self.initialize()
            self.randomize()
            self.generate()
            self.buttons_grid()

        size_change = tk.Entry(new_top, validate='key',
                               textvariable=actual_size,
                               validatecommand=(size_val, '%P'),
                               width=4, justify='center')
        size_change.grid(row=1, column=2, sticky="E",
                         ipady=2, pady=10, columnspan=2)

        hour_scroll = tk.Scrollbar(new_top, command=size_ch)
        hour_scroll.grid(row=1, column=4, sticky="E", ipady=0, pady=10)

        okButton = tk.Button(new_top, text="OK", command=accept)
        okButton.grid(row=2, column=0, columnspan=5, sticky="NEWS")
