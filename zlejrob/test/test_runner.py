import unittest

from unittest_data_provider import data_provider

from .. import parse, Runner
from ..exceptions import OffTheBoardError
from . import puzzles

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
            self.assertEqual(self.runner.move(position, direction), result)

    def test_turn(self):
        self.assertEqual(self.runner.turn(0, 'R'), 1)
        self.assertEqual(self.runner.turn(0, 'L'), 3)
        self.assertEqual(self.runner.turn(3, 'R'), 0)
        self.assertEqual(self.runner.turn(3, 'L'), 2)

    programs = lambda: (
        # no instructions
        ('staircase', (0, 1), "|||||"),
        # end of instructions
        ('staircase', (1, 2), "_F|||||"),
        # jump off the board
        ('staircase', (1, 2), "_F_F|||||"),
        # go a bit further
        ('staircase', (2, 3), "_F_L_F_F|||||"),
        # infinite loop
        ('staircase', (1, 2), "_F_L_L_1|||||"),
        # success!
        ('staircase', (19, 20), "_F_L_F_R_1|||_F_R||"),
        # fail because of color
        ('staircase', (13, 14), "bFbLbFbRb1|||||"),
        # recursion
        ('arbitrary_counting', (1, 35), "_2_L_F_1|_Fb2_r_F||||"),
        # coloring
        ('colorful_bar', (17, 18), "_FrL_b_1|||||"),
    )

    @data_provider(programs)
    def test_run(self, puzzle_name, expected, program):
        puzzle = puzzles.puzzles[puzzle_name]
        instructions = parse.instructions_from_string(program)

        self.assertEqual(self.runner.run(puzzle, instructions), expected)


if __name__ == '__main__':
    unittest.main()
