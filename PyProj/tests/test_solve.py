"""Polinom test solutions."""

import unittest
from unittest.mock import MagicMock

import sys

sys.path.insert(0, '../Application')

from Polinoms import solve


class TestMock(unittest.TestCase):
    """Polinom tests."""

    def test1(self):
        """a = b = c = d = e = 0."""
        self.f = MagicMock(return_value=solve(0, 0, 0, 0, 0))
        self.assertEqual(self.f(), "Infinitetly many solutions")

    def test2(self):
        """a = b = c = d = 0, e != 0."""
        self.f = MagicMock(return_value=solve(0, 0, 0, 0, 27))
        self.assertEqual(self.f(), "No solutions")

    def test3(self):
        """Linear equation."""
        self.f = MagicMock(return_value=solve(0, 0, 0, 27, 27))
        self.assertEqual(self.f(), 'x =    -1.0   ')

    def test4(self):
        """Square equation, x1=x2."""
        self.f = MagicMock(return_value=solve(0, 0, 1, -2, 1))
        self.assertEqual(self.f(), 'x =    1.0    ')

    def test5(self):
        """Square equation, x1 != x2."""
        self.f = MagicMock(return_value=solve(0, 0, 2, 4, -6))
        self.assertEqual(self.f(), 'x1 =       -3.0,\nx2 =        1.0')

    def test6(self):
        """Square equatuion, complex solutions."""
        self.f = MagicMock(return_value=solve(0, 0, 1, 2.0, 2.0))
        s = "x1 = -0.9999999999999999 - 1.0        * i,\n"
        s = s+"x2 = -0.9999999999999999 + 1.0        * i"
        self.assertEqual(self.f(), s)

    def test7(self):
        """Cubic equation, one root."""
        self.f = MagicMock(return_value=solve(0, 1, 6, 12, 8))
        self.assertEqual(self.f(), "x =    -2.0   ")

    def test8(self):
        """Cubic equation, two roots."""
        self.f = MagicMock(return_value=solve(0, 1, 4, 5, 2))
        self.assertEqual(self.f(),
                         "x1 =       -2.0,\nx2 = -0.9999999999999999")

    def test_err(self):
        """Incorrect input."""
        with self.assertRaises(TypeError):
            self.f = MagicMock(return_value=solve(0, 1, 10, 24, "qwerty"))
