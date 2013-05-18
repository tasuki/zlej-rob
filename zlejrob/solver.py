import math
import random

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
        sampled = random.sample(instructions, mutations)

        # TODO refactor clusterfuck
        clusterfuck = [list([None]*i) for i in puzzle['subs']]
        for k,func in enumerate(clusterfuck):
            for i,inst in enumerate(func):
                if k*10 + i in sampled:
                    color = random.choice(self.COLORS)
                    action = random.choice(self.get_actions(puzzle))
                    clusterfuck[k][i] = (color, action, k*10 + i)
                else:
                    try:
                        clusterfuck[k][i] = program[k][i]
                    except:
                        pass

        return tuple(tuple(i for i in func if i != None) for func in clusterfuck)

    def solve(self, puzzle):
        # programs ordered by their score (low scores potentially dropped)
        programs_ordered = [set() for x in range(self.get_max_score(puzzle))]
        programs_ordered[1].add(((), (), (), (), ()))

        total_stars = len([x for x in puzzle['board'] if x in ['R', 'G', 'B']])

        generation = 0
        while True:
            survivors = 0
            generation += 1
            clearing = False
            score = self.get_max_score(puzzle)
            for programs in reversed(programs_ordered):
                score -= 1
                if clearing == True:
                    programs_ordered[score].clear()

                length = len(programs)
                if length == 0: continue

                survivors += length
                if survivors > self.settings['survivors']:
                    if 'debug' in self.settings:
                        print('Generation %i, survivors %i' % (generation, survivors))
                    clearing = True
                    continue # TODO remove lesser solutions from list

                for program in programs:
                    for i in range(self.settings['offsprings']):
                        mutation = self.mutate(puzzle, program)
                        stars, reached, unread = self.runner.run(puzzle, mutation)
                        if stars == total_stars:
                            if 'debug' in self.settings:
                                print(' ')
                                print('SOLVED')
                                print('Generation %i' % generation)
                                print(mutation)
                            return mutation
                        mutation_score = stars*2 + reached - unread*5
                        if mutation_score > score:
                            programs_ordered[mutation_score].add(mutation)

            if 'debug' in self.settings:
                score = self.get_max_score(puzzle)
                for programs in reversed(programs_ordered):
                    score -= 1
                    if len(programs):
                        print('Generation %i, score %i' % (generation, score))
                        #for program in programs:
                        #    print program
                        break
