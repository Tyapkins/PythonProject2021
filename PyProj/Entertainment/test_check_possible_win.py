import unittest
from unittest.mock import MagicMock
from Tic_tac_toe import check_possible_win


class TestMock(unittest.TestCase):

    def test1(self):
        self.f = MagicMock(return_value=check_possible_win(['   ', 'x', 'o',
                                                            'o', 'x', 'x', 'o',
                                                            'x', '   '], 'x'))
        self.assertEqual(self.f(), -1)

    def test2(self):
        self.f = MagicMock(return_value=check_possible_win(['   ', 'x', 'o',
                                                            'o', 'x', 'x', 'o',
                                                            'x', '   '], 'o'))
        self.assertEqual(self.f(), 0)

    def test3(self):
        self.f = MagicMock(return_value=check_possible_win(['o', '   ', 'o',
                                                            'x', 'x',
                                                            '   ', 'o',
                                                            '   ', 'x'], 'x'))
        self.assertEqual(self.f(), 5)

    def test4(self):
        self.f = MagicMock(return_value=check_possible_win(['o', '   ', 'o',
                                                            'x', 'x',
                                                            '   ', 'o',
                                                            '   ', 'x'], 'o'))
        self.assertEqual(self.f(), 1)

    def test5(self):
        self.f = MagicMock(return_value=check_possible_win(['   ', '   ', 'o',
                                                            'x', '   ',
                                                            '   ', '   ',
                                                            '   ',
                                                            '   '], 'x'))
        self.assertEqual(self.f(), -1)

    def test6(self):
        self.f = MagicMock(return_value=check_possible_win(['   ', '   ', 'o',
                                                            'x', 'x',
                                                            '   ', '   ',
                                                            '   ',
                                                            '   '], 'o'))
        self.assertEqual(self.f(), -1)
