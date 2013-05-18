import unittest2
import zlejrob.parser

class ParserTest(unittest2.TestCase):
    def setUp(self):
        self.parser = zlejrob.parser.Parser()

    def test_instructions_from_string(self):
        instructions = self.parser.instructions_from_string(
            "_F_2_4_F_F_F_F_F_F_F|_R||_L_F||"
        )
        self.assertEquals( 2, instructions[0][2][2])
        self.assertEquals(10, instructions[1][0][2])
        self.assertEquals([
            [('_', 'F', 0), ('_', '2', 1), ('_', '4', 2), ('_', 'F', 3),
             ('_', 'F', 4), ('_', 'F', 5), ('_', 'F', 6), ('_', 'F', 7),
             ('_', 'F', 8), ('_', 'F', 9)],
            [('_', 'R', 10)],
            [],
            [('_', 'L', 30), ('_', 'F', 31)],
            [],
            [],
        ], instructions)


if __name__ == '__main__':
    unittest2.main()
