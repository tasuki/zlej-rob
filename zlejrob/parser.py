import re

class Parser:
    def instructions_from_string(self, program):
        """Get instruction list from a string.

        Return a list of functions. A function is a list of instructions,
        each of which is a tuple of (color condition, action, instruction id)
        """
        instructions = [list(i) for i in re.split('\|', program)]
        for k,func in enumerate(instructions):
            instructions[k] = [tuple(func[i:i+2] + [10*k+i/2])
                               for i in range(0, len(func), 2)]
        return instructions
