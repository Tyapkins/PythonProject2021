"""Tick-tack-toe test to determine draw."""

import unittest
from unittest.mock import MagicMock
import sys

sys.path.insert(0, '../Entertainment')

from Tic_tac_toe import check_draw


class TestMock(unittest.TestCase):
    """Tick-tack-toe tests."""

    def test1(self):
        """Player wins."""
        self.f = MagicMock(return_value=check_draw(['   ', 'x', 'o', 'o', 'x',
                                                    'x', 'o', 'x', '   ']))
        self.assertEqual(self.f(), False)

    def test2(self):
        """Computer wins."""
        self.f = MagicMock(return_value=check_draw(['   ', 'o', 'x', 'x', 'o',
                                                    'o', 'x', 'o', 'x']))
        self.assertEqual(self.f(), False)

    def test3(self):
        """No dots."""
        self.f = MagicMock(return_value=check_draw(['   ', '   ', '   ', '   ',
                                                    '   ', '   ', '   ',
                                                    '   ', '   ']))
        self.assertEqual(self.f(), False)

    def test4(self):
        """Little dots."""
        self.f = MagicMock(return_value=check_draw(['   ', 'x', '   ', '   ',
                                                    'x', '   ', '   ',
                                                    'o', '   ']))
        self.assertEqual(self.f(), False)

    def test5(self):
        """Field is filled, draw."""
        self.f = MagicMock(return_value=check_draw(['x', 'o', 'x', 'x',
                                                    'o', 'o', 'o', 'x', 'x']))
        self.assertEqual(self.f(), True)

    def test6(self):
        """Field if field, comoputer wins."""
        self.f = MagicMock(return_value=check_draw(['x', 'o', 'o', 'o',
                                                    'x', 'o', 'x', 'x', 'o']))
        self.assertEqual(self.f(), False)
