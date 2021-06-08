"""To-Do List."""
import sys

import tkinter as tk
import tkinter.messagebox
from tkinter import ttk
import datetime

sys.path.insert(0, '..')
from skeleton import Application
from change_window import change_table


NO_REMINDERS = _("There's no reminders yet!")
NEXT_EV = _("Next event:")
NO_EV = _("No events yet!")
REM_NUM = _("Number of All Reminders:")
IMP_NUM = _("Number of Important Reminders:")
ADD_REM = _("Add a Reminder")
ED_REM = _("Edit the Reminder")
DEL_REM = _("Delete the Reminder")
SAVE_CONF = _("Save Configuration")
LOAD_CONF = _("Load Configuration")
GO_TO_MAIN = _("Go to Main Menu")
CLOSE = _("Close")
MENU_OPEN = _("Menu")


class ToD(Application):
    """Create application with list of Reminders."""

    def __init__(self, master=None, mainm=None, **kw):
        """Initialize To-Do application."""
        super().__init__(master=master, **kw)
        master.minsize(800, 400)
        master.maxsize(1000, 500)
        self.back = mainm
        self.create_widgets()

    def create_widgets(self):
        """Widgets creation."""
        self.Scroll = tk.Scrollbar(self)
        self.Scroll.grid(row=0, rowspan=6, column=4, sticky="NS")

        self.mas = []
        self.list = tk.StringVar(value=self.mas)

        self.Rlist = tk.Listbox(self,
                                listvariable=self.list,
                                yscrollcommand=self.Scroll.set,
                                selectmode=tk.EXTENDED)
        self.Rlist.grid(row=0,
                        column=2,
                        rowspan=6,
                        columnspan=2,
                        sticky="NEWS")

        self.Rlist.configure(justify=tk.CENTER)

        self.Rlist.insert(tk.END, NO_REMINDERS)

        self.cur_date = datetime.datetime.now().date()
        self.cur_rem = "No reminders!"
        self.cur_time = datetime.datetime.now().time()

        self.Scroll.configure(command=self.Rlist.yview)

        self.sep = ttk.Separator(self, orient="vertical")
        self.sep.grid(row=0, rowspan=6, column=1, sticky="SN")

        self.near_ev = tk.Label(self, text=NEXT_EV)
        self.near_ev.grid(row=0, column=0, sticky="S")

        self.date_diff = tk.StringVar()
        self.date_diff.set(NO_EV)
        self.near_ev_date = tk.Label(self, textvariable=self.date_diff)
        self.near_ev_date.grid(row=1, column=0, sticky="NS")

        self.evnum = tk.Label(self, text=REM_NUM)
        self.evnum.grid(row=2, column=0, sticky="S")

        self.ev_count = tk.StringVar()
        self.ev_count.set(0)

        self.ev_num = tk.Label(self, textvariable=self.ev_count)
        self.ev_num.grid(row=3, column=0, sticky="NS")

        self.imnum = tk.Label(self, text=IMP_NUM)
        self.imnum.grid(row=4, column=0, sticky="S")

        self.im_count = tk.StringVar()
        self.im_count.set(0)

        self.imp_list = []

        self.im_num = tk.Label(self, textvariable=self.im_count)
        self.im_num.grid(row=5, column=0, sticky="NS")

        self.menubar = tk.Menu(self)
        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label=ADD_REM, command=self.add_rem)
        self.filemenu.add_command(label=ED_REM, command=self.ed_rem)
        self.filemenu.add_command(label=DEL_REM, command=self.del_rem)
        self.filemenu.add_separator()
        self.filemenu.add_command(label=SAVE_CONF, command=self.to_file)
        self.filemenu.add_command(label=LOAD_CONF, command=self.from_file)
        self.filemenu.add_separator()
        self.filemenu.add_command(label=GO_TO_MAIN, command=self.go_back)
        self.filemenu.add_command(label=CLOSE, command=self.quit)
        self.menubar.add_cascade(label=MENU_OPEN, menu=self.filemenu)

        self.master.config(menu=self.menubar)

        self.Rlist.bind("<<ListboxSelect>>", self.full_sel)

    def full_sel(self, event):
        """Define selection as 4-multiple."""
        nums = self.Rlist.curselection()
        normal_nums = set(i//4 for i in nums)
        for num in normal_nums:
            self.Rlist.selection_set(4*num, 4*num+3)

    def set_imp(self):
        """Recolor all Reminders."""
        for num in range(self.Rlist.size()):
            self.Rlist.itemconfig(num, foreground="black")
        for number in self.imp_list:
            self.Rlist.itemconfig(number, foreground="red")
        self.im_count.set(len(self.imp_list))

    def go_back(self):
        """Return to main menu."""
        self.master.config(menu=tk.Menu())
        self.grid_forget()
        self.back.grid(sticky="NEWS")

    def new_num(self):
        """Find the nearest event."""
        nums = self.Rlist.get(self.out_of_date()+1)
        curin_date = datetime.datetime.strptime(nums, "%Y-%m-%d %H:%M:%S")
        ddif = curin_date - datetime.datetime.now()
        hdif = ddif.seconds // 3600
        mdif = ddif.seconds // 60 - 60 * hdif
        self.date_diff.set(_("{t}\n\n"
                             "{d} days, {h} hours and "
                             "{m} minutes left").format(
                           t=self.Rlist.
                           get(self.out_of_date()+2),
                           d=ddif.days,
                           h=hdif,
                           m=mdif))
        self.ev_count.set(self.Rlist.size() // 4)

    def del_el(self, date_num):
        """Delete selected reminder."""
        if len(self.mas) > 4*date_num + 1:
            self.mas = self.mas[:4*date_num] + self.mas[4*(date_num+1):]
        else:
            self.mas = self.mas[:4*date_num]
        self.remove_outdated(4*date_num,
                             self.out_of_date(),
                             self.out_of_date()-4)

    def remove_outdated(self, date, counter, bottom_line):
        """Delete oudated reminders."""
        if (counter > date):
            for num in range(bottom_line, counter):
                self.Rlist.itemconfig(num, bg="white")

    def color_change(self, date_inp, shift):
        """Insert new reminder with saving others' colors."""
        for i in range(len(self.mas)):
            self.Rlist.itemconfig(i, foreground="black")
        for i in range(len(self.imp_list)):
            if (self.imp_list[i] >= date_inp + 1)\
                    and (self.imp_list[i] + shift > 0):
                self.imp_list[i] += shift
            self.Rlist.itemconfig(self.imp_list[i], foreground="red")

    def date_in(self, date):
        """Find the place for new reminder."""
        count = 0
        check = self.Rlist.get(count + 1)
        while (check) and \
                (datetime.datetime.strptime(check,
                                            "%Y-%m-%d %H:%M:%S") < date):
            count += 4
            check = self.Rlist.get(count + 1)
        return count

    def ed_rem(self):
        """Edit selected reminder."""
        selected = self.Rlist.curselection()
        new_select = set(i // 4 for i in selected)
        if not (len(new_select)):
            tkinter.messagebox.showerror(_("Edit Error"),
                                         _("Choose Reminder to Edit!"))

        elif (len(new_select) == 1):

            num = new_select.pop()

            ed_top = tk.Toplevel(self)
            table = change_table(master=self, true_master=ed_top, new_num=num)

            ed_top.resizable(False, False)
            ed_top.protocol("WM_DELETE_WINDOW", table.on_closing)
            ed_top.focus_set()
            ed_top.grab_set()

            table.grid(row=0, column=0)

            ed_top.wait_window()

    def add_rem(self):
        """Add new reminder."""
        top = tk.Toplevel(self)
        table = change_table(master=self, true_master=top)
        top.resizable(False, False)
        top.protocol("WM_DELETE_WINDOW", table.on_closing)
        top.focus_set()
        top.grab_set()

        table.grid(row=0, column=0)

        top.wait_window()

    def del_rem(self):
        """Delete selected reminder."""
        selected = self.Rlist.curselection()
        new_select = set(i//4 for i in selected)
        if not(len(new_select)):
            tkinter.messagebox.showerror(_("Delete Error"),
                                         _("Choose Reminder to Delete!"))
        else:
            for i in new_select:
                if (4*i+1) in self.imp_list:
                    self.imp_list.remove(4*i+1)
                self.color_change(4*i+1, -4)
                self.del_el(i)
            self.list.set(self.mas)
            if (self.Rlist.size() == 0):
                self.Rlist.insert(tk.END, NO_REMINDERS)
                self.date_diff.set(NO_EV)
                self.ev_count.set(0)
            elif (self.Rlist.size() == 1) and\
                    (self.Rlist.get(tk.END) == NO_REMINDERS):
                tkinter.messagebox.showerror("Delete Error", NO_REMINDERS)
            else:
                self.new_num()
        self.im_count.set(len(self.imp_list))
        self.outdated_events()

    def out_of_date_vars(self):
        """Count outdated events."""
        count = self.out_of_date()
        if (count):
            self.ev_count.set(self.ev_count.get()[0])
            self.ev_count.set(self.ev_count.get() + _(", and {a} "
                                                      "of them outdated").
                              format(a=count//4))
            im_out = len([ev for ev in range(1, count, 4)
                          if ev in self.imp_list])
            self.im_count.set(self.im_count.get()[0])
            if (im_out):
                self.im_count.set(self.im_count.get() + _(", and {a} "
                                                          "of them outdated").
                                  format(a=im_out))

    def to_file(self):
        """Write configuration to file."""
        got_date = False
        date = ''
        important = False
        with open('test.txt', 'w') as f:
            for num, elem in enumerate(self.Rlist.get(0, self.Rlist.size())):
                if (elem != ''):
                    if (got_date):
                        f.write(date+';'+elem+';'+str(important)+'\n')
                        got_date = False
                    else:
                        date = elem
                        important = int(num in self.imp_list)
                        got_date = True

    def from_file(self):
        """Read configuration from file."""
        events = []
        self.imp_list = []
        num = 0
        with open('test.txt', 'r') as f:
            for line in f:
                events.append('')
                new_mas = line.split(';')
                events.append(new_mas[0])
                events.append(new_mas[1])
                events.append('')
                if (int(new_mas[2])):
                    if 4*num+1 not in self.imp_list:
                        self.imp_list.append(4*num+1)
                num += 1
        self.mas = events
        self.list.set(self.mas)
        self.set_imp()
        self.new_num()
        retired = self.out_of_date()
        if (retired):
            if tk.messagebox.askyesno(_("Out Of Date"),
                                      _("Some of Reminders are out of date."
                                        "\nDo you want to delete them?")):
                self.mas = self.mas[retired:]
                self.list.set(self.mas)
                to_delete = set()
                for i in range(len(self.imp_list)):
                    if (self.imp_list[i] < retired):
                        to_delete.add(i)
                    else:
                        self.imp_list[i] -= retired
                for num in to_delete:
                    self.imp_list.pop(num)
                self.set_imp()
                self.remove_outdated(-1, self.Rlist.size(), 0)
                self.ev_count.set(self.Rlist.size()//4)
            else:
                self.outdated_events()

    def out_of_date(self):
        """Define outadted events."""
        return self.date_in(datetime.datetime.now())

    def outdated_events(self):
        """Recolor outdated events."""
        outdate = self.out_of_date()
        for num in range(outdate):
            self.Rlist.itemconfig(num, bg="lightgray", foreground="gray")
            if num in self.imp_list:
                self.Rlist.itemconfig(num, foreground="tomato")
        self.out_of_date_vars()

    def hours(self, text):
        """Check hours field."""
        return not(text) or ((all([i.isdigit()
                             for i in text]) and (0 <= int(text) <= 23)) and (
                             len(text) <= 2))

    def minutes(self, text):
        """Check minutes field."""
        return not(text) or ((all([i.isdigit()
                              for i in text]) and (0 <= int(text) <= 59)) and (
                             len(text) <= 2))
