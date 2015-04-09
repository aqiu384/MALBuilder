import unittest

from unittests import BaseMalbTester


UPDATE_DATA = {
    'edit_form-myScore_0': 8,
    'edit_form-myEpisodes_0': 1,
}


class UpdateAnimeTest(BaseMalbTester.BaseMalbTest):

    def test_update_through_frontend(self):
        """Test update functionality through frontend"""
        # Login
        self.login()
        self.navigate_to('/updateanime')

        page = self.submit_to('/updateanime', UPDATE_DATA).data.decode('utf-8')

        self.assertTrue('<option selected value="8">' in page)
        self.assertTrue('My Episodes Watched: 1' in page)

if __name__ == '__main__':
    unittest.main()