"""Application Design."""
import sys
sys.path.insert(0, '..')
import tkinter as tk
from skeleton import Application
import tkinter.messagebox
import time
from tkinter import ttk
import datetime

from tkcalendar import Calendar, DateEntry
from pygame import mixer

#from Main_App import View

class ToD(Application):
    """Sample Application."""

    def __init__(self, master=None, mainm=None, **kw):
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

        self.Rlist = tk.Listbox(self, listvariable=self.list, yscrollcommand=self.Scroll.set, selectmode=tk.EXTENDED)
        self.Rlist.grid(row=0, column=2, rowspan=6, columnspan=2, sticky="NEWS")
        self.Rlist.configure(justify=tk.CENTER)

        self.Rlist.insert(tk.END, "There's no reminders yet!")

        self.cur_date = datetime.datetime.now().date()
        self.cur_rem = "No reminders!"
        self.cur_time = datetime.datetime.now().time()


        self.Scroll.configure(command=self.Rlist.yview)


        self.sep = tk.Frame(self, width=5, bg="red")
        self.sep.grid(row=0, rowspan=6, column=1, sticky="SN")

        self.near_ev = tk.Label(self, text="Next event:")
        self.near_ev.grid(row=0, column=0, sticky="S")

        self.date_diff = tk.StringVar()
        self.date_diff.set("No events yet!")
        self.near_ev_date = tk.Label(self, textvariable=self.date_diff)
        self.near_ev_date.grid(row=1, column=0, sticky="NS")

        self.evnum = tk.Label(self, text="Number of All Reminders:")
        self.evnum.grid(row=2, column=0, sticky="S")

        self.ev_count = tk.StringVar()
        self.ev_count.set(0)

        self.ev_num = tk.Label(self, textvariable=self.ev_count)
        self.ev_num.grid(row=3, column=0, sticky="NS")

        self.imnum = tk.Label(self, text="Number of Important Reminders:")
        self.imnum.grid(row=4, column=0, sticky="S")

        self.im_count = tk.StringVar()
        self.im_count.set(0)

        self.imp_list = []

        self.im_num = tk.Label(self, textvariable=self.im_count)
        self.im_num.grid(row=5, column=0, sticky="NS")

        self.menubar = tk.Menu(self)
        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Add a Reminder", command=self.add_rem)
        self.filemenu.add_command(label="Edit the Reminder", command=self.ed_rem)
        self.filemenu.add_command(label="Delete the Reminder", command=self.del_rem)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Save Configuration", command=self.to_file)
        self.filemenu.add_command(label="Load Configuration", command=self.from_file)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Change the Sound")
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Go to Main Menu", command=self.go_back)
        self.filemenu.add_command(label="Close", command=self.quit)
        self.menubar.add_cascade(label="Menu", menu=self.filemenu)

        self.master.config(menu=self.menubar)

        self.Rlist.bind("<<ListboxSelect>>", self.full_sel)

        #mixer.init()
        #self.sound = mixer.Sound("sound.wav")

    def full_sel(self, event):
        nums = self.Rlist.curselection()
        normal_nums = set(i//4 for i in nums)
        for num in normal_nums:
            self.Rlist.selection_set(4*num, 4*num+3)

    def set_imp(self):
        for num in range(self.Rlist.size()):
            self.Rlist.itemconfig(num, foreground="black")
        for number in self.imp_list:
            self.Rlist.itemconfig(number, foreground="red")
        self.im_count.set(len(self.imp_list))
        #self.outdated_events()

    def go_back(self):
        """Return to main menu."""
        self.master.config(menu=tk.Menu())
        self.grid_forget()
        self.back.grid(sticky="NEWS")

    def new_num(self):
        nums = self.Rlist.get(1)
        curin_date = datetime.datetime.strptime(nums, "%Y-%m-%d %H:%M:%S")
        ddif = curin_date - datetime.datetime.now()
        hdif = ddif.seconds // 3600
        mdif = ddif.seconds // 60 - 60 * hdif
        self.date_diff.set("{t}\n\n"
                           "{d} days, {h} hours and "
                           "{m} minutes left".format(t=self.Rlist.get(2), d=ddif.days, h=hdif, m=mdif))
        self.ev_count.set(self.Rlist.size() // 4)

    def del_el(self, date_num):
        #mixer.music.play()
        if len(self.mas) > 4*date_num + 1:
            self.mas = self.mas[:4*date_num] + self.mas[4*(date_num+1):]
        else:
            self.mas = self.mas[:4*date_num]


    def color_change(self, date_inp, shift):
        for i in range(len(self.mas)):
            self.Rlist.itemconfig(i, foreground="black")
        for i in range(len(self.imp_list)):
            if (self.imp_list[i] >= date_inp + 1) and (self.imp_list[i] + shift > 0):
                self.imp_list[i] += shift
            self.Rlist.itemconfig(self.imp_list[i], foreground="red")

    def date_in(self, date):
        count = 0
        check = self.Rlist.get(count + 1)
        while (check) and (datetime.datetime.strptime(check, "%Y-%m-%d %H:%M:%S") < date):
            count += 4
            check = self.Rlist.get(count + 1)
        return count

    def ed_rem(self):

        print("Edit!")
        #TODO

    def add_rem(self):

            def add_el(date_num):
                self.mas.insert(date_num, "")
                self.mas.insert(date_num+1, "{a} {b}".format(a=self.cur_date, b=self.cur_time))
                self.mas.insert(date_num+2, self.cur_rem)
                self.mas.insert(date_num+3, "")

            def add_sel():
                if not (hour.get()) or not (minute.get()):
                    tk.messagebox.showerror("Time Error", "Input hours and minutes!")
                else:
                    self.cur_time = datetime.time(int(hour.get()), int(minute.get()))
                if not(ent.get()):
                    tk.messagebox.showerror("Description Error", "Input the description!")
                else:
                    self.cur_rem = ent.get()
                self.cur_date = cal.get_date()
                in_date = datetime.datetime(self.cur_date.year, self.cur_date.month, self.cur_date.day,
                                                                self.cur_time.hour, self.cur_time.minute, self.cur_time.second)
                if (datetime.datetime.now() > in_date):
                    tkinter.messagebox.showerror("Wrong data", "Time travel, huh?\n"
                                                               "Why do you need a reminder to a previous events?\n"
                                                               "Change the date!")
                elif (all([hour.get(), minute.get(), ent.get()])):
                    if (self.Rlist.get(tk.END) == "There's no reminders yet!"):
                        self.Rlist.delete(tk.END)
                        #date_inp = tk.END
                        date_inp = 0
                    else:
                        date_inp = self.date_in(in_date)
                    add_el(date_inp)
                    self.list.set(self.mas)
                    self.color_change(date_inp, 4)
                    self.outdated_events()
                    if (imp.get()):
                        self.imp_list.append(date_inp+1)
                        self.Rlist.itemconfig(date_inp+1, foreground="red")
                        self.im_count.set(len(self.imp_list))
                    self.new_num()
                    self.ev_count.set(len(self.mas)//4)
                    top.destroy()

            def on_closing():
                if tk.messagebox.askyesno("Quit", "Do you want to quit?\nTo save your reminder, you have to press OK"):
                    top.destroy()

            top = tk.Toplevel(self)
            top.resizable(False, False)
            top.protocol("WM_DELETE_WINDOW", on_closing)
            top.focus_set()
            top.grab_set()

            tim_lab = tk.Label(top, text="Choose Date:")
            tim_lab.grid(row=0, column=0, sticky="E", columnspan=4)

            cal = DateEntry(top, width=10, background='darkblue',
                        foreground='white', borderwidth=2)
            cal.grid(column=4, row=0, sticky="NEWS")

            hours = self.register(self.hours)
            minutes = self.register(self.minutes)

            hour = tk.StringVar()
            minute = tk.StringVar()

            tim_lab = tk.Label(top, text="Input Time:")
            tim_lab.grid(row=2, column=0, sticky="E", columnspan=2)

            tim_h = tk.Entry(top, validate='key', textvariable=hour, validatecommand=(hours, '%P'), width=2)
            tim_h.grid(row=2, column=2, sticky="E")

            two_dots = tk.Label(top, text=":")
            two_dots.grid(row=2, column=3, sticky="NEWS")

            tim_m = tk.Entry(top, validate='key', textvariable=minute, validatecommand=(minutes, '%P'), width=2)
            tim_m.grid(row=2, column=4, sticky="W")

            ent_lab = tk.Label(top, text="Input Description:")
            ent_lab.grid(row=3, column=0, columnspan=4, sticky="NEWS")

            ent = tk.Entry(top, width=10)
            ent.grid(row=3, column=4, sticky="NEWS")

            imp = tk.IntVar()
            imp_che = tk.Checkbutton(top, text="Important reminder", variable=imp, onvalue=1, offvalue=0)
            imp_che.grid(row=4, column=0, columnspan=5, sticky="NEWS")

            B = tk.Button(top, text="OK", command=add_sel)
            B.grid(row=5, column=0, columnspan=5, sticky="NEWS")

            top.wait_window()


    def del_rem(self):
        selected = self.Rlist.curselection()
        new_select = set(i//4 for i in selected)
        #self.sound.play(maxtime=4)
        if not(len(new_select)):
            tkinter.messagebox.showerror("Delete Error", "Choose Reminder to Delete!")
        else:
            for i in new_select:
                if (4*i+1) in self.imp_list:
                    self.imp_list.remove(4*i+1)
                self.color_change(4*i+1, -4)
                self.del_el(i)
            self.list.set(self.mas)
            if (self.Rlist.size() == 0):
                self.Rlist.insert(tk.END, "There's no reminders yet!")
                self.date_diff.set("No events yet!")
                self.ev_count.set(0)
            elif (self.Rlist.size() == 1) and (self.Rlist.get(tk.END) == "There's no reminders yet!"):
                tkinter.messagebox.showerror("Delete Error", "There's no reminders yet!")
            else:
                self.new_num()
        self.im_count.set(len(self.imp_list))
        
    def to_file(self):
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





    def hours(self, text):
        return not(text) or ((all([i.isdigit() for i in text]) and (0 <= int(text) <= 23)) and (len(text) <= 2))

    def minutes(self, text):
        return not(text) or ((all([i.isdigit() for i in text]) and (0 <= int(text) <= 59)) and (len(text) <= 2))
