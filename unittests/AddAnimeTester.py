import unittest

from unittests import BaseMalbTester


DEFAULT_SEARCH = {

}

DEFAULT_ADD = {
    'add_form-myStatus_0': 1,
    'add_form-myStatus_1': 1,
    'add_form-myStatus_2': 1
}


class AddAnimeTest(BaseMalbTester.BaseMalbTest):
    def test_default_search(self):
        """Test default search returns results in alphabetic order"""
        self.login()
        self.navigate_to('/searchanime')

        page = self.submit_to('/searchanime', DEFAULT_SEARCH).data.decode('utf-8')

        self.assertTrue('<form name="addanime" method="POST" id="addanimeform">' in page)

    def test_default_search_and_add(self):
        """Test adding anime from default search results"""

        # Do not execute out of app/data!

        self.login()
        self.navigate_to('searchanime')
        self.submit_to('/searchanime', DEFAULT_SEARCH)
        self.submit_to('/addanime', DEFAULT_ADD)

        page = self.navigate_to('/updateanime').data.decode('utf-8')

        self.assertTrue('.hack//Liminality' in page)
        self.assertTrue('.hack//Sign' in page)
        self.assertTrue('.hack//Tasogare no Udewa Densetsu' in page)

if __name__ == '__main__':
    unittest.main()