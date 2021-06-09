"""Tic-tac-toe test that checks if someone wins."""

import unittest
from unittest.mock import MagicMock
from Tic_tac_toe import check_win


class TestMock(unittest.TestCase):
    """Tic-tac-toe tests."""

    def test1(self):
        """Player wins."""
        self.f = MagicMock(return_value=check_win(
                           ['   ', 'x', 'o', 'o', 'x', 'x', 'o', 'x', '   ']))
        self.assertEqual(self.f(), True)

    def test2(self):
        """Computer wins, field is not fully filled."""
        self.f = MagicMock(return_value=check_win(
                           ['   ', 'o', 'x', 'x', 'o', 'o', 'x', 'o', 'x']))
        self.assertEqual(self.f(), True)

    def test3(self):
        """Fiels is empty."""
        self.f = MagicMock(return_value=check_win(
                           ['   ', '   ', '   ', '   ',
                            '   ', '   ', '   ', '   ', '   ']))
        self.assertEqual(self.f(), False)

    def test4(self):
        """Little dots."""
        self.f = MagicMock(return_value=check_win(
                           ['   ', 'x', '   ', '   ', 'x',
                            '   ', '   ', 'o', '   ']))
        self.assertEqual(self.f(), False)

    def test5(self):
        """Computer wins, field is filled."""
        self.f = MagicMock(return_value=check_win(
                           ['x', 'o', 'o', 'o', 'x', 'o', 'x', 'x', 'o']))
        self.assertEqual(self.f(), True)
