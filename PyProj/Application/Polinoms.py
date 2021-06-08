"""Solve polinoms."""
import tkinter as tk
import tkinter.messagebox
from math import acos, cos, acosh, cosh, asinh, sinh, pi

eps = 0.0000001


def sgn(x):
    """Signum function."""
    if x == 0:
        return 0
    if x > 0:
        return 1
    else:
        return -1


class Polinom(tk.Frame):
    """Polinom class."""

    def __init__(self, master=None):
        """Initialize."""
        tk.Frame.__init__(self, master)
        self.grid(sticky="NEWS")
        self.createWidgets()
        for column in range(self.grid_size()[0]):
            self.columnconfigure(column, weight=1)
        for row in range(self.grid_size()[1]):
            self.rowconfigure(row, weight=1)

    def createWidgets(self):
        """Create main widgets."""
        self.b = tk.Label(self, text="a = ")
        self.b.grid(row=1, column=0, sticky="NEWS")
        self.c = tk.Label(self, text="b = ")
        self.c.grid(row=2, column=0, sticky="NEWS")
        self.d = tk.Label(self, text="c = ")
        self.d.grid(row=3, column=0, sticky="NEWS")
        self.e = tk.Label(self, text="d = ")
        self.e.grid(row=4, column=0, sticky="NEWS")
        self.E2 = tk.Entry(self)
        self.E2.grid(row=1, column=1, sticky="NEWS")
        self.E3 = tk.Entry(self)
        self.E3.grid(row=2, column=1, sticky="NEWS")
        self.E4 = tk.Entry(self)
        self.E4.grid(row=3, column=1, sticky="NEWS")
        self.E5 = tk.Entry(self)
        self.E5.grid(row=4, column=1, sticky="NEWS")
        self.D = tk.Label(self, text="solve for f(x)=ax^3 + bx^2 + c^x + d=0")
        self.D.grid(row=5, columnspan=3, sticky="NEWS")
        self.L = tk.Label(self)
        self.L.grid(row=6, columnspan=3, sticky="NEWS")
        self.B = tk.Button(self, text="Solve", command=self.solver)
        self.B.grid(row=1, column=2, sticky="NEWS")
        self.Q = tk.Button(self, text="Quit", command=self.master.destroy)
        self.Q.grid(row=3, column=2, sticky="NEWS")

    def solver(self):
        """Get coefficients and solve equation."""
        b = self.E2.get()
        c = self.E3.get()
        d = self.E4.get()
        e = self.E5.get()
        if not b:
            b = 0
            self.E2.insert(0, 0)
        if not c:
            c = 0
            self.E3.insert(0, 0)
        if not d:
            d = 0
            self.E4.insert(0, 0)
        if not e:
            e = 0
            self.E5.insert(0, 0)
        # add error handler?
        self.L['text'] = solve(0.0, float(b), float(c), float(d), float(e))


def solve(a, b, c, d, e):
    """Solve equation if coefficients are given."""
    if a == 0:
        if b == 0:
            if c == 0:
                if d == 0:
                    if e:
                        return "No solutions"
                    return "Infinitetly many solutions"
                return "x = {s:^10}".format(s=-e/d)
            D = d ** 2 - 4 * c * e
            x1 = (-d - D ** (1/2))/(2 * c)
            x2 = (-d + D ** (1/2))/(2 * c)
            if (D >= 0):
                if (x1 != x2):
                    return "x1 = {s:>10},\nx2 = {p:>10}".format(s=x1, p=x2)
                else:
                    return "x = {s:^10}".format(s=x1)
            else:
                t = "x1 = {a:>10} - {b:<10} * i,\nx2 = {a:>10} + {b:<10} * i"
                return t.format(a=x2.real, b=x2.imag)
        c = c/b
        d = d/b
        e = e/b
        b = 1
        Q = (c**2 - 3*d)/9
        R = (2*c**3 - 9*c*d + 27*e)/54
        S = Q**3 - R**2
        if -eps < S < eps:
            x1 = -2*R**(1/3)-c/3
            x2 = R**(1/3)-c/3
            if (x1 != x2):
                return "x1 = {s:>10},\nx2 = {p:>10}".format(s=x1, p=x2)
            else:
                return "x = {s:^10}".format(s=x1)
        if S > 0:
            if Q == 0:
                return "x = {s:^10}".format(s=-c/3)
            phi = acos(R/Q**(1/3))
            x1 = -2*Q**(1/2)*cos(phi) - c/3
            x2 = -2*Q**(1/2)*cos(phi + 2*pi/3) - c/3
            x3 = -2*Q**(1/2)*cos(phi - 2*pi/3) - c/3
            t = "x1 = {s:>10},\nx2 = {p:>10},\nx3={r:>10}"
            return t.format(s=x1, p=x2, r=x3)
        else:
            if Q > 0:
                phi = acosh(abs(R) / Q**(1/3)) / 3
                x1 = -2*sgn(R) * Q**(1/2) * cosh(phi) - a/3
                x2_real = sgn(R) * Q**(1/2) * cosh(phi) - a/3
                x2_im = abs(3**(1/2) * Q**(1/2) * sinh(phi))
                t = "x1 = {s:>10},\nx2 = {a:>10} - {b:<10} * i,\n"
                t += "x3 = {a:>10} + {b:<10} * i"
                return t.format(s=x1, a=x2_real, b=x2_im)
            if Q < 0:
                Q = abs(Q)
                phi = asinh(abs(R) / Q**(1/3)) / 3
                x1 = -2*sgn(R) * Q**(1/2) * sinh(phi) - a/3
                x2_real = sgn(R) * Q**(1/2) * sinh(phi) - a/3
                x2_im = abs(3**(1/2) * Q**(1/2) * cosh(phi))
                t = "x1 = {s:>10},\nx2 = {a:>10} - {b:<10} * i,\n"
                t += "x3 = {a:>10} + {b:<10} * i"
                return t.format(s=x1, a=x2_real, b=x2_im)
            else:
                x1 = - (e - c**3/27) - c/3
                x2_real = -(c + x1)/2
                x2_im = (abs((c-3*x1)*(c+x1) - 4*d))**(1/2) / 2
                t = "x1 = {s:>10},\nx2 = {a:>10} - {b:<10} * i,\n"
                t += "x3 = {a:>10} + {b:<10} * i"
                return t.format(s=x1, a=x2_real, b=x2_im)
