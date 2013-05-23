import json
import unittest

from zlejrob.client import Client
from zlejrob.test import puzzles

class ClientTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_get_puzzle(self):
        puzzle = puzzles.puzzles['arbitrary_counting']
        puzzle['board'] = ''.join(puzzle['board'])
        self.assertEqual(json.loads(self.client.get_puzzle(1539)), puzzle)


if __name__ == '__main__':
    unittest.main()
