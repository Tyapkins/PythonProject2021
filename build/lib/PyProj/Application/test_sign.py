import unittest
from unittest.mock import MagicMock
from Polinoms import sgn


class TestMock(unittest.TestCase):

    def test1(self):
        self.f = MagicMock(return_value=sgn(0))
        self.assertEqual(self.f(), 0)

    def test2(self):
        self.f = MagicMock(return_value=sgn(2.3))
        self.assertEqual(self.f(), 1)

    def test3(self):
        self.f = MagicMock(return_value=sgn(-3.7))
        self.assertEqual(self.f(), -1)

    def test4(self):
        self.f = MagicMock(return_value=sgn(0.0))
        self.assertEqual(self.f(), 0)

    def test_err(self):
        with self.assertRaises(TypeError):
            self.f = MagicMock(return_value=sgn("qwerty"))
