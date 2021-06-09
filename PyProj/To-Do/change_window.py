"""Reminders manipulation window."""

import tkinter as tk
import datetime
from tkcalendar import DateEntry
import tkinter.messagebox


class change_table(tk.Frame):
    """Class for reminders creation and modification."""

    def __init__(self, master=None, true_master=None, new_num=-1, **kw):
        """Initialize the window."""
        super().__init__(master=true_master, **kw)
        self.master = master
        self.true_master = true_master
        self.num = new_num
        self.create_widg()

    def hour_change(self, movement):
        """Change hour field by these rules."""
        day_delta = datetime.timedelta(days=1)
        where_to = int(movement)
        if (self.hour.get() != ''):
            num = int(self.hour.get())
            if (where_to == -1):
                if (num < 23):
                    self.hour.set(num + 1)
                elif (num == 23):
                    self.hour.set(0)
                    self.cal.set_date(self.cal.get_date() + day_delta)
            elif (where_to == 1):
                if (num > 0):
                    self.hour.set(num - 1)
                elif (num == 0):
                    self.cal.set_date(self.cal.get_date() - day_delta)
                    self.hour.set(23)
        else:
            self.hour.set(0)

    def minute_change(self, movement):
        """Change minutes field by these rules."""
        where_to = int(movement)
        if (self.minute.get() != ''):
            num = int(self.minute.get())
            if (where_to == -1):
                if (num < 59):
                    self.minute.set(num + 1)
                elif (num == 59):
                    self.minute.set(0)
                    self.hour_change(-1)
            elif (where_to == 1):
                if (num > 0):
                    self.minute.set(num - 1)
                elif (num == 0):
                    self.minute.set(59)
                    self.hour_change(1)
        else:
            self.minute.set(0)

    def on_closing(self):
        """Do some actions if window is closing."""
        if self.changed():
            if tk.messagebox.askyesno(_("Quit"),
                                      _("Do you want to quit?\n"
                                        "To save the changes,"
                                        "you have to press OK")):
                self.true_master.destroy()
        else:
            self.true_master.destroy()

    def changed(self):
        """Define if the window content changed."""
        new_time = datetime.time(int(self.hour.get()), int(self.minute.get()))
        new_date = self.cal.get_date()
        in_date = datetime.datetime(new_date.year,
                                    new_date.month,
                                    new_date.day,
                                    new_time.hour,
                                    new_time.minute,
                                    new_time.second)
        return (((self.cur_description) != (
            self.ent.get())) and (
            self.ent.get() != '')) or (
            ' '.join(self.cur_date_time) != str(in_date))\
            and (in_date)

    def create_widg(self):
        """Creation of window widgets."""
        self.tim_lab = tk.Label(self, text=_("Date:"))
        self.tim_lab.grid(row=0, column=0, sticky="NEWS", columnspan=4, padx=4)

        self.cal = DateEntry(self, width=10, background='darkblue',
                             foreground='white', borderwidth=2)
        self.cal.grid(column=3, row=0, sticky="NEWS",
                      columnspan=10, ipady=4, pady=10)

        self.hour = tk.StringVar()
        self.minute = tk.StringVar()

        hours = self.register(self.master.hours)
        minutes = self.register(self.master.minutes)

        self.tim_lab = tk.Label(self, text=_("Time:"))
        self.tim_lab.grid(row=2, column=0, sticky="NEWS", columnspan=3, padx=4)

        self.tim_h = tk.Entry(self, validate='key', textvariable=self.hour,
                              validatecommand=(hours, '%P'),
                              width=2, justify='center')
        self.tim_h.grid(row=2, column=3, sticky="E", ipady=2, pady=10)

        self.hour_scroll = tk.Scrollbar(self, command=self.hour_change)
        self.hour_scroll.grid(row=2, column=4, sticky="E", ipady=0, pady=10)

        self.two_dots = tk.Label(self, text=":")
        self.two_dots.grid(row=2, column=5, sticky="E", ipady=2, pady=10)

        self.tim_m = tk.Entry(self, validate='key', textvariable=self.minute,
                              validatecommand=(minutes, '%P'),
                              width=2, justify='center')
        self.tim_m.grid(row=2, column=6, sticky="E", ipady=2, pady=10)

        self.minute_scroll = tk.Scrollbar(self, command=self.minute_change)
        self.minute_scroll.grid(row=2, column=7, sticky="E", ipady=0, pady=10)

        self.ent_lab = tk.Label(self, text=_("Description:"))
        self.ent_lab.grid(row=3, column=0, columnspan=3, sticky="NEWS", padx=4)

        self.ent = tk.Entry(self, width=10, justify='center')
        self.ent.grid(row=3, column=3, columnspan=10,
                      sticky="NEWS", ipady=5, pady=10)

        self.imp = tk.IntVar()
        self.imp_che = tk.Checkbutton(self, text=_("Important reminder"),
                                      variable=self.imp, onvalue=1, offvalue=0)
        self.imp_che.grid(row=4, column=0, columnspan=8, sticky="NEWS", padx=2)

        if (self.num != -1):
            self.cur_date_time = self.master.mas[4 * self.num + 1].split(' ')
            self.cur_date = self.cur_date_time[0]
            self.cur_time = self.cur_date_time[1]
            cur_hour_min = self.cur_time.split(':')
            cur_hour = cur_hour_min[0]
            cur_min = cur_hour_min[1]
            self.cur_date = self.cur_date.split('-')

            self.cal.set_date(datetime.date(int(self.cur_date[0]),
                                            int(self.cur_date[1]),
                                            int(self.cur_date[2])))
            self.hour.set(cur_hour)
            self.minute.set(cur_min)

            self.cur_description = self.master.mas[4 * self.num + 2]
            self.ent.insert(0, self.cur_description)

            if (4 * self.num + 1 in self.master.imp_list):
                self.imp.set(1)

        self.old_imp = self.imp.get()

        self.B = tk.Button(self, text="OK")
        self.B.grid(row=5, column=0, columnspan=8,
                    sticky="NEWS", padx=2, pady=2)

        if (self.num != -1):
            self.B.configure(command=self.ed_sel)
        else:
            self.B.configure(command=self.add_sel)

    def check_correct(self):
        """Check if the content of window is correct."""
        correct = True
        if not (self.hour.get()) or not (self.minute.get()):
            tk.messagebox.showerror(_("Time Error"),
                                    _("Input hours and minutes!"))
            correct = False
        else:
            self.cur_time = datetime.time(int(self.hour.get()),
                                          int(self.minute.get()))
        if (self.ent.get() == ''):
            tk.messagebox.showerror(_("Description Error"),
                                    _("Input the description!"))
            correct = False
        else:
            self.cur_rem = self.ent.get()
        self.cur_date = self.cal.get_date()
        if (correct):
            self.in_date = datetime.datetime(self.cur_date.year,
                                             self.cur_date.month,
                                             self.cur_date.day,
                                             self.cur_time.hour,
                                             self.cur_time.minute,
                                             self.cur_time.second)
            if (datetime.datetime.now() > self.in_date):
                tkinter.messagebox.showerror(_("Wrong data"),
                                             _("Time travel, huh?\n"
                                               "Why do you need a reminder"
                                               "to a previous events?\n"
                                               "Change the date!"))
                correct = False
        return correct

    def add_sel(self):
        """Add Reminder to the list."""
        if (self.check_correct()):
            if (self.master.Rlist.get(
                    tk.END) == _("There's no reminders yet!")):
                self.master.Rlist.delete(tk.END)
                date_inp = 0
            else:
                date_inp = self.master.date_in(self.in_date)
            self.add_el(date_inp)
            self.master.list.set(self.master.mas)
            self.master.color_change(date_inp, 4)
            self.master.outdated_events()
            if (self.imp.get()):
                self.master.imp_list.append(date_inp + 1)
                self.master.Rlist.itemconfig(date_inp + 1, foreground="red")
                self.master.im_count.set(len(self.master.imp_list))
            self.master.new_num()
            self.master.ev_count.set(len(self.master.mas) // 4)
            self.true_master.destroy()

    def ed_sel(self):
        """Edit the Reminder from the list."""
        if (self.check_correct()):
            self.master.mas[4 * self.num + 1] = str(self.in_date)
            self.master.mas[4 * self.num + 2] = self.cur_rem
            self.master.list.set(self.master.mas)
            if (self.imp.get() != self.old_imp):
                if (self.old_imp == 0):
                    self.master.imp_list.append(4 * self.num + 1)
                else:
                    self.master.imp_list.remove(4 * self.num + 1)
            self.master.set_imp()
            self.master.new_num()
            self.edit_list()
            self.true_master.destroy()

    def edit_list(self):
        """Modify list of all reminders, including important ones."""
        old_date = self.master.mas.index(str(self.in_date))
        if (old_date) in self.master.imp_list:
            self.master.imp_list.remove(old_date)
        del self.master.mas[old_date - 1:old_date + 3]

        self.master.list.set(self.master.mas)

        date_put = self.master.date_in(self.in_date)
        self.add_el(date_put)

        self.master.list.set(self.master.mas)
        forw = 2 * (date_put + 1 < old_date) - 1
        for i in range(len(self.master.imp_list)):
            if (min(old_date,
                    date_put + 1) <= self.master.
                    imp_list[i] <= max(old_date, date_put + 1)):
                self.master.imp_list[i] += forw * 4
        if (self.imp.get()):
            self.master.imp_list.append(date_put + 1)
        self.master.set_imp()

    def add_el(self, date_num):
        """Insert Reminder information into list."""
        self.master.mas.insert(date_num, "")
        self.master.mas.insert(date_num + 1, "{a} {b}".
                               format(a=self.cur_date, b=self.cur_time))
        self.master.mas.insert(date_num + 2, self.cur_rem)
        self.master.mas.insert(date_num + 3, "")
