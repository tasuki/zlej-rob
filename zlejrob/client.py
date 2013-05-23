import re
import requests

from zlejrob.exceptions import UnexpectedHTTPStatusCode

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
        url = self.baseurl + "js/play.aspx?puzzle=" + str(id)
        content = self.session.get(url).text
        puzzle = re.search('var puzzles = \[(.*?)\];', content, re.DOTALL)
        return re.sub('([a-zA-Z]*):', '"\\1":', puzzle.group(1))

    def get_puzzlelist(self):
        """Get list of existing puzzles."""
        self.login()
        response = self.session.get(self.baseurl + "js/index.aspx?sortby=date")
        # TODO
