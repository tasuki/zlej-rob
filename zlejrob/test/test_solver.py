import unittest

from unittest_data_provider import data_provider

from zlejrob.runner import Runner
from zlejrob.solver import Solver
from zlejrob.test import puzzles

class SolverTest(unittest.TestCase):
    def setUp(self):
        self.solver = Solver(Runner(), {
            'star_score': 2,
            'mutability': 1,
            'offsprings': 100,
            'survivors': 100,
        })

    def test_get_instruction_numbers(self):
        self.assertEqual((0, 1, 10, 11, 12, 30),
                         self.solver.get_instruction_numbers([2,3,0,1,0]))

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
        self.assertEqual(expected, self.solver.get_actions(puzzle))

    def test_mutate(self):
        puzzle = {
            'subs': [3, 4, 0, 0, 0],
            'allowedCommands': 0,
        }
        program = ((), (), (), (), ())
        for i in range(100):
            program = self.solver.mutate(puzzle, program)
        self.assertEqual(3, len(program[0]))
        self.assertEqual(4, len(program[1]))
        self.assertEqual(0, len(program[2]))

    def test_solve(self):
        # TODO
        self.solver.solve(puzzles.puzzles['staircase'])


if __name__ == '__main__':
    unittest.main()
