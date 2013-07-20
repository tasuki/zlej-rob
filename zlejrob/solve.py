import math
import random

from .exceptions import GenerationLimitExceeded

class Solver:
    COLORS = ('_', 'r', 'g', 'b')

    def __init__(self, puzzle, runner, settings):
        """Solver constructor

        Args:
            puzzle: dict, puzzle info
            runner: Runner, puzzle runner
            settings: dict
                star_score: int, points for collecting a star
                reached_score: int, points for reaching a field
                length_penalty: int, minus points for instruction used
                degeneration: float, probability of instruction removal
                mutability: int, number of changed instructions =
                                 = gaus(0,1) * mutability
                offsprings: int, offsprings per parent
                survivors: int, programs surviving
                generation_limit: int, when to give up
        """
        # save params
        self.puzzle = puzzle
        self.runner = runner
        self.settings = settings

        # puzzle properties
        self.actions = get_actions(self.puzzle)
        self.instruction_numbers = get_instruction_numbers(self.puzzle['subs'])

        self.observers = []

    def initialize(self):
        """Initialize global properties"""
        # puzzle properties
        self.total_stars = get_total_stars(self.puzzle['board'])
        self.max_score = get_max_score(self.puzzle['board'],
                                       self.settings['star_score'],
                                       self.settings['reached_score'])

        # all tried programs
        self.programs_all = set()

        # programs ordered by their score (low scores potentially dropped)
        self.programs_ordered = [set() for x in range(self.max_score)]
        self.programs_ordered[1].add(((), (), (), (), ()))

        self.generation = 0

    def attach(self, observer):
        """Attach an observer."""
        self.observers.append(observer)

    def notify(self, event, *args):
        """Notify observers of an event."""
        for observer in self.observers:
            getattr(observer, event)(*args)

    def mutate(self, program):
        """Create a random mutation of a program.

        Args:
            program: tuple
        Returns:
            tuple, mutated program
        """
        mutations = int(math.ceil(abs(random.gauss(0, 1)) *
                                  self.settings['mutability']))

        if (mutations > len(self.instruction_numbers)):
            mutations = len(self.instruction_numbers)
        # randomly choose instructions to be overridden
        sampled = random.sample(self.instruction_numbers, mutations)

        # TODO refactor clusterfuck
        # initialize empty list of functions of appropriate length
        clusterfuck = [list([None]*i) for i in self.puzzle['subs']]
        for k,func in enumerate(clusterfuck):
            for i,inst in enumerate(func):
                if k*10 + i in sampled:
                    # instruction chosen to be altered
                    if random.random() < self.settings['degeneration']:
                        # remove instruction
                        clusterfuck[k][i] = None
                    else:
                        # change instruction to random color and action
                        color = random.choice(self.COLORS)
                        action = random.choice(self.actions)
                        clusterfuck[k][i] = (color, action, k*10 + i)
                else:
                    # inherit instruction from parent program
                    try:
                        clusterfuck[k][i] = program[k][i]
                    except IndexError:
                        pass

        return tuple(tuple(i for i in func if i != None) for func in clusterfuck)

    def get_score(self, mutation, stars, reached):
        """Score a mutation based on reached stars and fields."""
        return (stars * self.settings['star_score']
                + reached * self.settings['reached_score']
                - sum([len(x) for x in mutation]
                  * self.settings['length_penalty']))

    def mutate_and_evaluate(self, program):
        """Create a mutation, check if it solves the puzzle.

        Args:
            program: tuple
        Returns:
            solution or False
        """
        while True:
            mutation = self.mutate(program)
            if mutation not in self.programs_all: break
        self.programs_all.add(mutation)

        stars, reached = self.runner.run(self.puzzle, mutation)
        mutation_score = self.get_score(mutation, stars, reached)

        if mutation_score > self.current_score:
            self.programs_ordered[mutation_score].add(mutation)
            self.notify('added', mutation, mutation_score, program, self.generation)

        if stars == self.total_stars:
            self.notify('solved', self.generation, self.programs_all,
                        mutation, mutation_score)
            return mutation

        return False

    def solve(self):
        """Solve the puzzle."""
        self.initialize()

        while True:
            survivors = 0
            self.generation += 1
            if "generation_limit" in self.settings:
                if self.generation > self.settings['generation_limit']:
                    raise GenerationLimitExceeded('Give it up!')

            clearing = False
            for i,programs in enumerate(reversed(self.programs_ordered)):
                self.current_score = self.max_score - i - 1

                if clearing == True:
                    self.programs_ordered[self.current_score].clear()

                length = len(programs)
                if length == 0: continue

                survivors += length
                if survivors > self.settings['survivors']:
                    clearing = True
                    continue

                for program in programs:
                    for i in range(self.settings['offsprings']):
                        mutation = self.mutate_and_evaluate(program)
                        if mutation != False:
                            return mutation

            self.notify('generation_finished', self.generation,
                        self.programs_all, self.programs_ordered,
                        self.max_score, survivors)

def get_actions(puzzle):
    """Get available actions for the puzzle."""
    actions = ['F', 'L', 'R']

    # function calls
    for k,f in enumerate(puzzle['subs']):
        if f > 0:
            actions.append(str(k + 1))

    # recolorings
    for mask, command in [(1, 'r'), (2, 'g'), (4, 'b')]:
        if puzzle['allowedCommands'] & mask:
            actions.append(command)

    return actions

def get_instruction_numbers(subs):
    """Get all possible instruction numbers based on function lengths."""
    return tuple(10*k + i for k,func in enumerate(subs)
                 for i in range(func))

def get_max_score(board, star_score, reached_score):
    """Get maximum possible score for board size."""
    board_size = len(board)
    return 1 + board_size * reached_score + board_size * star_score

def get_total_stars(board):
    """Get total number of stars on the board."""
    return len([x for x in board if x in ['R', 'G', 'B']])
