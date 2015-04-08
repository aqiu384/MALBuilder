import unittest
import src.malb as MALB

from unittests import basemalbtest
from src import app, db


UPDATE_DATA = {
    'edit_form-myScore_0': 8,
    'edit_form-myEpisodes_0': 1,
}

ORIGINAL_UPDATE_DATA = {
    'edit_form-myScore_0': 0,
    'edit_form-myEpisodes_0': 0,
}


class MalTransactionTest(basemalbtest.BaseMalbTest):
    def setUp(self):
        app.config['MAL_TRANSACTIONS_ENABLED'] = True
        self.setUpHelper()

    def revertMalTransaction(self, page, data):
        self.submit_to(page, data)

    def test_update_through_frontend(self):
        """Test update functionality through frontend"""
        # Login
        self.login()
        self.navigate_to('/updateanime')
        self.submit_to('/updateanime', UPDATE_DATA)
        self.navigate_to('/sync')

        page = self.navigate_to('/updateanime').data.decode('utf-8')

        self.assertTrue('<option selected value="8">' in page)
        self.assertTrue('My Episodes Watched: 1' in page)

        self.submit_to('/updateanime', ORIGINAL_UPDATE_DATA)

if __name__ == '__main__':
    unittest.main()