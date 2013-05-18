import unittest
import zlejrob.parser

class ParserTest(unittest.TestCase):
    instructions = (
        (('_', 'F', 0), ('_', '2', 1), ('_', '4', 2), ('_', 'F', 3),
         ('_', 'F', 4), ('_', 'F', 5), ('g', '4', 6), ('_', 'R', 7),
         ('_', 'F', 8), ('_', 'F', 9)),
        (('_', 'R', 10),),
        (),
        (('r', 'L', 30), ('_', 'F', 31)),
        (),
    )

    program = "_F_2_4_F_F_Fg4_R_F_F|_R||rL_F||"

    def setUp(self):
        self.parser = zlejrob.parser.Parser()

    def test_instructions_from_string(self):
        instructions = self.parser.instructions_from_string(self.program)
        self.assertEqual(self.instructions, instructions)

    def test_string_from_instructions(self):
        program = self.parser.string_from_instructions(self.instructions)
        self.assertEqual(self.program, program)


if __name__ == '__main__':
    unittest.main()
