import collections

from zlejrob.exceptions import OffTheBoardError

class Runner:
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
            raise ValueError('No such direction.')

    def turn(self, direction, turn):
        """Rotate from direction."""
        if turn == 'L':
            new = direction - 1
        elif turn == 'R':
            new = direction + 1
        else:
            raise ValueError('No such rotation direction.')
        return new % 4

    def collected_all(self, board, reached):
        """Have we collected all the stars?"""
        for position,color in enumerate(board):
            if color == 'B' and reached[position] == False:
                return False
        return True

    def count(self, board, reached):
        """Get collected stars, reached fields, and unused instructions."""
        collected = 0; unused = 0
        for position,color in enumerate(board):
            if color == 'B' and reached[position] == True:
                collected = collected + 1

        return (collected, len([x for x in reached if x == True]), unused)

    def run(self, puzzle, instructions):
        """Run instruction set on puzzle

        :param dict puzzle
        :param list instructions list of functions, where function is list of instructions
        :return tuple (stars collected, squares reached, instructions skipped)
        """
        queue = collections.deque(instructions[0])
        position = puzzle['robotCol'] + self.width*puzzle['robotRow']
        direction = puzzle['robotDir']
        board = puzzle['board']
        steps = 0

        reached = [False] * self.height * self.width
        reached[position] = True

        while queue:
            steps = steps + 1
            if steps > self.max_steps:
                # Step limit exceeded
                return self.count(board, reached)

            color, action = queue.popleft()
            if color != '_' and color != board[position].lower():
                # Instruction skipped because of its color
                continue

            if action == 'F':
                try:
                    position = self.move(position, direction)
                except OffTheBoardError:
                    # Fallen off the board
                    return self.count(board, reached)

                if board[position] == ' ':
                    # Fallen off the board
                    return self.count(board, reached)

                reached[position] = True
                if self.collected_all(board, reached):
                    # Collected all stars
                    return self.count(board, reached)

            elif action == 'L' or action == 'R':
                direction = self.turn(direction, action)
            else:
                raise NotImplementedError

        # Ran out of instructions
        return self.count(board, reached)
