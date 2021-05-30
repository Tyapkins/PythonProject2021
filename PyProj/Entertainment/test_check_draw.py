import unittest
from unittest.mock import MagicMock
from Tic_tac_toe import check_draw
# from Tic_tac_toe import check_win


class TestMock(unittest.TestCase):

    def test1(self):
        self.f = MagicMock(return_value=check_draw(['   ', 'x', 'o', 'o', 'x',
                                                    'x', 'o', 'x', '   ']))
        self.assertEqual(self.f(), False)

    def test2(self):
        self.f = MagicMock(return_value=check_draw(['   ', 'o', 'x', 'x', 'o',
                                                    'o', 'x', 'o', 'x']))
        self.assertEqual(self.f(), False)

    def test3(self):
        self.f = MagicMock(return_value=check_draw(['   ', '   ', '   ', '   ',
                                                    '   ', '   ', '   ',
                                                    '   ', '   ']))
        self.assertEqual(self.f(), False)

    def test4(self):
        self.f = MagicMock(return_value=check_draw(['   ', 'x', '   ', '   ',
                                                    'x', '   ', '   ',
                                                    'o', '   ']))
        self.assertEqual(self.f(), False)

    def test5(self):
        self.f = MagicMock(return_value=check_draw(['x', 'o', 'x', 'x',
                                                    'o', 'o', 'o', 'x', 'x']))
        self.assertEqual(self.f(), True)

    def test6(self):
        self.f = MagicMock(return_value=check_draw(['x', 'o', 'o', 'o',
                                                    'x', 'o', 'x', 'x', 'o']))
        self.assertEqual(self.f(), False)
