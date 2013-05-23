import re
import urllib.request

class Client:
    baseurl = "http://robozzle.com/"

    def get_puzzle(self, id):
        """Fetch valid json puzzle string from puzzle id."""
        url = self.baseurl + "js/play.aspx?puzzle=" + str(id)
        handle = urllib.request.urlopen(url)
        content = handle.read().decode()
        handle.close()
        puzzle = re.search('var puzzles = \[(.*?)\];', content, re.DOTALL)
        return re.sub('([a-zA-Z]*):', '"\\1":', puzzle.group(1))

    def get_puzzlelist(self):
        """Get list of existing puzzles."""
        pass
