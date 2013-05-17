import unittest
import re
import zlejrob.runner
from unittest_data_provider import data_provider

class RunnerTest(unittest.TestCase):
    def setUp(self):
        self.runner = zlejrob.runner.Runner(width = 16, height = 12)

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
                "         BB     "
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
        ('staircase', (1, 2, 0), "_F|||||"),
        ('staircase', (1, 2, 0), "_F_F|||||"),
        #('staircase', (1, 2, 1), "_F_F_F|||||"),
        #('staircase', (2, 3, 0), "_F_L_F_F|||||"),
    )

    @data_provider(programs)
    def test_run(self, puzzle_name, expected, program):
        puzzle = self.puzzles[puzzle_name]

        # Instruction list from string; TODO abstract
        instructions = [list(i) for i in re.split('\|', program)]
        for k,func in enumerate(instructions):
            instructions[k] = [tuple(func[i:i+2]) for i in range(0, len(func), 2)]

        self.assertEquals(self.runner.run(puzzle, instructions), expected)


if __name__ == '__main__':
    unittest.main()
