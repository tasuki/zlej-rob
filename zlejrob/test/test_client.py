import json
import unittest

from .. import Client, config
from . import puzzles

class ClientTest(unittest.TestCase):
    def setUp(self):
        self.client = Client({
            'name': config.robozzle_name,
            'pass': config.robozzle_pass,
        })

    def test_login(self):
        # This one should log in.
        self.client.login()

        # Should already be logged in.
        # Obviously we're not testing that, we're testing that
        # login isn't broken when when called multiple times.
        self.client.login()

    def test_get_puzzle(self):
        puzzle = puzzles.puzzles['arbitrary_counting']
        puzzle['board'] = ''.join(puzzle['board'])
        self.assertEqual(json.loads(self.client.get_puzzle(1539)), puzzle)

    def test_get_puzzlelist(self):
        author = '<a href="/user.aspx?name=igoro">igoro</a>'
        puzzles = self.client.get_puzzlelist(filter_by=('author', author))
        self.assertEqual(24, len(puzzles))

    def test_submit(self):
        self.client.submit(27, '_F_L_F_R_1|||||')

if __name__ == '__main__':
    unittest.main()
