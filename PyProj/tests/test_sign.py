"""Polinoms test, check sign function."""

import unittest
from unittest.mock import MagicMock
import sys

sys.path.insert(0, '../Application')

from Polinoms import sgn


class TestMock(unittest.TestCase):
    """Polinoms tests."""

    def test1(self):
        """Testing int 0."""
        self.f = MagicMock(return_value=sgn(0))
        self.assertEqual(self.f(), 0)

    def test2(self):
        """Testing positive number."""
        self.f = MagicMock(return_value=sgn(2.3))
        self.assertEqual(self.f(), 1)

    def test3(self):
        """Testing negative number."""
        self.f = MagicMock(return_value=sgn(-3.7))
        self.assertEqual(self.f(), -1)

    def test4(self):
        """Testing float 0."""
        self.f = MagicMock(return_value=sgn(0.0))
        self.assertEqual(self.f(), 0)

    def test_err(self):
        """Incorrect input."""
        with self.assertRaises(TypeError):
            self.f = MagicMock(return_value=sgn("qwerty"))
