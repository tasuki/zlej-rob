import os
import os.path
import time

from zlejrob import exceptions, parse, Solver
from zlejrob.debug import solver_observers

class Zlo:
    """Glue for zlejrob components, IO-heavy hence the name

    Contains convenience functions, the most useful being:
        - fetch_solve_submit: solving an individual puzzle
        - solve_unsolved_puzzles: solving a whole bunch of puzzles
    """

    def __init__(self, client, runner, solver_config,
                 datadir='data', log=False):
        """Constructor of evil

        Args:
            client: RoboZZle Client
            runner: puzzle runner
            solver_config: dictionary of solver parameters
            datadir: directory to store various files, created if not exists
            log: should debug information be logged?
        """
        self.client = client
        self.runner = runner
        self.solcon = solver_config
        self.datadir = datadir
        self.log = log
        self.make_dirs()

    def make_dirs(self):
        """Create data directories if they don't exist"""
        for directory in [self.datadir + '/debug',
                          self.datadir + '/puzzles',
                          self.datadir + '/solutions']:
            try:
                os.makedirs(directory)
            except OSError:
                pass

    def fetch_puzzle(self, puzzle_id):
        """Fetch puzzle of id and save to file"""
        print(' ')
        print('==============')
        puzzle_id = str(puzzle_id)
        fname = self.datadir + '/puzzles/%s.js' % puzzle_id

        if os.path.isfile(fname):
            print('Puzzle %s already in %s.' % (puzzle_id, fname))
            return

        print('Getting puzzle ' + puzzle_id)
        puzzle = None
        while puzzle is None:
            try:
                puzzle = self.client.get_puzzle(puzzle_id)
            except:
                print(('Failed getting puzzle %s, ' \
                     + 'will retry in 10 seconds.') % puzzle_id)
                time.sleep(10)

        f = open(fname, 'w')
        f.write(puzzle)
        f.close()

    def solve(self, puzzle):
        """Solve puzzle from string"""
        solver = Solver(puzzle, self.runner, self.solcon)

        if self.log:
            directory = self.datadir + '/debug/' + \
                        time.strftime("%Y-%m-%d_%H:%M:%S")
            solver.attach(solver_observers.Logger(puzzle, directory))

        solver.attach(solver_observers.Printer(puzzle))
        return solver.solve()

    def solve_puzzle_file(self, puzzle_id):
        """Load a puzzle from file and solve it

        Returns:
            solution string or None
        """
        puzzle_file = str(puzzle_id) + '.js'
        json = open(self.datadir + '/puzzles/' + puzzle_file, 'r').read()
        puzzle = parse.puzzle_from_json(json)

        try:
            solution = parse.string_from_instructions(self.solve(puzzle))
        except (exceptions.GenerationLimitExceeded):
            print('Generation limit exceeded, aborting.')
        else:
            f = open(self.datadir + '/solutions/' + puzzle_file, 'w')
            f.write(solution)
            f.close()
            return solution

    def submit(self, puzzle_id, solution):
        """Submit a puzzle solution to the website"""
        while True:
            try:
                self.client.submit(puzzle_id, solution)
                break
            except:
                print(('Failed submitting puzzle %s, ' \
                     + 'will retry in 10 seconds.') % puzzle_id)
                time.sleep(10)

    def fetch_solve_submit(self, puzzle_id):
        """Fetch a puzzle from the website, solve it, and submit solution

        Prints debug info to stdout.

        Args:
            puzzle_id: a numeric id of the puzzle
        """
        self.fetch_puzzle(puzzle_id)
        solution = self.solve_puzzle_file(puzzle_id)
        if solution:
            self.submit(puzzle_id, solution)

    def solve_unsolved_puzzles(self, sort_by='campaign', skip_until=None):
        """Fetch a list of puzzles, solve them, and submit their solutions

        Prints debug info to stdout.

        Args:
            sort_by: as in http://robozzle.com/js/index.aspx?sortby=difficulty
            skip_until: puzzle id, ignore all puzzles before encountering it
        """
        for puzzle in self.client.get_puzzlelist(sort_by=sort_by):
            if skip_until:
                if puzzle['id'] == str(skip_until):
                    skip_until = False
                else:
                    print('Continuing ' + puzzle['id'])
                    continue

            if puzzle['solved'] == 'X':
                print(' ')
                print("Skipping puzzle %s - it's already been solved." \
                      % (puzzle['id']))
                continue

            self.fetch_solve_submit(puzzle['id'])
