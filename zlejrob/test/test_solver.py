import unittest

from unittest_data_provider import data_provider

from .. import Runner, solve
from . import puzzles

class SolveTest(unittest.TestCase):
    def get_solver(self, puzzle = None):
        return solve.Solver(puzzle, Runner(), {
            'star_score': 4,
            'reached_score': 2,
            'length_penalty': 1,
            'degeneration': 0.3,
            'mutability': 1,
            'offsprings': 100,
            'survivors': 100,
        })

    def test_get_instruction_numbers(self):
        self.assertEqual((0, 1, 10, 11, 12, 30),
                         solve.get_instruction_numbers([2,3,0,1,0]))

    actions = lambda: (
        (['F','L','R','1','2','4'], 0, [3,4,0,1,0]),
        (['F','L','R','1','r'], 1, [3,0,0,0,0]),
        (['F','L','R','1','g'], 2, [3,0,0,0,0]),
        (['F','L','R','1','b'], 4, [3,0,0,0,0]),
        (['F','L','R','1','r','b'], 5, [3,0,0,0,0]),
        (['F','L','R','1','r','g','b'], 7, [3,0,0,0,0]),
    )

    @data_provider(actions)
    def test_get_actions(self, expected, allowed, functions):
        puzzle = {
            'subs': functions,
            'allowedCommands': allowed,
        }
        self.assertEqual(expected, solve.get_actions(puzzle))

    def test_mutate(self):
        puzzle = {
            'subs': [3, 4, 0, 0, 0],
            'allowedCommands': 0,
            'board': [],
        }
        program = ((), (), (), (), ())
        reached_1 = False
        reached_2 = False
        for i in range(100):
            program = self.get_solver(puzzle).mutate(program)
            if len(program[0]) == 3:
                reached_1 = True
            if len(program[1]) == 4:
                reached_2 = True
        self.assertTrue(reached_1)
        self.assertTrue(reached_2)
        self.assertEqual(0, len(program[2]))

    puzzles = lambda: (
        ('staircase',),
        ('colorful_bar',),
    )

    @data_provider(puzzles)
    def test_solve(self, puzzle):
        program = self.get_solver(puzzles.puzzles[puzzle]).solve()


if __name__ == '__main__':
    unittest.main()
