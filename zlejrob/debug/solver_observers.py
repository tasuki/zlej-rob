import json
import os

from .. import parse

class Dummy:
    def added(self, *args):
        pass
    def generation_finished(self, *args):
        pass
    def solved(self, *args):
        pass

class Printer(Dummy):
    def generation_finished(self, generation, programs_all,
                            programs_ordered, max_score, survivors):
        highest_score = False
        for i,programs in enumerate(reversed(programs_ordered)):
            score = max_score - i - 1
            if len(programs):
                if highest_score == False:
                    highest_score = score
                    max_count = len(programs)
                cutoff = score

        best = next(iter(programs_ordered[highest_score]))
        best = parse.string_from_instructions(best)
        print('Generation %i, max score %i (%i programs), cutoff %i, survivors %i, programs %i, best %s' %
              (generation, highest_score, max_count, cutoff, survivors, len(programs_all), best))

    def solved(self, generation, programs_all, mutation, mutation_score):
        print(' ')
        print('SOLVED')
        print('Generation %i, score %i, programs %i'
              % (generation, mutation_score, len(programs_all)))
        print(parse.string_from_instructions(mutation))

class Logger(Dummy):
    original = ((), (), (), (), ())

    def __init__(self, puzzle, directory):
        os.mkdir(directory)
        self.directory = directory
        self.puzzle = puzzle
        self.history = {}

    def added(self, mutation, score, parent, generation):
        self.history[mutation] = {
            'generation': generation,
            'parent': parent,
            'score': score,
        }

    def generation_finished(self, generation, programs_all,
                            programs_ordered, max_score, survivors):

        programs = {}
        for instructions,info in self.history.items():
            programs[parse.string_from_instructions(instructions)] = {
                'parent': parse.string_from_instructions(info['parent']),
                'generation': info['generation'],
                'score': info['score'],
            }

        data = {
            'puzzle': self.puzzle,
            'programs': programs,
        }

        handle = open('%s/history-%s.js' % (self.directory, generation), 'w');
        handle.write(json.dumps(data))

    def get_history(self):
        return self.history

    def get_program_history(self, program):
        info = [{
            'program': parse.string_from_instructions(program),
            'generation': self.history[program]['generation'],
            'score': self.history[program]['score'],
        }]

        parent = self.history[program]['parent']
        if parent == self.original:
            return info

        return self.get_program_history(parent) + info
