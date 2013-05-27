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

        print('Generation %i, max score %i (%i programs), cutoff %i, survivors %i, programs %i'
              % (generation, highest_score, max_count, cutoff, survivors, len(programs_all)))

    def solved(self, generation, programs_all, mutation, mutation_score):
        print(' ')
        print('SOLVED')
        print('Generation %i, score %i, programs %i'
              % (generation, mutation_score, len(programs_all)))
        print(parse.string_from_instructions(mutation))

class Logger(Dummy):
    def __init__(self):
        pass
