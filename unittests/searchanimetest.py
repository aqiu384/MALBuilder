import unittest

from unittests import basemalbtest


class SearchAnimeTest(basemalbtest.BaseMalbTest):
    def test_log(self):
        response = self.login()
        self.assertTrue('Filter' in response.data.decode('utf-8'))

        response = self.navigate_to('/addanime')
        self.assertTrue('Search' in response.data.decode('utf-8'))

        response = self.logout()
        self.assertTrue('Please' in response.data.decode('utf-8'))

if __name__ == '__main__':
    unittest.main()