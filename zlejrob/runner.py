import collections

from zlejrob.exceptions import OffTheBoardError

class Runner:
    COLORS = ('R', 'G', 'B')
    def __init__(self, width=16, height=12, max_steps=1000):
        self.width  = width
        self.height = height
        self.max_steps = max_steps

    def move(self, position, direction):
        """Move from position in direction."""
        if direction == 0:
            if position % self.width == self.width - 1:
                raise OffTheBoardError
            else:
                return position + 1
        elif direction == 1:
            if position >= (self.height - 1) * self.width:
                raise OffTheBoardError
            else:
                return position + self.width
        elif direction == 2:
            if position % self.width == 0:
                raise OffTheBoardError
            else:
                return position - 1
        elif direction == 3:
            if position < self.width:
                raise OffTheBoardError
            else:
                return position - self.width
        else:
            raise ValueError('No direction %s.' % direction)

    def turn(self, direction, turn):
        """Rotate from direction."""
        if turn == 'L':
            new = direction - 1
        elif turn == 'R':
            new = direction + 1
        else:
            raise ValueError('No rotational direction %s.' % turn)
        return new % 4

    def collected_all(self):
        """Have we collected all the stars?"""
        for position,color in enumerate(self.board):
            if color in self.COLORS  and self.reached[position] == False:
                return False
        return True

    def count(self):
        """Get number of collected stars and reached fields."""
        collected = 0
        for position,color in enumerate(self.board):
            if color in self.COLORS and self.reached[position] == True:
                collected = collected + 1

        return (collected, self.reached.count(True))

    def run(self, puzzle, instructions):
        """Run instruction set on puzzle

        Args:
            puzzle: dict with puzzle information
            instructions: list of functions
        Returns:
            tuple (stars collected, squares reached)
        """
        # Instruction queue
        queue = collections.deque(instructions[0])

        # Robot setup
        position = puzzle['robotCol'] + self.width * puzzle['robotRow']
        direction = puzzle['robotDir']

        # Local board with color changes
        board = list(puzzle['board'])

        # Original board; do not touch
        self.board = puzzle['board']

        # Reached fields
        self.reached = [False] * self.height * self.width
        self.reached[position] = True

        # Step counter
        steps = 0

        while queue:
            steps = steps + 1
            if steps > self.max_steps:
                # Step limit exceeded
                return self.count()

            color, action, instruction = queue.popleft()

            if color != '_' and color != board[position].lower():
                # Instruction skipped because of its color
                continue

            if action == 'F':
                try:
                    position = self.move(position, direction)
                except OffTheBoardError:
                    # Fallen off the board
                    return self.count()

                if board[position] == ' ':
                    # Fallen off the board
                    return self.count()

                self.reached[position] = True
                if self.collected_all():
                    # Collected all stars
                    return self.count()

            elif action in ['L', 'R']:
                direction = self.turn(direction, action)
            elif action in ['r', 'g', 'b']:
                board[position] = action
            elif int(action) > 0:
                queue.extendleft(reversed(instructions[int(action) - 1]))
            else:
                raise ValueError('No action: %s.' % action)

        # Ran out of instructions
        return self.count()
