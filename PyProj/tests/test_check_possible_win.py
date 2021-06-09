"""Tick-tack-toe test, check field for win."""

import unittest
from unittest.mock import MagicMock
import sys

sys.path.insert(0, '../Entertainment')

from Tic_tac_toe import check_possible_win


class TestMock(unittest.TestCase):
    """Tick-tack-toe tests."""

    def test1(self):
        """Computer can not win."""
        self.f = MagicMock(return_value=check_possible_win(['   ', 'x', 'o',
                                                            'o', 'x', 'x', 'o',
                                                            'x', '   '], 'x'))
        self.assertEqual(self.f(), -1)

    def test2(self):
        """Computer can win by field 0."""
        self.f = MagicMock(return_value=check_possible_win(['   ', 'x', 'o',
                                                            'o', 'x', 'x', 'o',
                                                            'x', '   '], 'o'))
        self.assertEqual(self.f(), 0)

    def test3(self):
        """Computer can win by field 5."""
        self.f = MagicMock(return_value=check_possible_win(['o', '   ', 'o',
                                                            'x', 'x',
                                                            '   ', 'o',
                                                            '   ', 'x'], 'x'))
        self.assertEqual(self.f(), 5)

    def test4(self):
        """Computer can win by field 1."""
        self.f = MagicMock(return_value=check_possible_win(['o', '   ', 'o',
                                                            'x', 'x',
                                                            '   ', 'o',
                                                            '   ', 'x'], 'o'))
        self.assertEqual(self.f(), 1)

    def test5(self):
        """Too little dots."""
        self.f = MagicMock(return_value=check_possible_win(['   ', '   ', 'o',
                                                            'x', '   ',
                                                            '   ', '   ',
                                                            '   ',
                                                            '   '], 'x'))
        self.assertEqual(self.f(), -1)

    def test6(self):
        """Too little dots."""
        self.f = MagicMock(return_value=check_possible_win(['   ', '   ', 'o',
                                                            'x', 'x',
                                                            '   ', '   ',
                                                            '   ',
                                                            '   '], 'o'))
        self.assertEqual(self.f(), -1)
