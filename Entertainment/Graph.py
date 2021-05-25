"""Redactor for text and samples."""
import tkinter as tk
import tkinter.colorchooser as clr


class Application(tk.Frame):
    """Sample tkinter application class."""

    def __init__(self, master=None, title="<application>", **kwargs):
        """Create root window with frame, tune weight and resize."""
        super().__init__(master, **kwargs)
        self.master.title(title)
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        self.grid(sticky="NEWS")
        self.create_widgets()
        for column in range(self.grid_size()[0]):
            self.columnconfigure(column, weight=1)
        for row in range(self.grid_size()[1]):
            self.rowconfigure(row, weight=1)

    def create_widgets(self):
        """.Create all the widgets."""


class Graph(Application):
    """Text and picture redactor."""

    def create_widgets(self):
        """Create fields to fill with text or samples."""
        super().create_widgets()

        self.C = tk.Canvas(self)
        self.C.grid(row=0, column=3, sticky="news",
                    columnspan=6, rowspan=6, ipadx=200)

        self.C.bind("<ButtonPress>", self.BuPress)
        self.C.bind("<ButtonRelease>", self.BuRel)
        self.C.bind("<Motion>", self.Move)

        self.beg_ov = [0, 0]
        self.first_pos = [0, 0]
        self.isPressed = False
        self.Moving = False
        self.obj_id = 0
        self.known_names = ["oval", "rectangle", "arc"]
        self.curr_fill = "green"
        self.curr_border = "black"
        self.num = tk.StringVar()
        self.num.set(1)

        self.cl1 = tk.Button(self, text=_("Fill"), command=self.fill_change)
        self.cl1.grid(row=3, column=0, sticky="NEWS")

        self.cl2 = tk.Button(self, text=_("Border"), command=self.bord_change)
        self.cl2.grid(row=4, column=0, sticky="NEWS")

        self.wdLab = tk.Label(self, text=_("Width:"))
        self.wdLab.grid(row=4, column=1, sticky="E")
        self.entr = tk.Entry(self, textvariable=self.num, width=6)
        self.entr.grid(row=4, column=2, sticky="W", ipady=3)

        self.T = tk.Text(self)
        self.T.grid(row=0, column=0, sticky="NEWS", columnspan=3)

        self.T.bind("<KeyPress>", self.Key)

        self.T.tag_configure('no', foreground='red')

        self.figure = tk.StringVar(self)
        self.figure.set('oval')

        self.chosing = tk.OptionMenu(self, self.figure,
                                     "oval", "rectangle", "arc")
        self.chosing.grid(row=3, column=1, sticky="NEWS")

        self.Q = tk.Button(self, text=_("Quit"), command=self.master.destroy)
        self.Q.grid(row=5, column=0, columnspan=3, sticky="NEWS")

    def bord_change(self):
        """Change border color."""
        self.curr_border = clr.askcolor()[1]

    def fill_change(self):
        """Change fill color."""
        self.curr_fill = clr.askcolor()[1]

    def clear(self):
        """Delete all samples."""
        for i in self.C.find_all():
            self.C.delete(i)

    def BuPress(self, event):
        """Process mouse button click."""
        self.isPressed = True
        self.first_pos = [event.x, event.y]
        self.beg_ov = [event.x, event.y]
        obj_list = self.C.find_overlapping(event.x, event.y, event.x, event.y)
        self.obj_id = obj_list[-1] if obj_list else 0
        if not(self.obj_id):
            new_command = self.C.create_oval if \
                (self.figure.get() == 'oval') else \
                (self.C.create_arc if self.figure.get() == 'arc'
                 else (self.C.create_rectangle
                 if (self.figure.get() == 'rectangle')
                 else self.C.create_line))
            self.obj_id = new_command(event.x, event.y, event.x, event.y,
                                      fill=self.curr_fill,
                                      outline=self.curr_border,
                                      width=self.num.get())
        else:
            self.Moving = True
        self.first_pos = self.C.coords(self.obj_id)

    def BuRel(self, event):
        """Process mouse button release."""
        if not(self.Moving):
            self.C.coords(self.obj_id, (self.beg_ov[0],
                                        self.beg_ov[1], event.x, event.y))
            self.T.insert(tk.END, '{nam} {a} {b} {c} {d} '
                                  'fill="{e}" outline="{f}" width={g}\n'.
                          format(a=self.beg_ov[0],
                                 b=self.beg_ov[1], c=event.x, d=event.y,
                                 e=self.curr_fill, f=self.curr_border,
                                 g=self.num.get(),
                                 nam=self.figure.get()))
        else:
            srchline = "{a} {b} {c} {d}".\
                format(a=int(self.first_pos[0]), b=int(self.first_pos[1]),
                       c=int(self.first_pos[2]), d=int(self.first_pos[3]))
            pam = self.T.search(srchline, '1.0')
            if pam:
                new_cords = self.C.coords(self.obj_id)
                new_line = '{nam} {a} {b} {c} {d}' \
                           'fill="{e}" outline="{f}" width={g}\n'.\
                    format(a=int(new_cords[0]),
                           b=int(new_cords[1]), c=int(new_cords[2]),
                           d=int(new_cords[3]),
                           e=self.curr_fill, f=self.curr_border,
                           g=self.num.get(),
                           nam=self.figure.get())
                self.T.delete(pam[0]+'.0 linestart',
                              str(int(pam[0])+1)+'.0 linestart')
                self.T.insert(pam[0] + '.0 linestart', new_line)
        self.isPressed = False
        self.Moving = False

    def Move(self, event):
        """Move sample with mouse movement."""
        if self.isPressed:
            if not(self.Moving):
                self.C.coords(self.obj_id, self.beg_ov[0],
                              self.beg_ov[1], event.x, event.y)
            else:
                self.C.move(self.obj_id,
                            event.x-self.beg_ov[0], event.y-self.beg_ov[1])
                self.beg_ov[0], self.beg_ov[1] = event.x, event.y

    def Key(self, event):
        """Process text changes."""
        start, end = "insert linestart", "insert lineend"
        check_str = self.T.get(start, end) + event.char
        if self.is_correct(check_str):
            self.T.tag_remove('no', start, end)
        else:
            self.T.tag_add('no', start, end)
        self.run()

    def run(self):
        """Check text lines correction."""
        self.clear()
        lines = self.T.get('0.0', 'end').split('\n')
        for i, line in enumerate(lines):
            if self.is_correct(line) >= 3:
                name, *parameters = line.split()
                try:
                    eval(f"self.C.create_{name}({','.join(parameters)})")
                except Exception:
                    self.T.tag_add('no', str(i+1)+'.0 linestart',
                                   str(i+1)+'.0 lineend')

    def is_correct(self, line):
        """Check line correction."""
        new_line = ''.join(line.split())
        if (not(new_line)):
            return 1
        elif (new_line.startswith('#')):
            return 2
        elif (line.split()[0] in self.known_names):
            return 3
        return False
