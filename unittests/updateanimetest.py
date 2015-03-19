import unittest

from unittests import basemalbtest


UPDATE_DATA = {
    'edit_form-myScore_0': 7,
    'edit_form-myEpisodes_0': 7,
}

UPDATE_DATA2 = {
    'edit_form-myScore_0': 7,
    'edit_form-myEpisodes_0': 7,
}


class UpdateAnimeTest(basemalbtest.BaseMalbTest):
    # test_update_through_backend(self):
    #   pass

    def test_update_through_frontend(self):
        """Test update functionality through frontend"""
        # Login
        response = self.login()
        self.assertTrue('Filter' in response.data.decode('utf-8'))

        # Go to "Update Anime" page
        response = self.navigate_to('/updateanime')
        self.assertTrue('Update' in response.data.decode('utf-8'))

        # Fill out form and submit
        response = self.submit_to('/updateanime', UPDATE_DATA)
        self.assertTrue('My Episodes Watched: 7' in response.data.decode('utf-8'))

        # Fill out form and submit
        response = self.submit_to('/updateanime', UPDATE_DATA2)
        self.assertTrue('My Episodes Watched: 7' in response.data.decode('utf-8'))

        # Logout
        response = self.logout()
        self.assertTrue('Please' in response.data.decode('utf-8'))

if __name__ == '__main__':
    unittest.main()