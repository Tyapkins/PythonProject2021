"""Tick-Tack-Toe game."""
import tkinter as tk
import tkinter.messagebox
from random import choice


def check_win(table):
    """Check if someone wins."""
    t = (table[0] == table[1] == table[2] and table[0] != '   ')
    t = t or (table[3] == table[4] == table[5] and table[3] != '   ')
    t = t or (table[6] == table[7] == table[8] and table[6] != '   ')
    t = t or (table[0] == table[3] == table[6] and table[0] != '   ')
    t = t or (table[1] == table[4] == table[7] and table[1] != '   ')
    t = t or (table[2] == table[5] == table[8] and table[2] != '   ')
    t = t or (table[0] == table[4] == table[8] and table[0] != '   ')
    t = t or (table[2] == table[4] == table[6] and table[2] != '   ')
    return t
    # return ((table[0] == table[1] == table[2] and table[0] != '   ') or
    #        (table[3] == table[4] == table[5] and table[3] != '   ') or
    #        (table[6] == table[7] == table[8] and table[6] != '   ') or
    #        (table[0] == table[3] == table[6] and table[0] != '   ') or
    #        (table[1] == table[4] == table[7] and table[1] != '   ') or
    #        (table[2] == table[5] == table[8] and table[2] != '   ') or
    #        (table[0] == table[4] == table[8] and table[0] != '   ') or
    #        (table[2] == table[4] == table[6] and table[2] != '   '))


def check_draw(table):
    """Check if it is a draw."""
    t = True and not check_win(table)
    for i in range(9):
        t *= (table[i] == 'x' or table[i] == 'o')
    return t


def check_possible_win(table, var):
    """Try to pick a square for a computer."""
    # horizontally
    if (table[2] == table[1] == var and table[0] == '   '):
        return 0
    if (table[5] == table[4] == var and table[3] == '   '):
        return 3
    if (table[8] == table[7] == var and table[6] == '   '):
        return 6
    if (table[0] == table[2] == var and table[1] == '   '):
        return 1
    if (table[3] == table[5] == var and table[4] == '   '):
        return 4
    if (table[6] == table[8] == var and table[7] == '   '):
        return 7
    if (table[0] == table[1] == var and table[2] == '   '):
        return 2
    if (table[3] == table[4] == var and table[5] == '   '):
        return 5
    if (table[6] == table[7] == var and table[8] == '   '):
        return 8
    # vertically
    if (table[0] == table[3] == var and table[6] == '   '):
        return 6
    if (table[1] == table[4] == var and table[7] == '   '):
        return 7
    if (table[2] == table[5] == var and table[8] == '   '):
        return 8
    if (table[0] == table[6] == var and table[3] == '   '):
        return 3
    if (table[1] == table[7] == var and table[4] == '   '):
        return 4
    if (table[2] == table[8] == var and table[5] == '   '):
        return 5
    if (table[6] == table[3] == var and table[0] == '   '):
        return 0
    if (table[7] == table[4] == var and table[1] == '   '):
        return 1
    if (table[8] == table[5] == var and table[2] == '   '):
        return 2
    # diagonally
    if (table[0] == table[4] == var and table[8] == '   '):
        return 8
    if (table[0] == table[8] == var and table[4] == '   '):
        return 4
    if (table[4] == table[8] == var and table[0] == '   '):
        return 0
    if (table[2] == table[4] == var and table[6] == '   '):
        return 6
    if (table[2] == table[6] == var and table[4] == '   '):
        return 4
    if (table[4] == table[6] == var and table[2] == '   '):
        return 2

    return -1


