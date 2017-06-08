import re

import requests
from bs4 import BeautifulSoup

from .exceptions import UnexpectedHTTPStatusCode

class Client:
    baseurl = "http://robozzle.com/"

    def __init__(self, settings):
        self.settings = settings
        self.session = requests.Session()

    def login(self):
        """Log into robozzle.com"""
        url = self.baseurl + "login.aspx"

        # get login page
        response = self.session.get(url, allow_redirects=False)
        if response.status_code == 302:
            # we're already logged in
            return

        # csrf protection
        content = response.text
        validation = re.search('id="__EVENTVALIDATION" value="(.*?)"', content)
        viewstate = re.search('id="__VIEWSTATE" value="(.*?)"', content)

        # post data
        params = {
            '__VIEWSTATE': viewstate.group(1),
            '__EVENTVALIDATION': validation.group(1),
            'UserEmail': self.settings['name'],
            'UserPass': self.settings['pass'],
            'Submit1': 'Log On',
        }

        response = self.session.post(url, params, allow_redirects=False)
        if response.status_code != 302:
            raise UnexpectedHTTPStatusCode('Could not log in.')

    def get_puzzle(self, id):
        """Fetch valid json puzzle string from puzzle id."""
        id = str(id)
        url = self.baseurl + "js/play.aspx?puzzle=" + id
        content = self.session.get(url).text
        if re.search('error occurred while processing your request', content):
            # Strictly speaking not a http status code, but it should be!
            raise UnexpectedHTTPStatusCode("Puzzle %s probably doesn't exist." % id)

        puzzle = re.search('var puzzles = \[(.*?)\];', content, re.DOTALL)
        if puzzle is None:
            raise RuntimeError("Puzzle string not in response.")
        return re.sub('^ *([a-zA-Z]*):', '  "\\1":', puzzle.group(1), 0, re.MULTILINE)

    def get_puzzlelist(self, sort_by="campaign", filter_by=None):
        """Get list of existing puzzles."""
        self.login()
        response = self.session.get(self.baseurl + "js/index.aspx?sortby=" + sort_by)

        puzzles = []
        soup = BeautifulSoup(response.text, "lxml")
        for row in soup.table.find_all('tr'):
            cells = row.find_all('td')
            if len(cells) == 0:
                continue

            puzzle = ({
                'id':         str(cells[0].contents[0]),
                'title':      str(cells[1].contents[0]),
                'solved':     str(cells[2].contents[0]),
                'author':     str(cells[3].contents[0]),
                'difficulty': str(cells[4].contents[0]),
                'liked':      str(cells[5].contents[0]),
                'comments':   str(cells[6].contents[0]),
            })

            if filter_by:
                if puzzle[filter_by[0]] != filter_by[1]:
                    continue

            puzzles.append(puzzle)
        return puzzles

    def submit(self, level, solution):
        """Submit a problem solution."""
        self.login()

        url = self.baseurl + "js/submit.aspx"
        params = {
            'solution': solution,
            'levelId': level,
        }

        response = self.session.post(url, params, allow_redirects=False)
        if response.status_code != 200:
            raise UnexpectedHTTPStatusCode('Solution could not be submitted.')
