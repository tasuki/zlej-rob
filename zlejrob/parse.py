import json
import re

def instructions_from_string(program):
    """Get instruction list from a string.

    Return a list of functions. A function is a list of instructions,
    each of which is a tuple of (color condition, action, instruction id)
    """
    split = re.split('\|', program)
    split.pop()
    instructions = [list(i) for i in split]
    for k,func in enumerate(instructions):
        instructions[k] = tuple(tuple(func[i:i+2] + [10*k+i/2])
                                      for i in range(0, len(func), 2))
    return tuple(instructions)

def string_from_instructions(instructions):
    """Get program string from instruction list"""
    funcs = []
    for func in instructions:
        funcs.append(''.join([instruction[0] + instruction[1]
                              for instruction in func]))

    return ''.join([func + '|' for func in funcs])

def puzzle_from_json(string):
    """Get puzzle dictionary from json string."""
    puzzle = json.loads(string)
    puzzle['board'] = list(puzzle['board'])
    return puzzle
