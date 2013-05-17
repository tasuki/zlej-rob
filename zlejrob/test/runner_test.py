import unittest

from unittest_data_provider import data_provider

from zlejrob.runner import Runner
from zlejrob.parser import Parser
from zlejrob.exceptions import OffTheBoardError

class RunnerTest(unittest.TestCase):
    def setUp(self):
        self.runner = Runner(width=16, height=12)

    moves = lambda: (
        # move in the middle
        (36, 0, 37),
        (36, 1, 52),
        (36, 2, 35),
        (36, 3, 20),

        # upper left
        (0, 0,  1),
        (0, 1, 16),
        (0, 2, -1),
        (0, 3, -1),

        # mid sides
        (31, 0, -1),
        (32, 2, -1),

        # edge cases
        ( 15, 3,  -1),
        ( 16, 3,   0),
        (175, 1, 191),
        (176, 1,  -1),
    )

    @data_provider(moves)
    def test_move(self, position, direction, result):
        if result == -1:
            self.assertRaises(OffTheBoardError, self.runner.move, position, direction)
        else:
            self.assertEquals(self.runner.move(position, direction), result)

    def test_turn(self):
        self.assertEquals(self.runner.turn(0, 'R'), 1)
        self.assertEquals(self.runner.turn(0, 'L'), 3)
        self.assertEquals(self.runner.turn(3, 'R'), 0)
        self.assertEquals(self.runner.turn(3, 'L'), 2)

    puzzles = {
        'staircase' : {
            'robotCol': 3,
            'robotRow': 10,
            'robotDir': 0,
            'board': list(
                "                "
                "            BB  "
                "           BB   "
                "          BB    "
                "         BG     "
                "        BB      "
                "       BB       "
                "      BB        "
                "     BB         "
                "    BB          "
                "   bB           "
                "                "
            )
        }
    }

    programs = lambda: (
        ('staircase', (0, 1, 0), "|||||"),
        ('staircase', (1, 2, 0), "_F|||||"),
        ('staircase', (1, 2, 0), "_F_F|||||"),
        ('staircase', (1, 2, 1), "_F_F_F|||||"),
        ('staircase', (2, 3, 0), "_F_L_F_F|||||"),
        ('staircase', (19, 20, 2), "_F_L_F_R_1|||_F_R||"),
        ('staircase', (13, 14, 0), "bFbLbFbRb1|||||"),
    )

    @data_provider(programs)
    def test_run(self, puzzle_name, expected, program):
        puzzle = self.puzzles[puzzle_name]
        p = Parser()
        instructions = p.instructions_from_string(program)

        self.assertEquals(self.runner.run(puzzle, instructions), expected)


if __name__ == '__main__':
    unittest.main()