class TTT(tk.Frame):
    """Game."""

    turn = 1
    table = ['   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ', '   ']

    def __init__(self, master=None):
        """Initialize."""
        self.turn = 1
        self.table = ['   ', '   ', '   ', '   ',
                      '   ', '   ', '   ', '   ', '   ']
        tk.Frame.__init__(self, master)
        self.grid(sticky="NEWS")
        self.createWidgets()
        for column in range(self.grid_size()[0]):
            self.columnconfigure(column, weight=1)
        for row in range(self.grid_size()[1]):
            self.rowconfigure(row, weight=1)

    def new_game(self):
        """Begin new game."""
        self.turn = 1
        self.table = ['   ', '   ', '   ', '   ',
                      '   ', '   ', '   ', '   ', '   ']
        self.createWidgets()

    def end_game(self):
        """End the game."""
        if self.turn == 1:
            tk.messagebox.showinfo(_("Game over"), _("Computer win!"))
        else:
            tk.messagebox.showinfo(_("Game over"), _("Player 1 win!"))

    def finished(self):
        """Check if someone wins or it is a draw."""
        self.Square1 = tk.Button(self, text=self.table[0],
                                 command=self.no_more)
        self.Square2 = tk.Button(self, text=self.table[1],
                                 command=self.no_more)
        self.Square3 = tk.Button(self, text=self.table[2],
                                 command=self.no_more)
        self.Square4 = tk.Button(self, text=self.table[3],
                                 command=self.no_more)
        self.Square5 = tk.Button(self, text=self.table[4],
                                 command=self.no_more)
        self.Square6 = tk.Button(self, text=self.table[5],
                                 command=self.no_more)
        self.Square7 = tk.Button(self, text=self.table[6],
                                 command=self.no_more)
        self.Square8 = tk.Button(self, text=self.table[7],
                                 command=self.no_more)
        self.Square9 = tk.Button(self, text=self.table[8],
                                 command=self.no_more)
        self.Square1.grid(row=1, column=1, sticky="NEWS")
        self.Square2.grid(row=1, column=2, sticky="NEWS")
        self.Square3.grid(row=1, column=3, sticky="NEWS")
        self.Square4.grid(row=2, column=1, sticky="NEWS")
        self.Square5.grid(row=2, column=2, sticky="NEWS")
        self.Square6.grid(row=2, column=3, sticky="NEWS")
        self.Square7.grid(row=3, column=1, sticky="NEWS")
        self.Square8.grid(row=3, column=2, sticky="NEWS")
        self.Square9.grid(row=3, column=3, sticky="NEWS")

    def put_turn(self, num, var):
        """Player's move."""
        finish = False
        self.table[num-1] = var
        if check_win(self.table):
            self.end_game()
            finish = True
        else:
            if check_draw(self.table):
                tk.messagebox.showinfo(_("Game over"), _("It's a draw!"))
                finish = True
        if finish:
            self.finished()

    def ai_move(self, i):
        """Move done by computer."""
        if i == 0:
            var = '   '
            if (self.turn == 2):
                self.Square1 = tk.Button(self, text='o', command=self.no_more)
                self.L = tk.Label(self, text=_('Turn: Player 1'))
                self.L.grid(row=4, columnspan=4, sticky="NEWS")
                self.turn = 1
                var = 'o'
                self.Square1.grid(row=1, column=1, sticky="NEWS")
                self.put_turn(1, var)
        if i == 1:
            var = '   '
            if (self.turn == 2):
                self.Square2 = tk.Button(self, text='o', command=self.no_more)
                self.L = tk.Label(self, text=_('Turn: Player 1'))
                self.L.grid(row=4, columnspan=4, sticky="NEWS")
                self.turn = 1
                var = 'o'
                self.Square2.grid(row=1, column=2, sticky="NEWS")
                self.put_turn(2, var)
        if i == 2:
            var = '   '
            if (self.turn == 2):
                self.Square3 = tk.Button(self, text='o', command=self.no_more)
                self.L = tk.Label(self, text=_('Turn: Player 1'))
                self.L.grid(row=4, columnspan=4, sticky="NEWS")
                self.turn = 1
                var = 'o'
                self.Square3.grid(row=1, column=3, sticky="NEWS")
                self.put_turn(3, var)
        if i == 3:
            var = '   '
            if (self.turn == 2):
                self.Square4 = tk.Button(self, text='o', command=self.no_more)
                self.L = tk.Label(self, text=_('Turn: Player 1'))
                self.L.grid(row=4, columnspan=4, sticky="NEWS")
                self.turn = 1
                var = 'o'
                self.Square4.grid(row=2, column=1, sticky="NEWS")
                self.put_turn(4, var)
        if i == 4:
            var = '   '
            if (self.turn == 2):
                self.Square5 = tk.Button(self, text='o', command=self.no_more)
                self.L = tk.Label(self, text=_('Turn: Player 1'))
                self.L.grid(row=4, columnspan=4, sticky="NEWS")
                self.turn = 1
                var = 'o'
                self.Square5.grid(row=2, column=2, sticky="NEWS")
                self.put_turn(5, var)
        if i == 5:
            var = '   '
            if (self.turn == 2):
                self.Square6 = tk.Button(self, text='o', command=self.no_more)
                self.L = tk.Label(self, text=_('Turn: Player 1'))
                self.L.grid(row=4, columnspan=4, sticky="NEWS")
                self.turn = 1
                var = 'o'
                self.Square6.grid(row=2, column=3, sticky="NEWS")
                self.put_turn(6, var)
        if i == 6:
            var = '   '
            if (self.turn == 2):
                self.Square7 = tk.Button(self, text='o', command=self.no_more)
                self.L = tk.Label(self, text=_('Turn: Player 1'))
                self.L.grid(row=4, columnspan=4, sticky="NEWS")
                self.turn = 1
                var = 'o'
                self.Square7.grid(row=3, column=1, sticky="NEWS")
                self.put_turn(7, var)
        if i == 7:
            var = '   '
            if (self.turn == 2):
                self.Square8 = tk.Button(self, text='o', command=self.no_more)
                self.L = tk.Label(self, text=_('Turn: Player 1'))
                self.L.grid(row=4, columnspan=4, sticky="NEWS")
                self.turn = 1
                var = 'o'
                self.Square8.grid(row=3, column=2, sticky="NEWS")
                self.put_turn(8, var)
        if i == 8:
            var = '   '
            if (self.turn == 2):
                self.Square9 = tk.Button(self, text='o', command=self.no_more)
                self.L = tk.Label(self, text=_('Turn: Player 1'))
                self.L.grid(row=4, columnspan=4, sticky="NEWS")
                self.turn = 1
                var = 'o'
                self.Square9.grid(row=3, column=3, sticky="NEWS")
                self.put_turn(9, var)

    def ai_turn(self):
        """Pick one of computer possible moves."""
        i = check_possible_win(self.table, 'o')
        if i >= 0:
            self.ai_move(i)
        i = check_possible_win(self.table, 'x')
        if i >= 0:
            self.ai_move(i)
        list = []
        for i in range(9):
            if self.table[i] != 'x' or self.table[i] != 'o':
                list.append(i)
        self.ai_move(choice(list))

    def pressed1(self):
        """Press first button."""
        var = '   '
        if (self.turn == 1):
            self.Square1 = tk.Button(self, text='x', command=self.no_more)
            self.L = tk.Label(self, text=_('Turn: Computer'))
            self.L.grid(row=4, columnspan=4, sticky="NEWS")
            self.turn = 2
            var = 'x'
            self.Square1.grid(row=1, column=1, sticky="NEWS")
            self.put_turn(1, var)
            if not check_win(self.table):
                self.ai_turn()

    def pressed2(self):
        """Press second button."""
        var = '   '
        if (self.turn == 1):
            self.Square2 = tk.Button(self, text='x', command=self.no_more)
            self.L = tk.Label(self, text=_('Turn: Computer'))
            self.L.grid(row=4, columnspan=4, sticky="NEWS")
            self.turn = 2
            var = 'x'
            self.Square2.grid(row=1, column=2, sticky="NEWS")
            self.put_turn(2, var)
            if not check_win(self.table):
                self.ai_turn()

    def pressed3(self):
        """Press third button."""
        var = '   '
        if (self.turn == 1):
            self.Square3 = tk.Button(self, text='x', command=self.no_more)
            self.L = tk.Label(self, text=_('Turn: Computer'))
            self.L.grid(row=4, columnspan=4, sticky="NEWS")
            self.turn = 2
            var = 'x'
            self.Square3.grid(row=1, column=3, sticky="NEWS")
            self.put_turn(3, var)
            if not check_win(self.table):
                self.ai_turn()

    def pressed4(self):
        """Press forth button."""
        var = '   '
        if (self.turn == 1):
            self.Square4 = tk.Button(self, text='x', command=self.no_more)
            self.L = tk.Label(self, text=_('Turn: Computer'))
            self.L.grid(row=4, columnspan=4, sticky="NEWS")
            self.turn = 2
            var = 'x'
            self.Square4.grid(row=2, column=1, sticky="NEWS")
            self.put_turn(4, var)
            if not check_win(self.table):
                self.ai_turn()

    def pressed5(self):
        """Press fifth button."""
        var = '   '
        if (self.turn == 1):
            self.Square5 = tk.Button(self, text='x', command=self.no_more)
            self.L = tk.Label(self, text=_('Turn: Computer'))
            self.L.grid(row=4, columnspan=4, sticky="NEWS")
            self.turn = 2
            var = 'x'
            self.Square5.grid(row=2, column=2, sticky="NEWS")
            self.put_turn(5, var)
            if not check_win(self.table):
                self.ai_turn()

    def pressed6(self):
        """Press sixth button."""
        var = '   '
        if (self.turn == 1):
            self.Square6 = tk.Button(self, text='x', command=self.no_more)
            self.L = tk.Label(self, text=_('Turn: Computer'))
            self.L.grid(row=4, columnspan=4, sticky="NEWS")
            self.turn = 2
            var = 'x'
            self.Square6.grid(row=2, column=3, sticky="NEWS")
            self.put_turn(6, var)
            if not check_win(self.table):
                self.ai_turn()

    def pressed7(self):
        """Press seventh button."""
        var = '   '
        if (self.turn == 1):
            self.Square7 = tk.Button(self, text='x', command=self.no_more)
            self.L = tk.Label(self, text=_('Turn: Computer'))
            self.L.grid(row=4, columnspan=4, sticky="NEWS")
            self.turn = 2
            var = 'x'
            self.Square7.grid(row=3, column=1, sticky="NEWS")
            self.put_turn(7, var)
            if not check_win(self.table):
                self.ai_turn()

    def pressed8(self):
        """Press eighth button."""
        var = '   '
        if (self.turn == 1):
            self.Square8 = tk.Button(self, text='x', command=self.no_more)
            self.L = tk.Label(self, text=_('Turn: Computer'))
            self.L.grid(row=4, columnspan=4, sticky="NEWS")
            self.turn = 2
            var = 'x'
            self.Square8.grid(row=3, column=2, sticky="NEWS")
            self.put_turn(8, var)
            if not check_win(self.table):
                self.ai_turn()

    def pressed9(self):
        """Press ninth button."""
        var = '   '
        if (self.turn == 1):
            self.Square9 = tk.Button(self, text='x', command=self.no_more)
            self.L = tk.Label(self, text=_('Turn: Computer'))
            self.L.grid(row=4, columnspan=4, sticky="NEWS")
            self.turn = 2
            var = 'x'
            self.Square9.grid(row=3, column=3, sticky="NEWS")
            self.put_turn(9, var)
            if not check_win(self.table):
                self.ai_turn()

    def no_more(self):
        """No more buttons."""
        pass

    def quit(self):
        """Go to menu."""
        self.turn = 1
        self.table = ['   ', '   ', '   ', '   ',
                      '   ', '   ', '   ', '   ', '   ']
        self.master.destroy()

    def createWidgets(self):
        """Widgets creation."""
        self.Square1 = tk.Button(self, text='   ', command=self.pressed1)
        self.Square2 = tk.Button(self, text='   ', command=self.pressed2)
        self.Square3 = tk.Button(self, text='   ', command=self.pressed3)
        self.Square4 = tk.Button(self, text='   ', command=self.pressed4)
        self.Square5 = tk.Button(self, text='   ', command=self.pressed5)
        self.Square6 = tk.Button(self, text='   ', command=self.pressed6)
        self.Square7 = tk.Button(self, text='   ', command=self.pressed7)
        self.Square8 = tk.Button(self, text='   ', command=self.pressed8)
        self.Square9 = tk.Button(self, text='   ', command=self.pressed9)
        self.quitButton = tk.Button(self, text=_('Quit'), command=self.quit)
        self.newButton = tk.Button(self, text=_('New Game'),
                                   command=self.new_game)
        self.L = tk.Label(self, text=_('Turn: Player 1'))
        self.quitButton.grid(row=0, columnspan=4, sticky="NEWS")
        self.L.grid(row=4, columnspan=4, sticky="NEWS")
        self.newButton.grid(row=5, columnspan=4, sticky="NEWS")
        self.Square1.grid(row=1, column=1, sticky="NEWS")
        self.Square2.grid(row=1, column=2, sticky="NEWS")
        self.Square3.grid(row=1, column=3, sticky="NEWS")
        self.Square4.grid(row=2, column=1, sticky="NEWS")
        self.Square5.grid(row=2, column=2, sticky="NEWS")
        self.Square6.grid(row=2, column=3, sticky="NEWS")
        self.Square7.grid(row=3, column=1, sticky="NEWS")
        self.Square8.grid(row=3, column=2, sticky="NEWS")
        self.Square9.grid(row=3, column=3, sticky="NEWS")
