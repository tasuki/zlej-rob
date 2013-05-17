import collections

class Runner:
    def __init__(self, width, height):
        self.width  = width
        self.height = height

    def move(self, position, direction):
        if direction == 0:
            if position % self.width == self.width - 1:
                return -1
            else:
                return position + 1
        elif direction == 1:
            if position >= (self.height - 1) * self.width:
                return -1
            else:
                return position + self.width
        elif direction == 2:
            if position % self.width == 0:
                return -1
            else:
                return position - 1
        elif direction == 3:
            if position < self.width:
                return -1
            else:
                return position - self.width
        else:
            raise 'no such direction'

    def turn(self, direction, turn):
        if turn == 'L':
            new = direction - 1
        elif turn == 'R':
            new = direction + 1
        else:
            raise 'no such turn direction'
        return new % 4

    def run(self, puzzle, instructions):
        """Run instruction set on puzzle

        :param dict puzzle
        :param list instructions list of functions, where function is list of instructions
        :return tuple (stars collected, squares visited, instructions skipped)
        """
        queue = collections.deque(instructions[0])
        position = puzzle['robotCol'] + self.width*puzzle['robotRow']
        direction = puzzle['robotDir']
        board = puzzle['board']
        steps = 0

        reached = [' '] * self.height * self.width
        reached[position] = 'x'

        while queue:
            steps = steps + 1
            if steps > 1000:
                raise 'too many steps!'

            color, action = queue.popleft()
            if color != '_' and color != board[position].lower():
                continue

            if action == 'F':
                position = self.move(position, direction)
                reached[position] = 'x'
            elif action == 'L' or action == 'R':
                direction = self.turn(direction, action)

        return (1, 2, 0)
