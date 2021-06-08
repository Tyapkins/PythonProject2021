import unittest
from unittest.mock import MagicMock
from Polinoms import solve


class TestMock(unittest.TestCase):

    def test1(self):
        self.f = MagicMock(return_value=solve(0, 0, 0, 0, 0))
        self.assertEqual(self.f(), "Infinitetly many solutions")

    def test2(self):
        self.f = MagicMock(return_value=solve(0, 0, 0, 0, 27))
        self.assertEqual(self.f(), "No solutions")

    def test3(self):
        self.f = MagicMock(return_value=solve(0, 0, 0, 27, 27))
        self.assertEqual(self.f(), 'x =    -1.0   ')

    def test4(self):
        self.f = MagicMock(return_value=solve(0, 0, 1, -2, 1))
        self.assertEqual(self.f(), 'x =    1.0    ')

    def test5(self):
        self.f = MagicMock(return_value=solve(0, 0, 2, 4, -6))
        self.assertEqual(self.f(), 'x1 =       -3.0,\nx2 =        1.0')

    def test6(self):
        self.f = MagicMock(return_value=solve(0, 0, 1, 2.0, 2.0))
        s = "x1 = -0.9999999999999999 - 1.0        * i,\n"
        s = s+"x2 = -0.9999999999999999 + 1.0        * i"
        self.assertEqual(self.f(), s)

    def test7(self):
        self.f = MagicMock(return_value=solve(0, 1, 6, 12, 8))
        self.assertEqual(self.f(), "x =    -2.0   ")

    def test8(self):
        self.f = MagicMock(return_value=solve(0, 1, 4, 5, 2))
        self.assertEqual(self.f(),
                         "x1 =       -2.0,\nx2 = -0.9999999999999999")

    def test_err(self):
        with self.assertRaises(TypeError):
            self.f = MagicMock(return_value=solve(0, 1, 10, 24, "qwerty"))
