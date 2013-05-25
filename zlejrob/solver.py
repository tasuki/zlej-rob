import math
import random

from . import parse

class Solver:
    COLORS = ('_', 'r', 'g', 'b')

    def __init__(self, runner, settings):
        self.runner = runner
        self.settings = settings

    def get_max_score(self, puzzle):
        """Get maximum possible score for board size."""
        board_size = len(puzzle['board'])
        return 1 + board_size + board_size * self.settings['star_score']

    def get_actions(self, puzzle):
        """Get available actions for a puzzle."""
        # TODO cache per puzzle?
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

    def get_instruction_numbers(self, subs):
        """Get all possible instruction numbers based on function lengths."""
        # TODO cache per puzzle?
        return tuple(10*k + i for k,func in enumerate(subs)
                     for i in range(func))

    def mutate(self, puzzle, program):
        """Create a random mutation of a program."""
        mutations = int(math.ceil(abs(random.gauss(0, 1)) *
                                  self.settings['mutability']))

        instructions = self.get_instruction_numbers(puzzle['subs'])
        if (mutations > len(instructions)):
            mutations = len(instructions)
        sampled = random.sample(instructions, mutations)

        # TODO refactor clusterfuck
        clusterfuck = [list([None]*i) for i in puzzle['subs']]
        for k,func in enumerate(clusterfuck):
            for i,inst in enumerate(func):
                if k*10 + i in sampled:
                    if random.random() < self.settings['degeneration']:
                        clusterfuck[k][i] = None
                    else:
                        color = random.choice(self.COLORS)
                        action = random.choice(self.get_actions(puzzle))
                        clusterfuck[k][i] = (color, action, k*10 + i)
                else:
                    try:
                        clusterfuck[k][i] = program[k][i]
                    except IndexError:
                        pass

        return tuple(tuple(i for i in func if i != None) for func in clusterfuck)

    def solve(self, puzzle):
        # programs ordered by their score (low scores potentially dropped)
        programs_ordered = [set() for x in range(self.get_max_score(puzzle))]
        programs_ordered[1].add(((), (), (), (), ()))
        programs_all = set()

        total_stars = len([x for x in puzzle['board'] if x in ['R', 'G', 'B']])

        generation = 0
        while True:
            survivors = 0
            generation += 1
            clearing = False
            for i,programs in enumerate(reversed(programs_ordered)):
                score = self.get_max_score(puzzle) - i - 1

                if clearing == True:
                    programs_ordered[score].clear()

                length = len(programs)
                if length == 0: continue

                survivors += length
                if survivors > self.settings['survivors']:
                    clearing = True
                    continue

                for program in programs:
                    for i in range(self.settings['offsprings']):
                        while True:
                            mutation = self.mutate(puzzle, program)
                            if mutation not in programs_all: break
                        programs_all.add(mutation)

                        stars, reached = self.runner.run(puzzle, mutation)
                        mutation_score = (stars * self.settings['star_score']
                                          + reached * self.settings['reached_score']
                                          - sum([len(x) for x in mutation]
                                            * self.settings['length_penalty']))
                        if mutation_score > score:
                            programs_ordered[mutation_score].add(mutation)

                        if stars == total_stars:
                            if 'debug' in self.settings:
                                print(' ')
                                print('SOLVED')
                                print('Generation %i, score %i, survivors %i, programs %i'
                                      % (generation, mutation_score, survivors, len(programs_all)))
                                print(parse.string_from_instructions(mutation))
                            return mutation

            if 'debug' in self.settings:
                max_score = False
                for i,programs in enumerate(reversed(programs_ordered)):
                    score = self.get_max_score(puzzle) - i - 1
                    if len(programs):
                        if max_score == False:
                            max_score = score
                            max_count = len(programs)
                        cutoff = score

                print('Generation %i, max score %i (%i programs), cutoff %i, survivors %i, programs %i'
                      % (generation, max_score, max_count, cutoff, survivors, len(programs_all)))
